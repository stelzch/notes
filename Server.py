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
        self.root = Path(os.getcwd()+"/notes")

    def get_dir(self, path=''):
        """Loads a list of subdirs and files from a directory

        Args:
            path: the relative path

        Returns:
            A tuple of files, dirs and parent found
            
            - files is a list of the named note-tuple with an empty content variable
            - dirs is a list of directory names
            - parent is the path to the parent directory relative to the databases root dir


        Raises:
            DatabaseReadError: The given path wasn't a directory
        """
        dirs = list()
        files = list()
        p = Path(path_join(str(self.root), path))
        if path is not '':
            parent = p.parent.relative_to(self.root)
        else:
            parent = ""
        if not p.is_dir():
            raise DatabaseReadError('Given Path is not a directory')
        else:
            for file in p.iterdir():
                if file.is_dir():
                    dirs.append(file.name)
                else:
                    if file.suffix == ".md":
                        print("Loading note %s" % file)
                        files.append(load_note(str(file), True))
        return files, dirs, parent

    def get_note(self, path):
        """Loads a single note from the given path

        Args:
            path: the relative path to the notefile from the databases root directory

        Returns:
            A named-tuple note object

        Raises:
            DatabaseReadError: The given path didn't point at a file
            NoteFileMalformedError: The notefile has an invalid structure or metadata is missing


        """
        notefile = Path(path_join(str(self.root), path))
        parent = notefile.parent.relative_to(self.root)

        """ Security checks go first: We need to check if the given file
            exists at all
        """
        print("Loading "+str(notefile))
        if not notefile.is_file():
            print("Couldn't find "+notefile.read_text())
            raise DatabaseReadError("Notefile couldn't be read.")
        note = load_note(str(notefile))
        return note, parent


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
        notef, parent = db.get_note(note+".md")
    except DatabaseReadError as e:
        return "404"
    rendered = render_note(notef)
    return render_template("note.html", note=notef,
                                        root=parent,
                                        render=rendered)
                                        

@app.route('/<path:directory>')
def view_dir(directory):
    files, dirs, parent = db.get_dir(directory)
    dirs.sort()
    files.sort()
    return render_template("dir.html", dirname=directory,
                                       files=files,
                                       folders=dirs,
                                       root=directory,
                                       parent=parent)

