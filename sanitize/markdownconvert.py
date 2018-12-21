from markdown import markdown


def htmlFromMarkdown(fragment):
    return markdown(fragment, output_format='html5')
