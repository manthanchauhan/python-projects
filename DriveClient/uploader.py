from googleapiclient.discovery import build
import googleapiclient
from httplib2 import Http
from oauth2client import file, client, tools
import warnings
import sys
import os
import argparse
import io
from mimetypes import MimeTypes
import urllib.request
import http


export_dict = {'document': [('html', 'text/html'), ('zip', 'application/zip'), ('txt', 'text/plain'),
                            ('rtf', 'application/rtf'), ('odt', 'application/vnd.oasis.opendocument.text'),
                            ('pdf', 'application/pdf'), ('epub', 'application/epub+zip'),
                            ('docx', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                            ],
               'spreadsheet': [('xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                               ('ods', 'application/x-vnd.oasis.opendocument.spreadsheet'), ('pdf', 'application/pdf'),
                               ('csv', 'text/csv'), ('txt', 'text/tab-separated-values'), ('zip', 'application/zip'),
                               ],
               'presentation': [('pptx', 'application/vnd.openxmlformats-officedocument.presentationml.presentation'),
                                ('odp', 'application/vnd.oasis.opendocument.presentation'), ('pdf', 'application/pdf'),
                                ('txt', 'text/plain')
                                ],
               'drawing': [('jpeg', 'image/jpeg'), ('png', 'image/png'), ('xml', 'image/svg+xml'),
                           ('pdf', 'application/pdf')]
               }


scopes = ['https://www.googleapis.com/auth/drive']
warnings.filterwarnings('ignore')
token = 'D:\Git\python-projects\DriveClient\\token.json'
download_path = 'D:\Git\python-projects\DriveClient\\'
client_credentials = 'D:\Git\python-projects\DriveClient\credentials.json'


class DriveClient(object):
    def __init__(self):
        """logs in the client google account in case of logout
           otherwise, processes the given command
        """
        store = file.Storage(token)     # creates credential object of 'token'
        creds = store.get()             # reads credential aka token
        if creds is None:
            if len(sys.argv) > 1:
                print('Please login before proceeding')
                print('For login use: DriveClient <no_command>')
                sys.exit()
            flow = client.flow_from_clientsecrets(client_credentials, scopes)  # create 'flow' object for authentication
            tools.run_flow(flow, store)  # open page in browser, get token after authentication and store it
            print('logged in')
            sys.exit()
        self.service = build('drive', 'v3', http=creds.authorize(Http()))

        parser = argparse.ArgumentParser(description='command-line suite for google drive.')
        parser.add_argument('command', help='sub-command to run', action='store')
        args = parser.parse_args(sys.argv[1:2])
        if not getattr(self, args.command, False):
            print('Invalid command')
            print('for help use: "DriveClient -h" or "DriveClient --help"')
        else:
            getattr(self, args.command)()

    @staticmethod
    def logout():
        """logout from current Google account
        """
        try:
            os.remove(token)
        except FileNotFoundError:
            pass
        print('logged out successfully')

    def list_files(self):
        """list files stored in current Google Account (GDrive)
        """
        parser = argparse.ArgumentParser(description='view files')
        parser.add_argument('pages', help='range of pages to print ie, "page_x"-"page_y" (both inclusive)',
                            action='store', type=str)
        parser.add_argument('-det', '--detailed', help='print file details', action='store_true')
        args = parser.parse_args(sys.argv[2:])
        pages = args.pages.split('-')
        if len(pages) != 2:
            print('Invalid range format.\nTo se help use: DriveClient list_files -h')
            sys.exit()
        pages = [int(s) for s in pages]
        if pages[1] < pages[0] or pages[0] < 0 or pages[1] < 0:
            print('Invalid range')
            sys.exit()
        page_token = None
        current_page = 0
        result = []
        while True:
            current_page += 1
            if current_page > pages[1]:
                break
            param = {}
            if page_token:
                param['pageToken'] = page_token
            files = self.service.files().list(**param).execute()
            if current_page >= pages[0]:
                files_new = files['files']
                if not args.detailed:
                    result.extend([File['name'] for File in files_new])
                else:
                    result.extend(files_new)
            page_token = files.get('nextPageToken')
            if not page_token:
                break
        for i in range(0, len(result)):
            try:
                if not args.detailed:
                    print('[' + str(i+1 + (pages[0]-1)*100) + '] ' + result[i])
                else:
                    print('[' + str(i+1 + (pages[0]-1)*100) + '] ' + result[i]['name'])
                    for tpl in result[i]:
                        if tpl != 'name':
                            print('\t' + tpl + ' : ' + str(result[i][tpl]))
            except UnicodeEncodeError:
                print('[' + str(i+1 + (pages[0]-1)*100) + '] -----<encoding error in filename>-----')

    def download(self):
        """download a file from GDrive
        """
        parser = argparse.ArgumentParser(description='download some file')
        parser.add_argument('filename', help='name of file to be downloaded', action='store')
        parser.add_argument('address', help='location to download file, "default" for default location', action='store')
        args = parser.parse_args(sys.argv[2:])
        page_token = None
        file_id = None

        while True:             # get file ID from filename
            param = {}
            if page_token:
                param['pageToken'] = page_token
            files = self.service.files().list(**param).execute()
            files_new = files['files']
            for File in files_new:
                if File['name'] == args.filename:
                    file_id = File['id']
                    if File['mimeType'].find('google') != -1:
                        print('use export method for google docs')
                        sys.exit()
                    break
            if file_id is not None:
                break
            page_token = files.get('nextPageToken')
            if not page_token:
                break
        if file_id is None:
            print('file not found')
            sys.exit()

        request = self.service.files().get_media(fileId=file_id)    # initiate download
        fh = io.BytesIO()
        downloader = googleapiclient.http.MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print('%d' % (status.progress()*100), end='%')
            print(' Downloaded')

        if args.address == 'default':               # save downloaded file
            address = download_path + args.filename
        else:
            address = args.address
        with open(address, 'wb') as File:
            File.write(fh.getvalue())
        File.close()
        print(args.filename + ' was downloaded successfully')

    def export(self):
        """export any Google document to another system compatible format
        """
        parser = argparse.ArgumentParser(description='export Google documents to compatible formats')
        parser.add_argument('filename', help='name of file to export', action='store')
        parser.add_argument('format', help='format to export to', action='store')
        parser.add_argument('address', help='address to export, "default" for default address', action='store')
        args = parser.parse_args(sys.argv[2:])
        page_token = None
        file_id = None
        MimeType = None
        while True:                 # get file ID and Mime Type form filename
            param = {}
            if page_token:
                param['pageToken'] = page_token
            files = self.service.files().list(**param).execute()
            files_new = files['files']
            for File in files_new:
                if File['name'] == args.filename:
                    MimeType = File['mimeType']
                    file_id = File['id']
                    if File['mimeType'].find('google') == -1:
                        print('export is only used for google docs, use download otherwise.')
                        sys.exit()
                    if File['mimeType'].find('folder') != -1:
                        print('folders cannot be exported')
                        sys.exit()
                    break
            if file_id is not None:
                break
            page_token = files.get('nextPageToken')
            if not page_token:
                break
        if file_id is None:
            print('file not found')
            sys.exit()

        file_type = MimeType[28:]           # determine present file format
        if file_type not in export_dict.keys():
            print('file format either invalid or unsupported by DriveClient')
            sys.exit()

        MimeType = None                     # determine required file format
        for tupl in export_dict[file_type]:
            if tupl[0] == args.format:
                MimeType = tupl[1]
                break

        if MimeType is None:
            print('conversion format either invalid or unsupported by DriveClient')
            sys.exit()
        request = self.service.files().export_media(fileId=file_id, mimeType=MimeType)
        fh = io.BytesIO()
        downloader = googleapiclient.http.MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print('%d' %(status.progress()*100), end='%')
            print(' Downloaded')
        if args.address == 'default':
            address = download_path + args.filename + '.' + args.format
        else:
            address = args.address + '.' + args.format
        with open(address, 'wb') as File:
            File.write(fh.getvalue())
        File.close()
        print(args.filename + ' was downloaded successfully')

    def upload(self):
        """upload any file to GDrive
        """
        parser = argparse.ArgumentParser(description='upload any file to GDrive')
        parser.add_argument('filename', help='name of file to upload', action='store')
        parser.add_argument('address', help='drive: upload in drive, folder: upload in a folder', action='store')
        args = parser.parse_args(sys.argv[2:])
        try:
            stats = os.stat(args.filename)
        except FileNotFoundError:
            print('file does not exists')
            sys.exit()
        size = stats.st_size
        slash = args.filename.rfind('\\')
        if slash == -1:
            name = args.filename
        else:
            name = args.filename[slash + 1:]
        if args.address == 'drive':
            meta_data = {'name': name}
            url = urllib.request.pathname2url(args.filename)
            MimeType = MimeTypes().guess_type(url)[0]
        elif args.address == 'folder':
            pass
        if size <= 5*(10**6):
            media = googleapiclient.http.MediaFileUpload(args.filename, mimetype=MimeType)
        else:
            media = googleapiclient.http.MediaFileUpload(args.filename, mimetype=MimeType, resumable=True)
        self.service.files().create(body=meta_data, media_body=media, fields='id').execute()
        print('file uploaded successfully')


if __name__ == '__main__':
    DriveClient()
