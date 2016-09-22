from flask import Flask, render_template
from os.path import join as path_join
import os
from pathlib import Path
from Note import Note, Notebook, load_note
from Renderer import render_note

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
            for file in p.iterdir():
                if file.is_dir():
                    dirs.append(str(file))
                else:
                    if file.suffix == ".md":
                        files.append(load_note(str(file), True)
        return (files, dirs)

    def get_note(self, path):
        notefile = Path(path_join(self.root, path))

        """ Security checks go first: We need to check if the given file
            exists at all
        """
        print("Loading "+str(notefile))
        if not notefile.is_file():
            print("Couldn't find "+notefile.read_text())
            raise DatabaseReadError("Notefile couldn't be read.")
        note = load_note(str(notefile))
        return(note)


class DatabaseReadError(Exception):
    pass

db = Database()

@app.route('/')
def index():
    ret = view_dir('')
    return ret

@app.route('/<path:note>.md')
def view_note(note):
    try:
        notef = db.get_note(note+".md")
    except DatabaseReadError as e:
        return "404"
    rendered = render_note(notef)
    return render_template("note.html", note=notef,
                                        render=rendered)
                                        

@app.route('/<path:directory>')
def view_dir(directory):
    files, dirs = db.get_dir()
    dirs.sort()
    files.sort()
    return render_template("dir.html", dirname=directory,
                                       files=files,
                                       folders=dirs,
                                       root=directory)
