import json
from .json_loader import read_json


def update_data(path, key, value):
    old_data = read_json(path)
    data = old_data[key] = value
    with open(path, 'w', encoding="utf-8") as f:
        json.dump(old_data, f, indent=2)
    return data

def write_(path, key, value: dict):
    
    self.update_data(old_data, key, value, path)