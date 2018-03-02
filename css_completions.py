import sublime
import sublime_plugin

import webbrowser
# from html import escape
import re

from .src.data import load_data

MINIHTML_ESCAPES = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
}
def escape(string):
    return re.sub(r'[&<>]', lambda m: MINIHTML_ESCAPES[m.group(0)], string)

class HtmlTemplate():
    def __init__(self, template):
        self.template = template

    def render(self, **kwargs):
        return self.template.format(**{
            k: escape(v)
            for k, v in kwargs.items()
        })

TEMPLATE = HtmlTemplate("""
<div>
    <a href="{url}">{name}</a>: <pre>{syntax}</pre>
</div>
""")

TOOLTIP_TYPES = [
    {
        'selector': 'support.type.property-name.css',
        'url': 'https://developer.mozilla.org/en-US/docs/Web/CSS/%s',
        'data': load_data('properties'),
    },
    {
        'selector': 'meta.selector.pseudo-class.css',
        'url': 'https://developer.mozilla.org/en-US/docs/Web/CSS/%s',
        'data': load_data('selectors'),
    },
    {
        'selector': 'meta.selector.pseudo-element.css',
        'url': 'https://developer.mozilla.org/en-US/docs/Web/CSS/%s',
        'data': load_data('selectors'),
    },
]

class CssCompletionsListener(sublime_plugin.ViewEventListener):

    def on_hover(self, point, hover_zone):
        if hover_zone != sublime.HOVER_TEXT: return
        if not self.view.match_selector(point, 'source.css'): return

        type = next((
            t for t in TOOLTIP_TYPES
            if self.view.match_selector(point, t['selector'])
        ), None)

        if not type: return

        region = self.enclosing_scope(point, type['selector'])
        name = self.view.substr(region)
        if name in type['data']:
            content = TEMPLATE.render(
                name=name,
                url=type['url'] % name,
                syntax=type['data'][name].get('syntax', None),
            )

            self.view.show_popup(
                content=content,
                location=point,
                flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY,
                on_navigate=webbrowser.open_new_tab,
                max_width=1000
            )

    def enclosing_scope(self, point, selector):
        if not self.view.match_selector(point, selector): return None

        l = point
        while (l > 0 and self.view.match_selector(l-1, selector)):
            l -= 1

        r = point
        while (self.view.match_selector(r, selector)):
            r += 1

        return sublime.Region(l, r)
