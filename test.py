from Note import Note
from Renderer import NoteRenderer

note1 = Note.load("example1.md")
print(NoteRenderer.render(note1))
