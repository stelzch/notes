""" This class represents a note renderer.
    It simply turns a Note object into html
"""

from Note import Note
from mistune import markdown

class NoteRenderer:
    
    @staticmethod
    def render(note):
        note_content = "# "+note.title+"\n"
        for tag in note.tags:
            note_content += "\#" + tag + " "
        note_content += "\n"

        note_content += note.content
        
        return markdown(note_content)
