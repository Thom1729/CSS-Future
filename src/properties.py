from yamlmacros.lib.syntax import rule

import re

from .data import load_data

def property_contexts(ignore):
    data = load_data('properties')

    def property_rule(prop):
        value_scope = 'property-value'

        keywords = re.findall(r"(?<!['<])\b[A-Za-z](?:[A-Za-z0-9-]*[A-Za-z]+)*\b(?!['>])", data[prop]['syntax'])
        if keywords:
            expr = r'(?:%s){{identifier_end}}' % r'|'.join(keywords)
            value_scope = [
                rule(
                    match=expr,
                    scope='support.constant.property-value.css',
                ),
                rule(include='property-value'),
            ]

        return rule(
            match=prop+r'{{identifier_end}}',
            scope='meta.property-name.css support.type.property-name.css',
            push=[ [rule(include='immediately-pop')], 'property-meta', value_scope, 'property-colon' ]
        )

    return list(map(property_rule, data))
