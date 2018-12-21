from .markdownconvert import htmlFromMarkdown
from .htmlsanitizer import sanitizeHTML


def sanitizeInput(fragment):
    return sanitizeHTML(htmlFromMarkdown(fragment))
