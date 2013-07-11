import locale
from functools import partial
from format_date import FormatDate

import sublime
import sublime_plugin


# I wrote this for InactivePanes, but why not just use it here as well?
class Settings(object):
    """Provides various helping functions for wrapping the sublime settings objects.

    `settings` should be provided as a dict of tuples and attribute names should not be one of the
    existing functions. And of course they should be valid attribute names.

    Example constructor:
    Settings(
        sublime.load_settings("Preferences.sublime-settings"),
        dict(
            attribute_name_to_save_as=('settings_key_to_read_from', 'default_value')
            #, ...
        ),
        on_settings_changed  # optional, callback
    )

    `settings_changed` will be called when the registered settings changed, and this time for real.
    Sublime Text currently behaves weird with `add_on_change` calls and the callback is run more
    often than it should be (as in, the specified setting didn't actually change), this wrapper
    however tests if one of the values has changed and then calls the callback.
    `update()` is called before the callback.

    Methods:
        * update()
            Reads all the settings and saves them in their respective attributes.
        * has_changed()
            Returns a boolean if the currently cached settings differ.
        * register(callback)
            Runs `add_on_change` for all settings defined with `callback` as the second parameter.
            You usually want to use `set_callback` instead.
        * unregister()
            See above, `clear_on_change`.
        * get_state()
            Returns a dict with the tracked settings as keys and their values (not the attribute
            names). With the above example: `{"settings_key_to_read_from": 'current_value'}`.
        * set_callback(callback)
            Calls `callback` whenever a tracked setting's value changes. See above on why this
            behavior differs to `register`.
        * clear_callback()
            Clears the callback set above and returns it in the process.
    """
    _sobj = None
    _settings = None
    _callback = None

    def __init__(self, settings_obj, settings, callback=None):
        self._sobj = settings_obj
        self._settings = settings

        self.update()
        self.set_callback(callback)

    def update(self):
        for attr, (name, def_value) in self._settings.items():
            setattr(self, attr, self._sobj.get(name, def_value))

    def _on_change(self):
        # Only trigger if relevant settings changed
        if self.has_changed():
            self.update()
            self._callback()

    def has_changed(self):
        for attr, (name, def_value) in self._settings.items():
            if getattr(self, attr) != self._sobj.get(name, def_value):
                return True

        return False

    def register(self, callback):
        for name, _ in self._settings.values():
            self._sobj.add_on_change(name, callback)

    def unregister(self):
        for name, _ in self._settings.values():
            self._sobj.clear_on_change(name)

    def get_state(self):
        return dict((name, self._sobj.get(name, def_value))
                    for name, def_value in self._settings.values())

    def set_callback(self, callback):
        if callable(callback):
            if not self._callback:
                # Order actually matters
                self._callback = callback
                self.register(self._on_change)
            else:
                self._callback = callback

    def clear_callback(self):
        cb = self._callback
        if cb:
            self.unregister(self._on_change)
            self._callback = None
        return cb

# Instantiate global variables
fdate = FormatDate()

s = Settings(
    sublime.load_settings('insert_date.sublime-settings'),
    settings=dict(
        format=('format', '%x %X'),
        tz_in=('tz_in', 'local')
    )
)


# Register on settings changes
def on_settings_changed():
    # These defaults will be used when the command's parameters are None
    fdate.set_default(s.get_state())
    print "updated"

on_settings_changed()  # Apply initial settings
s.set_callback(on_settings_changed)

print s.get_state()


# The actual command
class InsertDateCommand(sublime_plugin.TextCommand):
    """Prints Date according to given format string"""

    def run(self, edit, format=None, prompt=False, tz_in=None, tz_out=None):
        if prompt:
            self.view.window().show_input_panel(
                # Caption
                "Date format string:",
                # Default text
                str(format) if format else '',
                # on_done callback (call this function again)
                partial(self.run, edit, tz_in=tz_in, tz_out=tz_out),
                # Unnecessary callbacks
                None, None
            )
            return  # Call already handled

        if format == '' or (isinstance(format, basestring) and format.isspace()):
            # Emtpy string or only whitespaces entered in input panel
            return

        # Do the actual parse action
        print format, tz_in, tz_out
        try:
            text = fdate.parse(format, tz_in, tz_out)
        except Exception as e:
            sublime.error_message("[InsertDate]\n%s: %s" % (type(e).__name__, e))
            return

        # Don't bother replacing selections with actually nothing
        if text == '' or text.isspace():
            return

        # Fix potential unicode/codepage issues
        if type(text) == str:
            # print(text)
            try:
                text = text.decode(locale.getpreferredencoding())
            except UnicodeDecodeError:
                text = text.decode('utf-8')

        # Do replacements
        for r in self.view.sel():
            # Insert when sel is empty to not select the contents
            if r.empty():
                self.view.insert (edit, r.a, text)
            else:
                self.view.replace(edit, r,   text)
