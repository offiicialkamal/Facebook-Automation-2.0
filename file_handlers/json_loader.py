import os
import json

def read_json(path):
    """reads and provodes the json file content as python dictionary"""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        # print(content)
        data = json.loads(content)
        return dict(data)