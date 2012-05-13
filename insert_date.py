import sublime
import sublime_plugin
from functools import partial
from format_date import FormatDate


class InsertDateCommand(sublime_plugin.TextCommand, FormatDate):
    """Prints Date according to given format string"""

    def run(self, edit, format=None, prompt=False, tz_in=None, tz_out=None):
        if prompt:
            self.view.window().show_input_panel(
                "Date format string:",
                str(format) if format else '',
                # pass this function as callback
                partial(self.run, edit, tz_in=tz_in, tz_out=tz_out),
                None, None
            )
            return  # call already handled

        if format == '' or (isinstance(format, basestring) and format.isspace()):
            # emtpy string or whitespaces entered in input panel
            return

        # do the actual parse action
        try:
            text = self.parse(format, tz_in, tz_out)
        except Exception as e:
            sublime.error_message("[InsertDate]\n%s: %s" % (type(e).__name__, e))
            return

        if text == '' or text.isspace():
            # don't bother replacing selections with actually nothing
            return

        if type(text) == str:
            # print(text)
            text = text.decode('utf-8')

        for r in self.view.sel():
            if r.empty():
                self.view.insert (edit, r.a, text)
            else:
                self.view.replace(edit, r,   text)
