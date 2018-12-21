from sanitize import sanitizeInput


def test_simple_mixed_input():
    raw = '''# Chapter One
Lorem *ipsum*.

P<span>2</span>'''
    html = sanitizeInput(raw)
    assert html == '''<h1>Chapter One</h1>\n<p>Lorem <em>ipsum</em>.</p>\n<p>P<span>2</span></p>'''


def test_mixed_within_markdown():
    raw = "*Emphasis <b>bold</b>*"
    html = sanitizeInput(raw)
    assert html == '''<p><em>Emphasis <b>bold</b></em></p>'''


def test_dont_strip_classes():
    raw = "<span class='classy'>test</span>"
    html = sanitizeInput(raw)
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
