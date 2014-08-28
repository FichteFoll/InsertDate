import sublime
import sublime_plugin

try:
    from .format_date import FormatDate, UnknownTimeZoneError  # ST3
except ValueError:
    from format_date import FormatDate, UnknownTimeZoneError  # ST2


ST2 = int(sublime.version()) < 3000

if not ST2:
    basestring = str

# Global variables
fdate = FormatDate()
# Global settings object
s = None
# Print tracebacks
DEBUG = False


def status(msg, e=None):
    msg = "[InsertDate] " + msg
    sublime.status_message(msg)
    if e is not None:
        msg += "\n%s: %s" % (type(e).__name__, e)
    print(msg)

    if e and DEBUG:
        import traceback
        traceback.print_exc()


# I wrote this for InactivePanes, but why not just use it here as well?
class Settings(object):
    """Provides various helping functions for wrapping the sublime settings objects.

    `settings` should be provided as a dict of tuples and attribute names should not be one of the
    existing functions. And of course they should be valid attribute names.

    Example constructor:
    Settings(
        sublime.load_settings("Preferences.sublime-settings"),
        dict(
            attr_name_to_save_as=('settings_key_to_read_from', 'default_value'),
            attr_name_to_save_as2='settings_key_to_read_from_with_default_None',
            attr_name_and_settings_key_with_default_None=None
            #, ...
        ),
        on_settings_changed,  # optional, callback
        auto_update  # optional, bool
                     # (whether the attributes should be kept up to date; default: True)
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
        * get_state()
            Returns a dict with the tracked settings as keys and their values (NOT the attribute
            names). With the above example: `{"settings_key_to_read_from": 'current_value'}`.
        * get_real_state()
            Same as above but ALWAYS returns the actual current values in the settings object.
        * set_callback(callback, auto_update=True)
            Calls `callback` whenever a tracked setting's value changes. See above on why this
            behavior differs to `register`.
            If `auto_update` is true it will automatically update the attributes when the settings
            changes. This is always true when a callback is set.
        * clear_callback(clear_auto_update=False)
            Clears the callback set above and returns it in the process.
    """
    _sobj = None
    _settings = None
    _callback = None
    _auto_update = False

    def __init__(self, settings_obj, settings, callback=None, auto_update=True):
        self._sobj = settings_obj

        for k, v in settings.items():
            if v is None:
                # Use the attr name as settings key and `None` as default
                settings[k] = (k, None)
            if isinstance(v, basestring):
                # Set default to `None` if a string was supplied
                settings[k] = (v, None)
        self._settings = settings

        self.update()
        self.set_callback(callback, auto_update)

    def update(self):
        for attr, (name, def_value) in self._settings.items():
            setattr(self, attr, self._sobj.get(name, def_value))

    def _on_change(self):
        # Only trigger if relevant settings changed
        if self.has_changed():
            self.update()
            if self._callback:
                self._callback()

    def _register(self, callback):
        for name, _ in self._settings.values():
            self._sobj.add_on_change(name, callback)

    def _unregister(self):
        for name, _ in self._settings.values():
            self._sobj.clear_on_change(name)

    def has_changed(self):
        return self.get_state() != self.get_real_state()

    def get_state(self):
        return dict((name, getattr(self, attr))
                    for attr, (name, _) in self._settings.items())

    def get_real_state(self):
        return dict((name, self._sobj.get(name, def_value))
                    for name, def_value in self._settings.values())

    def set_callback(self, callback, auto_update=True):
        if callback is not None and not callable(callback):
            raise TypeError("callback must be callable")

        cb = self._callback
        self._callback = callback
        if (not cb and not self._auto_update) and (callback or auto_update):
            self._register(self._on_change)

        self._auto_update = auto_update
        return cb

    def clear_callback(self, clear_auto_update=False):
        cb = self._callback
        if cb or not self._auto_update or clear_auto_update:
            self._unregister()
        self._callback = None
        return cb


