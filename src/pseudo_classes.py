from yamlmacros.lib.syntax import rule

import re

from .data import load_data

def pseudo_classes_context(ignored):
    data = load_data('selectors')

    def pseudo_class_rule(selector):
        name = selector.lstrip(':')
        return rule(
            match=name+r'{{identifier_end}}',
            scope='support.function.pseudo-class.css',
            pop=True,
        )

    return [
        pseudo_class_rule(selector)
        for selector in data
        if selector.startswith(':') and not selector.startswith('::')
    ]
