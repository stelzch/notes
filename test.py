from Note import Note
from Renderer import NoteRenderer
from mistune import Markdown

renderer = NoteRenderer()

note1 = Note.load("example1.md")
print(note1)
print(renderer.render(note1))
