from mistletoe.block_token import Document
from mistletoe.html_renderer import HTMLRenderer
import html


class SanitizedHTMLRenderer(HTMLRenderer):
    @staticmethod
    def render_html_block(token):
        return f'<p>{html.escape(token.content)}</p>'

    @staticmethod
    def render_html_span(token):
        return html.escape(token.content)


def markdown(iterable, renderer=SanitizedHTMLRenderer):
    with renderer() as renderer:
        return renderer.render(Document(iterable))


# This version escapes html.
def sanitizeMarkdown(fragment):
    return markdown(fragment)
