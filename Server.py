from flask import Flask, render_template, send_file
from os.path import join as path_join
import os
from pathlib import Path
from Note import Note, Notebook, load_note
from Renderer import render_note
from mimetypes import guess_type as guess_mime_type

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
        if p.is_dir():
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
    def get_media(self, file):
        """Loads a media file from the given path

        Args:
            file: the relative path to the file that should be retrieved, e.g. dir/image.png

        Returns:
            A tuple with the absolute filepath and the mimetype

        """
        p = str(Path(path_join(str(self.root), file)))
        mime = str(guess_mime_type(p)[0])
        print("Reading file "+p+"with mime "+mime)
        return (p, mime)

class DatabaseReadError(Exception):
    pass

db = Database()

@app.route('/')
def index():
    ret = view_dir('')
    return ret

def view_note(note):
    try:
        notef, parent = db.get_note(note+".md")
    except DatabaseReadError as e:
        return "404"
    rendered = render_note(notef)
    return render_template("note.html", note=notef,
                                        root=parent,
                                        render=rendered)

@app.route('/view/<path:file>.<string:ext>')
def view_file(file, ext):
    if ext in ["jpeg", "jpg", "png", "svg", "txt"]:
        path, mime = db.get_media(file+"."+ext)
        return send_file(path, mimetype=mime)
    elif ext in ["md"]:
        return view_note(file)
    else:
        print("ERROR: invalid file extension requested: "+str(ext))
        return ""

@app.route('/<path:directory>')
def view_dir(directory):
    print("Listing directory %s" % directory)
    if directory == "favicon.ico":
        print("Catched favicon")
        return "404"
    files, dirs, parent = db.get_dir(directory)
    dirs.sort()
    files.sort()
    print("Listing with root %s" % directory)
    return render_template("dir.html", dirname=directory,
                                       files=files,
                                       folders=dirs,
                                       root=directory,
                                       parent=parent)
