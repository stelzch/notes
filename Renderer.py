""" This class represents a note renderer.
    It simply turns a Note object into html
"""

from Note import Note
import mistune



class NoteMarkdownRenderer(mistune.Renderer):
    pass

class NoteRenderer:
    
    def __init__(self):
        self.renderer = NoteMarkdownRenderer()
        self.markdown = mistune.Markdown(renderer=self.renderer)
 
    def render(self, note):
        note_content = note.content

        return self.markdown(note_content)

r = NoteRenderer()

def render_note(note):
    return r.render(note)
