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

PROPERTY_TEMPLATE = HtmlTemplate("""
<div>
    <a href="{name}">{name}</a>: <i>{syntax}</i>
</div>
""")

class CssCompletionsListener(sublime_plugin.ViewEventListener):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.properties = load_data('properties')

    def on_query_completions(self, prefix, locations):
        point = locations

    def on_hover(self, point, hover_zone):
        if hover_zone != sublime.HOVER_TEXT: return
        if not self.view.match_selector(point, 'source.css'): return

        region = self.enclosing_scope(point, 'support.type.property-name.css')
        if not region: return
        text = self.view.substr(region)

        if text in self.properties:
            prop = self.properties[text]
            self.view.show_popup(
                content=PROPERTY_TEMPLATE.render(
                    name=text,
                    syntax=prop['syntax'],
                ),
                location=point,
                flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY,
                on_navigate=self.lookup,
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

    def lookup(self, prop):
        url = 'https://developer.mozilla.org/en-US/docs/Web/CSS/%s' % prop
        webbrowser.open_new_tab(url)
