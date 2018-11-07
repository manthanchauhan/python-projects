from __future__ import print_function
from googleapiclient.discovery import build
import googleapiclient
from httplib2 import Http
from oauth2client import file, client, tools
import warnings
import sys
import os
import argparse
import io
import http


SCOPES = 'https://www.googleapis.com/auth/drive'
warnings.filterwarnings('ignore')
token = 'D:\Git\python-projects\google drive terminal\\token.json'
download_path = 'D:\Git\python-projects\google drive terminal\\'


class DriveClient(object):
    def __init__(self):
        store = file.Storage(token)
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('D:\Git\python-projects\google drive terminal\credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
            print('logged in')
            sys.exit()
        self.service = build('drive', 'v3', http=creds.authorize(Http()))

        parser = argparse.ArgumentParser(description='command-line suite for google drive.')
        parser.add_argument('command', help='subcommand to run', action='store')    
        args = parser.parse_args(sys.argv[1:2])
        try:
            getattr(self, args.command)()
        except AttributeError:
            print('Invalid command')
            print('for help use: "Drive client -h" or "DriveClient --help"')
    
    def logout(self):
        try:
            os.remove(token)
        except FileNotFoundError:
            pass
        print('logged out successfully')
        sys.exit()

    def listfiles(self):
        parser = argparse.ArgumentParser(description='view files')
        parser.add_argument('number', help='number of pages to print', action='store', type=int)
        parser.add_argument('-det', '--detailed', help='print file details', action='store_true')
        args = parser.parse_args(sys.argv[2:])
        number = args.number
        result = []
        page_token = None
        while True:
            if not number:
                break
            number -= 1
            param = {}
            if page_token:
                param['pageToken'] = page_token
            files = self.service.files().list(**param).execute()
            Files = files['files']
            if not args.detailed:
                result.extend([File['name'] for File in Files])
            else:
                result.extend(Files)
            page_token = files.get('nextPageToken')
            if not page_token:
                break
        for i in range(0, len(result)):
            try:
                if not args.detailed:
                    print('[' + str(i+1) + '] ' + result[i])
                else:
                    print('[' + str(i+1) + '] ' + result[i]['name'])
                    for tpl in result[i]:
                        if tpl != 'name':
                            print('\t' + tpl + ' : ' + str(result[i][tpl]))
            except:
                print('[' + str(i+1) + '] -----<encoding error in filename>-----')
        sys.exit()  

    def download(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('filename', help='name of file to be downloaded', action='store')
        parser.add_argument('address', help='location to download file, "default" for default location', action='store')
        args = parser.parse_args(sys.argv[2:])
        page_token = None
        fileID = None
        while True:
            param = {}
            if page_token:
                param['pageToken'] = page_token
            files = self.service.files().list(**param).execute()
            Files = files['files']
            for File in Files:
                if File['name'] == args.filename:
                    fileID = File['id']
                    if File['mimeType'].find('google') != -1:
                        print('use export method for google docs')
                        sys.exit()
                    break
            if fileID != None:
                break
            page_token = files.get('nextPageToken')
            if not page_token:
                break
        if fileID is None:
            print('file not found')
            sys.exit()
        request = self.service.files().get_media(fileId= fileID)
        fh = io.BytesIO()
        downloader = googleapiclient.http.MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print('Downloaded %d'%(status.progress()*100))
        if args.address == 'default':
            address = download_path + args.filename
        else:
            address = args.address    
        with open(address, 'wb') as File:
            File.write(fh.getvalue())
        File.close()
        print(args.filename + ' was downloaded successfully')
        sys.exit()

if __name__ == '__main__':
    DriveClient()