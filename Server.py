from flask import Flask, render_template
from os.path import join as path_join
import os
from pathlib import Path
from Note import Note, Notebook, load_note

app = Flask(__name__)


""" The Database module lists notes for given folders and reads their
    content
"""
class Database:

    def __init__(self):
        self.root = '/home/cstelz/Notes/notes'

    def get_dir(self, path=''):
        dirs = list()
        files = list()
        p = Path(path_join(self.root, path))
        
        if not p.is_dir():
            raise DatabaseReadError('Given Path is not a directory')
        else:
            r_files = []
            r_dirs = []
            for root, dirs, files in os.walk(str(p)):
                print(root)
                for name in files:
                    if name.endswith(".md"):
                        path = path_join(root, name)
                        r_files.append(load_note(path, only_metadata=True))
                for name in dirs:
                    r_dirs.append(Notebook(name, "Not"))
        print(r_files)
        print(r_dirs)
        return (r_files, r_dirs)

class DatabaseReadError(Exception):
    pass

db = Database()

@app.route('/')
def index():
    files, dirs = db.get_dir()
    print(files)
    return render_template("dir.html", notes=files)