# The actual commands
class InsertDateCommand(sublime_plugin.TextCommand):

    """Prints Date according to given format string."""

    def run(self, edit, format=None, prompt=False, tz_in=None, tz_out=None):
        if prompt:
            self.view.window().show_input_panel(
                # Caption
                "Date format string:",
                # Default text
                str(format) if format else '',
                # on_done callback (call this command again)
                lambda f: self.view.run_command("insert_date",
                                                {"format": f, "tz_in": tz_in, "tz_out": tz_out}),
                # Unnecessary callbacks
                None, None
            )
            return  # Call already handled

        if format is not None:
            if format == '' or not isinstance(format, basestring) or format.isspace():
                # Not a string, empty or only whitespaces
                return

        # Do the actual parse action
        try:
            text = fdate.parse(format, tz_in, tz_out)
        except UnknownTimeZoneError as e:
            status(str(e).strip('"'), e)
            return
        except Exception as e:
            status('Error parsing format string `%s`' % format, e)
            return

        # Don't bother replacing selections with actually nothing
        if text == '' or text.isspace():
            return

        # Do replacements
        for r in self.view.sel():
            # Insert when sel is empty to not select the contents
            if r.empty():
                self.view.insert (edit, r.a, text)
            else:
                self.view.replace(edit, r,   text)


class InsertDatePanelCommand(sublime_plugin.TextCommand):

    """Shows a quick panel with configurable templates that are previewed."""

    panel_cache = []
    config_map = {}

    def run(self, edit, tz_in=None, tz_out=None):
        self.panel_cache = []
        self.config_map = {}

        if not isinstance(s.prompt_config, list):
            status("`prompt_config` setting is invalid")
            return

        configs = s.prompt_config
        if not isinstance(s.user_prompt_config, list):
            status("`user_prompt_config` setting is invalid")
        else:
            configs = configs + s.user_prompt_config

        # Generate panel cache for quick_panel
        for conf in configs:
            # Read config
            c = dict()
            c['tz_in']  = tz_in if tz_in else conf.get('tz_in')
            c['tz_out'] = tz_out if tz_out else conf.get('tz_out')
            c['format'] = conf.get('format')

            if isinstance(c['format'], basestring):
                c['format'] = c['format'].replace("$default", fdate.default['format'])

            # Do the actual parse action
            try:
                text = fdate.parse(**c)
            except UnknownTimeZoneError as e:
                status(str(e).strip('"'), e)
                return
            except Exception as e:
                status('Error parsing format string `%s`' % format, e)
                return

            self.panel_cache.append([conf['name'], text])
            self.config_map[conf['name']] = c

        self.view.window().show_quick_panel(self.panel_cache, self.on_done)

    def on_done(self, index):
        if index == -1:
            return

        name = self.panel_cache[index][0]
        self.view.run_command("insert_date", self.config_map[name])


# Handle context
def plugin_loaded():
    global s, fdate

    s = Settings(
        sublime.load_settings('insert_date.sublime-settings'),
        settings=dict(
            format=('format', '%c'),
            tz_in=('tz_in', 'local'),
            prompt_config=None,
            user_prompt_config=None
        )
    )

    # Register on settings changes
    def on_settings_changed():
        print("InsertDate settings changed")
        # These defaults will be used when the command's parameters are None
        fdate.set_default(s.get_state())

    on_settings_changed()  # Apply initial settings
    s.set_callback(on_settings_changed)


def plugin_unloaded():
    global s

    s.clear_callback(True)

    # Close the potentially opened zip file
    # Sadly, this doesn't help because ST itself still keeps an open handle to the file
    # even when disabling.
    from format_date import pytz
    if pytz.zf:
        pytz.zf.close()

# ST2 backwards (and don't call it twice in ST3)
unload_handler = plugin_unloaded if ST2 else lambda: None

# Call manually if on ST2
if ST2:
    plugin_loaded()
