import os
import json


def recompile_ui():
    directory = os.path.split(__file__)[0]
    try:
        index = json.load(open(os.path.join(directory, "file_index.json"), "r"))
    except Exception:
        index = {}
    index_changed = False

    for file in os.scandir(directory):
        if not file.name.endswith(".ui"): continue
        last_modified = os.path.getmtime(file.path)
        if file.name in index and index[file.name] == last_modified: continue
        index[file.name] = last_modified
        index_changed = True
        print(f"Recompiling {file.name}...")
        os.system(f"pyuic6 {file.path} -o {file.path[:-2] + 'py'} -x")

    if index_changed:
        json.dump(index, open(os.path.join(directory, "file_index.json"), "w"))


recompile_ui()
