from YAMLMacros.lib.syntax import meta, rule

from .data import load_data
from .properties import property_contexts
from .pseudo_classes import pseudo_classes_context, pseudo_elements_context

UNIT_TYPES = {
    'CSS Lengths': 'length',
    'CSS Flexible Lengths': 'flexible-lengths',
    'CSS Angles': 'angle',
    'CSS Times': 'time',
    'CSS Frequencies': 'frequency',
    'CSS Resolutions': 'resolution',
}

def quantity_rule(unit, subscope):
    return rule(
        match='{{number}}(%s){{identifier_end}}' % unit,
        scope='constant.numeric.%s.css' % subscope,
        captures={
            1: 'keyword.other.unit.%s.css' % subscope
        },
    )

def quantities_context(ignored):
    units = load_data('units')

    return [
        quantity_rule(
            unit,
            'quantity.%s.%s' % (
                UNIT_TYPES[next( cat for cat in info['groups'] if cat in UNIT_TYPES )],
                unit,
            )
        )
        for unit, info in units.items()
    ]

def units_context(ignored):
    data = load_data('units')

    return [
        rule(
            match=unit+r'{{identifier_end}}',
            scope='storage.type.unit.css',
            pop=True,
        )
        for unit in data
    ]
