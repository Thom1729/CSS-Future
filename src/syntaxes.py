from .data import load_data

import re

def parse_syntax(syntax):
    tokens = [
        re.sub(r'{.*}$', '', token.rstrip('*+?#!'))
        for token in syntax.split()
    ]

    for token in tokens:
        if token in { '&&', '||', '|', '[', ']' }:
            continue

        yield token

syntaxes = {}

syntaxes.update(**{
    name : list(parse_syntax(value['syntax']))
    for name, value in load_data('syntaxes').items()
})
