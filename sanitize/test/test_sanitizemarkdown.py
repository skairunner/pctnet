from sanitize import sanitizeMarkdown


def test_escapes_div_gtlt():
    md = '<div>bla</div>'
    output = '<p>&lt;div&gt;bla&lt;/div&gt;</p>'
    html = sanitizeMarkdown(md).strip()
    assert html == output


def test_preserves_inner_markdown():
    md = '<div>\n\n*thonk*\n\n</div>'
    html = sanitizeMarkdown(md).strip()
    assert 'em' in html
    assert '<div' not in html


# comments on mistletoe repo suggested this may be a problem
def test_escapes_svg():
    md = '<svg>hello</svg>'
    html = sanitizeMarkdown(md).strip()
    assert '&lt;svg' in html


def test_blockquotes_not_escaped():
    md = '''
    > Blockquote
    > End blockquote'''
    md = md.replace('    ', '')
    html = sanitizeMarkdown(md).strip()
    assert 'blockquote' in html
