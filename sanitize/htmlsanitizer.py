import bleach

HTML_ALLOWED_TAGS = [
    'a', 'abbr', 'acronym', 'address', 'b', 'big', 'blockquote', 'br',
    'caption', 'center', 'cite', 'code', 'col', 'colgroup', 'dd', 'del',
    'dfn', 'div', 'dl', 'dt', 'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'hr', 'i', 'img', 'ins', 'kbd', 'li', 'ol', 'p', 'pre', 'q', 's',
    'samp', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'table',
    'tbody', 'td', 'tfoot', 'th', 'thread', 'tr', 'tt', 'u', 'ul', 'var',
]

HTML_ALLOWED_ATTRIBUTES = [
    'align', 'alt', 'axis', 'class', 'height', 'href', 'name', 'src',
    'title', 'width',
]


def attrallowed(tag, name, value):
    allowedtag = tag in HTML_ALLOWED_TAGS
    allowedattr = name in HTML_ALLOWED_ATTRIBUTES
    return allowedtag and allowedattr


def sanitizeHTML(fragment):
    return bleach.clean(fragment, HTML_ALLOWED_TAGS, attrallowed)
