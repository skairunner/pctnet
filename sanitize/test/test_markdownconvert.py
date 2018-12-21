from sanitize import htmlFromMarkdown


def test_inline_html_preserved():
    md = "*Markdown is <span class='bla'>cool</span>*"
    html = htmlFromMarkdown(md)
    assert "<span class='bla'>" in html


def test_two_newlines_is_p():
    md = "markdown\n\nhtml"
    html = htmlFromMarkdown(md)
    assert len(html.split('<p>')) == 3
