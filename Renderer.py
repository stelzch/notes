""" This class represents a note renderer.
    It simply turns a Note object into html
"""

from Note import Note
import mistune
""" The Pygment Highlighter """
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name


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
                content += line + "\n"
            caption = mistune.markdown(caption)
            content = mistune.markdown(content)
            print(content)
            return '\n<div class="box">\n<div class="caption">%s</div>\n<div class="content">%s</div>\n</div>' % (caption, content)
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter(noclasses=True, style='monokai')
        result = highlight(code, lexer, formatter)
        return result

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
