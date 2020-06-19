tmp_prefix = 'tmp::'


def make_quote(text: str):
    return '\n'.join([f'>{line}' for line in text.splitlines()])
