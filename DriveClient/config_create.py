import json

config_dict = {'config': {'parent': 'drive',
                          'print_dir': False
                          },
               'paths': {'token': 'D:\Git\python-projects\DriveClient\\token.json',
                         'download': 'D:\Git\python-projects\DriveClient\\',
                         'credentials': 'D:\Git\python-projects\DriveClient\credentials.json',
                         },
               'scopes': ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.appfolder'],
               'extensions': {'document': [('html', 'text/html'), ('zip', 'application/zip'), ('txt', 'text/plain'),
                                           ('rtf', 'application/rtf'),
                                           ('odt', 'application/vnd.oasis.opendocument.text'),
                                           ('pdf', 'application/pdf'), ('epub', 'application/epub+zip'),
                                           ('docx', 'application/vnd.openxmlformats-officedocument.wordprocessingml.'
                                                    'document')
                                           ],
                              'spreadsheet': [('xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.'
                                                       'sheet'),
                                              ('ods', 'application/x-vnd.oasis.opendocument.spreadsheet'),
                                              ('pdf', 'application/pdf'), ('csv', 'text/csv'),
                                              ('txt', 'text/tab-separated-values'), ('zip', 'application/zip'),
                                              ],
                              'presentation': [('pptx', 'application/vnd.openxmlformats-officedocument.presentationml.'
                                                        'presentation'),
                                               ('odp', 'application/vnd.oasis.opendocument.presentation'),
                                               ('pdf', 'application/pdf'),
                                               ('txt', 'text/plain')
                                               ],
                              'drawing': [('jpeg', 'image/jpeg'), ('png', 'image/png'), ('xml', 'image/svg+xml'),
                                          ('pdf', 'application/pdf')]
                              },
               }
with open('config.json', 'w') as f:
    string = json.dumps(config_dict, indent=4, separators=(',', ': '), sort_keys=False)
    f.write(string)
