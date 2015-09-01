import pytz

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


def show_timezone_quickpanel(callback, selected_item):
    global s
    show_quick_panel = sublime.active_window().show_quick_panel
    if ST2:
        show_quick_panel(pytz.all_timezones, callback)
    else:
        try:
            selected_index = pytz.all_timezones.index(selected_item)
        except ValueError:
            selected_index = 0
        show_quick_panel(pytz.all_timezones, callback,
                         selected_index=selected_index)

# I wrote this for InactivePanes, but why not just use it here as well?
# TODO write methods to change settings and flush changes.
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


################################################################################
# The actual commands

# TODO `locale` setting to modify `%c %x %X %p` representation?
# TODO `shift` param
class InsertDateCommand(sublime_plugin.TextCommand):

    """Prints Date according to given format string."""

    def run(self, edit, format=None, tz_in=None, tz_out=None):
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
            status("Error parsing format string `%s`" % format, e)
            return

        # Don't bother replacing selections with actually nothing
        if not text or text.isspace():
            return

        # Do replacements
        for r in self.view.sel():
            # Insert when sel is empty to not select the contents
            if r.empty():
                self.view.insert(edit, r.a, text)
            else:
                self.view.replace(edit, r, text)


class InsertDatePromptCommand(sublime_plugin.TextCommand):

    """Ask for a format string, while preserving the other parameters.

    If "format" is provided, it will be pre-inserted into the prompt.
    """

    def run(self, edit, format=None, tz_in=None, tz_out=None):
        self.tz_in = tz_in
        self.tz_out = tz_out

        # Unset save_on_focus_lost so that ST doesn't save and remove trailing
        # whitespace when the input/quick panel is opened, if that option is
        # also enabled. (#26)
        self.view.settings().set('save_on_focus_lost', False)

        # Ask for the format string
        i_panel = self.view.window().show_input_panel(
            # caption
            "Date format string:",
            # initial_text
            format or fdate.default['format'],
            # on_done
            self.on_format,
            # on_change (unused)
            None,
            # on_cancel
            lambda: self.view.settings().erase('save_on_focus_lost')
        )

        # Select the default text
        i_panel.sel().clear()
        i_panel.sel().add(sublime.Region(0, i_panel.size()))

    def on_format(self, fmt):
        global s
        if fmt:
            self.format = fmt
        if self.tz_out:
            self.run_for_real()
        else:
            # Ask for an output timezone
            sublime.status_message("[InsertDate] "
                                   "Please select a timezone for the output "
                                   "(press 'esc' to use same as input)")
            show_timezone_quickpanel(self.on_tz_out, self.tz_in or s.tz_in)

    def on_tz_out(self, index):
        if index != -1:
            self.tz_out = pytz.all_timezones[index]
        self.run_for_real()

    def run_for_real(self):
        self.view.settings().erase('save_on_focus_lost')
        self.view.run_command(
            'insert_date',
            {'format': self.format, 'tz_in': self.tz_in, 'tz_out': self.tz_out}
        )


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

        if not configs:
            status("No configurations found to choose from")
            return

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

        # Unset save_on_focus_lost so that ST doesn't save and remove trailing
        # whitespace when the quick panel is opened, if that option is also
        # enabled. (#26)
        self.view.settings().set('save_on_focus_lost', False)
        self.view.window().show_quick_panel(self.panel_cache, self.on_done)

    def on_done(self, index):
        # Erase our settings override
        self.view.settings().erase('save_on_focus_lost')
        if index == -1:
            return

        name = self.panel_cache[index][0]
        self.view.run_command('insert_date', self.config_map[name])


class InsertDateSelectTimezone(sublime_plugin.ApplicationCommand):

    @staticmethod
    def on_select(index):
        global s
        if index == -1:
            return
        timezone = pytz.all_timezones[index]
        s._sobj.set('tz_in', timezone)
        s._sobj.erase('silence_timezone_request')
        sublime.save_settings('insert_date.sublime-settings')

    def run(self):
        global s
        show_timezone_quickpanel(self.on_select, s.tz_in)

################################################################################


def plugin_loaded():
    global s

    s = Settings(
        sublime.load_settings('insert_date.sublime-settings'),
        settings=dict(
            format=('format', '%c'),
            tz_in=('tz_in', 'local'),
            prompt_config=('prompt_config', []),
            user_prompt_config=('user_prompt_config', []),
            silence_timezone_request=None
        )
    )

    # Register on settings changes
    def on_settings_changed(initial=False):
        global fdate

        if not initial:
            status("settings changed")
        # These defaults will be used when the command's parameters are None
        fdate.set_default(s.get_state())

    on_settings_changed(True)  # Apply initial settings
    s.set_callback(on_settings_changed)

    if s.tz_in == 'local' and not s.silence_timezone_request:
        # Request user to set a timezone - later
        def request_timezone():
            if sublime.ok_cancel_dialog(
                "You should set your timezone in InsertDate's settings "
                "in order to properly use that package.\n"
                "Do you wish to do that now?"
                "\n\n"
                "Note: You can open the timezone prompt any time "
                'using the "InsertDate: Select Timezone" command.',
                "Yes"
            ):
                sublime.run_command('insert_date_select_timezone')
            else:
                s._sobj.set('silence_timezone_request', True)
                sublime.save_settings('insert_date.sublime-settings')

        sublime.set_timeout(request_timezone, 3000)


def plugin_unloaded():
    global s

    if s:
        s.clear_callback(True)

# ST2 backwards (and don't call it twice in ST3)
unload_handler = plugin_unloaded if ST2 else lambda: None

# Call manually if on ST2
if ST2:
    plugin_loaded()
