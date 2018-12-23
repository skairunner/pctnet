# Derived from https://www.owasp.org/index.php/XSS_Filter_Evasion_Cheat_Sheet
from sanitize import sanitizeInput


def test_basic_xss():
    raw = "<SCRIPT SRC=http://xss.rocks/xss.js></SCRIPT>"
    html = sanitizeInput(raw)
    assert '<script' not in html.lower()


def test_image_xss():
    raw = '''<IMG SRC="javascript:alert('XSS');">'''
    html = sanitizeInput(raw)
    assert 'javascript' not in html


def test_image_no_quotes():
    raw = '''<IMG SRC=javascript:alert('xss')>'''
    html = sanitizeInput(raw)
    assert '&lt;' in html


def test_image_function_literals():
    raw = '''<IMG SRC=`javascript:alert("RSnake says, 'XSS'")`>'''
    html = sanitizeInput(raw)
    assert '&lt;IMG' in html


def test_a_tag_malformed():
    raw = '''<a onmouseover="alert(document.cookie)">xxs link</a>'''
    html = sanitizeInput(raw)
    assert 'onmouseover' not in html


def test_malformed_img_tag():
    raw = '''<IMG """><SCRIPT>alert("XSS")</SCRIPT>">'''
    html = sanitizeInput(raw)
    assert '<script' not in html.lower()


def test_embedded_tab():
    raw = '''<IMG SRC="jav	ascript:alert('XSS');">'''
    html = sanitizeInput(raw)
    assert 'src' not in html.lower()


def test_input_type_image():
    raw = '''<INPUT TYPE="IMAGE" SRC="javascript:alert('XSS');">'''
    html = sanitizeInput(raw)
    assert '<input' not in html.lower()


def test_block_multiline_xss():
    raw = '''hello <a name="n"
href="javascript:alert('xss')">*you*</a>'''
    html = sanitizeInput(raw)
    assert 'javascript' not in html
