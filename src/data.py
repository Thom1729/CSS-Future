import sublime
import json

def load_data(name):
    resource_path = 'Packages/CSSFuture/data/%s.json' % name
    try:
        text = sublime.load_resource(resource_path)
        return json.loads(text)
    except IOError as err:
        raise IOError('Data file "%s" not found. (%s)' % (name, resource_path)) from err
