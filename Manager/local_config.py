import json

def load_local_config():
    with open('local_data.json', 'r') as f:
        config = json.load(f)
    return config

def save_local_config(data):
    with open('local_data.json', 'w') as f:
        json.dump(data, f, indent=4)