from sanitize import sanitizeInput


def test_simple_mixed_input():
    raw = '''# Chapter One
Lorem *ipsum*.

P<span>2</span>'''
    html = sanitizeInput(raw).strip()
    assert html == '''<h1>Chapter One</h1>\n<p>Lorem <em>ipsum</em>.</p>\n<p>P<span>2</span></p>'''


def test_mixed_within_markdown():
    raw = "*Emphasis <b>bold</b>*"
    html = sanitizeInput(raw).strip()
    assert html == '''<p><em>Emphasis <b>bold</b></em></p>'''


def test_markdown_inside_span():
    raw = "<span>I *want* this to work</span>"
    html = sanitizeInput(raw).strip()
    assert html == "<p><span>I <em>want</em> this to work</span></p>"


def test_markdown_inside_p():
    raw = '<p>*test*</p>'
    html = sanitizeInput(raw).strip()
    assert html == '<p>*test*</p>'
    raw = '<p>\n\n*test*\n\n</p>'
    html = sanitizeInput(raw)
    assert 'em' in html


def test_markdown_inside_div():
    raw = "<div>Howmst *this* work</div>"
    html = sanitizeInput(raw).strip()
    # one line block is not converted
    assert html == "<div>Howmst *this* work</div>"
    # must wrap markdown with 2 newlines for convert
    raw = "<div>\n\nHowmst *this* work\n\n</div>"
    html = sanitizeInput(raw).strip()
    assert 'em' in html


def test_dont_strip_classes():
    raw = "<span class='classy'>test</span>"
    html = sanitizeInput(raw).strip()
    # Sanitizer turns single quotes for attrs into double
    assert html == '<p><span class="classy">test</span></p>'


def test_strip_style():
    raw = "<span style='color: black;'>test</span>"
    html = sanitizeInput(raw)
    assert 'color' not in html


def test_dont_strip_src_attr():
    raw = "<img src='whatever'></img>"
    html = sanitizeInput(raw)
    assert 'src="whatever"' in html

