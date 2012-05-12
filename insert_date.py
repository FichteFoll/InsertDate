import sublime_plugin
from datetime import datetime
from functools import partial


class InsertDateCommand(sublime_plugin.TextCommand):
    """Prints Date"""
    default_format = "%Y-%m-%d %H:%M"

    def run(self, edit, format=None, prompt=False):
        if prompt:
            # pass this function as callback
            self.view.window().show_input_panel("Input date:", format, partial(self.run, edit), None, None)
            return
        elif format is None:
            format = self.default_format

        if not format:
            # emtpy string entered in input panel
            return

        now = datetime.now()
        if format.startswith("iso"):
            sep = 'T'
            if len(format) == 5 and format[3] == ':':
                sep = str(format[4])  # convert from unicode
            text = now.isoformat(sep)
        else:
            text = now.strftime(format)

        for r in self.view.sel():
            if r.empty():
                self.view.insert (edit, r.begin(), text)
            else:
                self.view.replace(edit, r, text)
