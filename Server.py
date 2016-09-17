from flask import Flask
from os.path import join as path_join
from pathlib import Path
from Note import Note, NoteDirectory

app = Flask(__name__)


""" The Database module lists notes for given folders and reads their
    content
"""
class Database:

    def __init__(self):
        self.root = '/home/cstelz/Notes/notes'

    def get_dir(self, path=''):
        dirs = files = []
        p = Path(path_join(self.root, path))
        
        if not p.is_dir():
            raise DatabaseReadError('Given Path is not a directory')
        else:
            for file in p.iterdir():
                suffixes = file.suffixes
                """ Go through all Markdown files in the directory """
                if file.is_dir():
                    dirs.append(NoteDirectory(str(file)))
                else:
                    if len(suffixes) > 0:
                        if suffixes[-1] is  ".md":
                            print("Found Markdown ", str(file))
                            files.append(Note.load(str(file), only_meta=True))
                    
        return result

class DatabaseReadError(Exception):
    pass

db = Database()

@app.route('/')
def index():

    return str(db.get_dir())


app.run(host='0.0.0.0', port=8080)
