#!/usr/bin/env python3

"""This is just the code I use to generate the example table rows for the readme."""

from __init__ import FormatDate

formats = [
    { 'format': "%d/%m/%Y %I:%M %p"},
    { 'format': "%d. %b %y"},
    { 'format': "%H:%M:%S.%f%z"},
    { 'format': "%Y-%m-%dT%H:%M:%S.%f%z"},
    { 'format': "iso",
      'tz_out': "UTC"},
    { 'format': "%c UTC%z",
      'tz_in':  "local"},
    { 'format': "%X %Z",
      'tz_in':  "Europe/Berlin"},
    { 'format': "%d/%m/%Y %I:%M %Z",
      'tz_in':  "America/St_Johns"},
    { 'format': "%c %Z (UTC%z)",
      'tz_out': "EST"},
    { 'format': "%x %X %Z (UTC%z)",
      'tz_out': "America/New_York"},
    { 'format': "unix"}
]
fdate = FormatDate()
formatted = []
for fmt in formats:
    formatted.append(fdate.parse(**fmt))

ftext = []
for s, fmt in zip(formatted, formats):
    params = fmt.copy()
    del params['format']
    params = "`%s`" % params if params else ''
    ftext.append("|`%s`|%s|%s|" % (fmt['format'], params, s))

text = '\n'.join(ftext)


if __name__ != '__main__':
    import sublime_plugin

    class TableGenCommand(sublime_plugin.TextCommand):
        def run(self, edit):
            self.view.insert(edit, self.view.sel()[0].begin(), text)
else:
    # Put on clipboard
    from tkinter import Tk
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(text)
    r.destroy()
