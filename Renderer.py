""" This class represents a note renderer.
    It simply turns a Note object into html
"""

from Note import Note
import mistune



class NoteMarkdownRenderer(mistune.Renderer):
    def paragraph(self, text):
        print(text)
        return "Lel"


class NoteRenderer:
    
    def __init__(self):
        self.renderer = NoteMarkdownRenderer()
        self.markdown = mistune.Markdown(renderer=self.renderer)
 
    def render(self, note):
        note_content = "# "+note.title+"\n"
        for tag in note.tags:
            note_content += "\#" + tag + " "
        note_content += "\n"
        note_content += note.content

        return self.markdown(note_content)


    
