from sanitize import sanitizeHTML


def test_remove_script_tags():
    dirty = '''
    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    <script src='whatever.org/thing.js'></script>
    '''
    clean = sanitizeHTML(dirty)
    assert '<script' not in clean


def test_fix_badly_nested_tags():
    dirty = '<em><strong>aaaaa</em></strong>'
    clean = sanitizeHTML(dirty)
    assert clean == '<em><strong>aaaaa</strong></em>'


def test_fix_unclosed_tags():
    dirty = '<p>Bla bla bla'
    clean = sanitizeHTML(dirty)
    assert clean == '<p>Bla bla bla</p>'


def test_multiple_unclosed_tags():
    dirty = '<p>Blablabla <em>emphasis <b>bla</p>'
    clean = sanitizeHTML(dirty)
    assert clean == '<p>Blablabla <em>emphasis <b>bla</b></em></p>'


def test_strip_style_attr_contents():
    dirty = '<p style="color: black">Lorem ipsum</p>'
    clean = sanitizeHTML(dirty)
    assert clean == '<p>Lorem ipsum</p>'
