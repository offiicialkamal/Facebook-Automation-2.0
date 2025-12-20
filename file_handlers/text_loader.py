import os

def read_text(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            # print(content)
            return content
    else:
        print("SORRY NO FILE EXISTS AT ", path)
