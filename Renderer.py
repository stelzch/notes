""" This class represents a note renderer.
    It simply turns a Note object into html
"""

from Note import Note
import mistune
""" The Pygment Highlighter """
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

class NoteMarkdownRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        if not lang:
            print("No language for "+code)
            return '\n<pre><code>%s</code></pre>\n' % mistune.escape(code)
        if lang == "_box":
            lines = code.split("\n")
            caption = lines[0]
            content_ = lines[1:]
            content = ""
            for line in content_:
                content += (line + "<br>")
            return '\n<div class="box">\n<div class="caption">%s</div>\n%s\n</div>' % (caption, content)
        print("Highlighting %s: %s" % (lang, code))
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter(full=True)
        result = highlight(code, lexer, formatter)
        print(result)
        return highlight(code, lexer, formatter)

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
