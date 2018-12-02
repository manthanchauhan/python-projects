import json

config_dict = {'parent': 'drive',
               'print_dir': False}
with open('config.json', 'w') as f:
    json.dump(config_dict, f)
