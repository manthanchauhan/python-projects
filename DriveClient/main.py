from googleapiclient.discovery import build
import googleapiclient
from httplib2 import Http
from oauth2client import file, client, tools
import warnings
import sys
import os
import argparse
import io
import json


warnings.filterwarnings('ignore')
config_file = 'D:\Git\python-projects\DriveClient\config.json'


class DriveClient(object):
    def __init__(self):
        """logs in the client google account in case of logout
           otherwise, processes the given command
        """
        self.config_file = config_file              # loads configuration dict
        if os.path.isfile(self.config_file):
            with open(self.config_file) as con:
                config_dict = json.load(con)

        self.config = config_dict['config']            # login
        self.extensions = config_dict['extensions']
        self.paths = config_dict['paths']
        self.scopes = config_dict['scopes']
        store = file.Storage(self.paths['token'])     # creates credential object of 'token'
        creds = store.get()             # reads credential aka token
        if creds is None:
            if len(sys.argv) > 1:
                if self.config['print_dir']:
                    print('Please login before proceeding')
                print('For login use: DriveClient <no_command>')
                sys.exit()
            # create 'flow' object for authentication
            flow = client.flow_from_clientsecrets(self.paths['credentials'], self.scopes)
            tools.run_flow(flow, store)  # open page in browser, get token after authentication and store it
            if self.config['print_dir']:
                print('logged in')
            sys.exit(0)
        self.service = build('drive', 'v2', http=creds.authorize(Http()))

        parser = argparse.ArgumentParser(description='command-line suite for google drive.')  # parse arguments
        parser.add_argument('command', help='sub-command to run', action='store')
        args = parser.parse_args(sys.argv[1:2])
        if not getattr(self, args.command, False):
            print('Invalid command')
            if self.config['print_dir']:
                print('for help use: "DriveClient -h" or "DriveClient --help"')
        else:
            getattr(self, args.command)()
        config_dict['config'] = self.config
        config_dict['extensions'] = self.extensions
        config_dict['paths'] = self.paths
        config_dict['scopes'] = self.scopes
        with open(self.config_file, 'w') as con:            # update configuration file
            string = json.dumps(config_dict, indent=4, separators=(',', ': '), sort_keys=False)
            con.write(string)

    def logout(self):
        """logout from current Google account
        """
        try:
            os.remove(self.paths['token'])
        except FileNotFoundError:
            pass
        if self.config['print_dir']:
            print('logged out successfully')

    def p_dir(self):
        """toggles 'print_dir' to show/hide user directions
        """
        self.config['print_dir'] = not self.config['print_dir']

    def cd(self):
        """changes current working directory
        """
        parser = argparse.ArgumentParser(description='change working user directory')
        parser.add_argument('destination', help='new destination to make parent directory', action='store', type=str)
        if len(sys.argv[1:]) == 1:
            current_parent = self.config['parent']
            parent = self.service.parents().list(fileId=current_parent).execute()
            if len(parent['items']) == 0:
                if self.config['print_dir']:
                    print('root directory reached')
                return
            self.config['parent'] = parent['items'][0]['id']
        else:
            args = parser.parse_args(sys.argv[2:])
            if args.destination == 'root':
                self.config['parent'] = self.config['root']
                return
            if args.destination == 'this':
                parent = self.service.files().get(fileId=self.config['parent']).execute()
                print(parent['title'])
                return
            page_token = None
            while True:
                children = self.service.files().list(q='\''+str(self.config['parent'])+'\' in parents and title = '
                                                     '\'' + args.destination + '\'', fields='nextPageToken, '
                                                     'items(title, id)', pageToken=page_token).execute()
                items = children['items']
                if len(items) != 0:
                    self.config['parent'] = items[0]['id']
                    return
                page_token = children.get('nextPageToken')
                if page_token is None:
                    print('invalid destination')
                    return

    def list(self):
        """list files stored in current Google Account (GDrive) directory
        """
        parser = argparse.ArgumentParser(description='view files')
        parser.add_argument('pages', help='range of pages to print ie, "page_x"-"page_y" (both inclusive)',
                            action='store', type=str)
        parser.add_argument('-det', '--detailed', help='print file details', action='store_true')
        parser.add_argument('-dir', '--directory', help='show only directories', action='store_true')
        args = parser.parse_args(sys.argv[2:])
        pages = args.pages.split('-')
        if len(pages) != 2:
            print('Invalid range format')
            if self.config['print_dir']:
                print('To se help use: DriveClient list_files -h')
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
            files = self.service.files().list(q='\'' + str(self.config['parent']) + '\' in parents', spaces='drive',
                                              fields='nextPageToken, items(title, createdDate, lastViewedByMeDate, '
                                                     'modifiedDate, ownerNames, editable, mimeType, parents, id)',
                                              pageToken=page_token).execute()
            if current_page >= pages[0]:
                items = files['items']
                if not args.detailed:
                    if args.directory:
                        result.extend([File['title'] for File in items if 'folder' in File['mimeType']])
                    else:
                        result.extend([File['title'] for File in items])
                else:
                    if args.directory:
                        result.extend([item for item in items if 'folder' in item['mimeType']])
                    else:
                        result.extend(items)
            page_token = files.get('nextPageToken')
            if not page_token:
                break

        if len(result) == 0:
            if self.config['print_dir']:
                print('parent directory is empty')
        for i in range(0, len(result)):         # presentation of files to user
            if not args.detailed:
                try:
                    print('[' + str(i+1 + (pages[0]-1)*100) + '] ' + result[i])
                except UnicodeEncodeError:
                    print('[' + str(i + 1 + (pages[0] - 1) * 100) + '] -----<encoding error in filename>-----')
            else:
                try:
                    print('[' + str(i+1 + (pages[0]-1)*100) + '] ' + result[i]['title'])
                except UnicodeEncodeError:
                    print('[' + str(i + 1 + (pages[0] - 1) * 100) + '] -----<encoding error in filename>-----')
                for key in result[i]:
                    if key != 'title':
                        try:
                            print('\t' + key + ' : ' + str(result[i][key]))
                        except UnicodeEncodeError:
                            print('\t' + '-----<encoding error in ' + key + '>-----')

    def download(self):
        """download a file from GDrive
        """
        parser = argparse.ArgumentParser(description='download some file')
        parser.add_argument('filename', help='name of file to be downloaded', action='store')
        parser.add_argument('address', help='location to download file, "default" for default location', action='store')
        args = parser.parse_args(sys.argv[2:])
        page_token = None
        while True:
            files = self.service.files().list(q='\'' + str(self.config['parent']) + '\' in parents and title = \'' +
                                                args.filename + '\'', fields='nextPageToken, items(id, mimeType)',
                                                pageToken=page_token).execute()
            items = files['items']
            if len(items) != 0:
                file_id = items[0]['id']
                mime_type = items[0]['mimeType']
                if mime_type.find('google') != -1:
                    print('use export method for google docs')
                    return
                request = self.service.files().get_media(fileId=file_id)    # initiate download
                fh = io.BytesIO()
                downloader = googleapiclient.http.MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    print('%d' % (status.progress()*100), end='%')
                    print(' Downloaded')
                if args.address == 'default':               # save downloaded file
                    address = self.paths['download'] + args.filename
                else:
                    address = args.address
                with open(address, 'wb') as File:
                    File.write(fh.getvalue())
                File.close()
                print(args.filename + ' was downloaded successfully')
                return
            page_token = files.get('nextPageToken')
            if page_token is None:
                print('requested file not found')
                return

    def export(self):
        """export any Google document to another system compatible format
        """
        parser = argparse.ArgumentParser(description='export Google documents to compatible formats')
        parser.add_argument('filename', help='name of file to export', action='store')
        parser.add_argument('format', help='format to export to', action='store')
        parser.add_argument('address', help='address to export, "default" for default address', action='store')
        args = parser.parse_args(sys.argv[2:])
        page_token = None
        while True:
            files = self.service.files().list(q='\'' + str(self.config['parent']) + '\' in parents and title = \'' +
                                              args.filename + '\'', fields='nextPageToken, items(id, mimeType)',
                                              pageToken=page_token).execute()
            items = file['items']
            if len(items) != 0:
                file_id = items[0]['id']
                mime_type = items[0]['mimeType']
                if mime_type.find('google') == -1:
                    print('export is only used for google docs, use download otherwise.')
                    return
                if mime_type.find('folder') != -1:
                    print('folders cannot be exported')
                    return
                file_type = mime_type[28:]           # determine present file format
                if file_type not in self.extensions.keys():
                    print('file format either invalid or unsupported by DriveClient')
                    return
                mime_type = None                     # determine required file format
                for tupl in self.extensions[file_type]:
                    if tupl[0] == args.format:
                        mime_type = tupl[1]
                        break
                if mime_type is None:
                    print('conversion format either invalid or unsupported by DriveClient')
                    return
                request = self.service.files().export_media(fileId=file_id, mimeType=mime_type)
                fh = io.BytesIO()
                downloader = googleapiclient.http.MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    print('%d' %(status.progress()*100), end='%')
                    print(' Downloaded')
                if args.address == 'default':
                    address = self.paths['download'] + args.filename + '.' + args.format
                else:
                    address = args.address + '.' + args.format
                with open(address, 'wb') as File:
                    File.write(fh.getvalue())
                File.close()
                print(args.filename + ' was exported successfully')
                return
            page_token = files.get('nextPageToken')
            if page_token is None:
                print('requested file not found')
                return

    def upload(self):
        """upload any file to GDrive
        """
        parser = argparse.ArgumentParser(description='upload any file to GDrive')
        parser.add_argument('filename', help='name of file to upload', action='store')
        args = parser.parse_args(sys.argv[2:])
        try:
            stats = os.stat(args.filename)
        except FileNotFoundError:
            print('file does not exists')
            return
        slash = args.filename.rfind('\\')
        if slash == -1:
            name = args.filename
        else:
            name = args.filename[slash + 1:]
        extension = name.rfind('.')
        extension = name[extension + 1:]
        meta_data = {
            'title': name,
            'parents': [{'id': self.config['parent']}]
        }
        mime_type = None
        for List in self.extensions.values():
            for tupl in List:
                if tupl[0] == extension:
                    mime_type = tupl[1]
        if mime_type is None:
            print('error: unsupported file type')
            return
        media = googleapiclient.http.MediaFileUpload(args.filename, mimetype=mime_type)
        self.service.files().insert(body=meta_data, media_body=media).execute()
        print('file uploaded successfully')

    def find(self):
        parser = argparse.ArgumentParser(description='find any file with filename')
        parser.add_argument('filename', help='name of the file to be searched', action='store')
        parser.add_argument('-det', '--details', help='show the details of the file', action='store_true')
        args = parser.parse_args(sys.argv[2:])
        page_token = None
        while True:
            files = self.service.files().list(q='title contains \' ' + args.filename + '\'', fields='nextPageToken,'
                                              ' items(title, id, mimeType, modifiedDate, ownerNames)', pageToken=
                                              page_token).execute()
            items = files['items']
            if len(items) != 0:
                for i in range(0, len(items)):
                    try:
                        print('[' + str(i+1) + '] ' + items[i]['title'])
                    except UnicodeEncodeError:
                        print('[' + str(i+1) + '] -----<encoding error in filename>-----')
                    if args.details:
                        for key in items[i]:
                            if key != 'title':
                                try:
                                    print('\t' + key + ' : ' + str(items[i][key]))
                                except UnicodeEncodeError:
                                    print('\t' + '-----<encoding error in ' + key + '>-----')
                page_token = files.get('nextPageToken')
                if page_token is None:
                    return
                continue
            else:
                return



    # def translation_dict(self):
    #     try:
    #         os.remove(self.paths['translation'])
    #     except FileNotFoundError:
    #         pass
    #     page_token = None
    #     translation_dict = {}
    #     while True:
    #         files = self.service.files().list(fields='nextPageToken, items(title, id)',
    # pageToken=page_token).execute()
    #         for item in files['items']:
    #             translation_dict[item['title']] = item
    #         page_token = files.get('nextPageToken')
    #         if not page_token:
    #             break
    #     with open(self.paths['translation'], 'w') as f:
    #         string = json.dumps(translation_dict, indent=4, separators=(',', ':'), sort_keys=True)
    #         f.write(string)


if __name__ == '__main__':
    DriveClient()

