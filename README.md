# InsertDate - Sublime Text Plugin

A plugin for [Sublime Text][st] 2 and 3 that inserts the current date and/or
time according to the format specified and supports named timezones.

For a brief introduction about the accepted formatting syntax, see
<http://strfti.me/>.


## Install

You can install this package with [Package Control][pck-ctrl] under
[*InsertDate*][pck-browse].


## Usage

### Screenshot

The panel opens on <kbd>F5</kbd> and shows a selection of pre-defined settings
that can be modified. See [Settings](#settings) on how to do that.

[![][scr-panel-thumb]][scr-panel]


### Command Examples

The following is an excerpt of the [default key bindings][keymap] (on
[OSX][keymap-osx]: `super` instead of `ctrl`):

```js
[
// Insert datetime using default format text
  { "keys": ["ctrl+f5", "ctrl+f5"],
    "command": "insert_date" },

// Insert datetime using the specified format
  // Locale date
  { "keys": ["ctrl+f5", "ctrl+d"],
    "command": "insert_date",
    "args": {"format": "%x"} },

  // Locale time
  { "keys": ["ctrl+f5", "ctrl+t"],
    "command": "insert_date",
    "args": {"format": "%X"} },

  // Full iso date and time
  { "keys": ["ctrl+f5", "ctrl+i"],
    "command": "insert_date",
    "args": {"format": "iso"} },

  // Locale date and time converted to UTC (with timezone name)
  { "keys": ["ctrl+f5", "ctrl+u"],
    "command": "insert_date",
    "args": {"format": "%c %Z", "tz_out": "UTC"} },

  // Unix time (seconds since the epoch, in UTC)
  { "keys": ["ctrl+f5", "ctrl+x"],
    "command": "insert_date",
    "args": {"format": "unix"} },

  // ... and many more

// Prompt for user input ("format" arg would behave as default text)
// and insert the datetime using that format string
  { "keys": ["alt+f5"],
    "command": "insert_date",
    "args": {"prompt": true} },

// Show the panel with pre-defined options from settings
  { "keys": ["f5"],
    "command": "insert_date",
    "args": {"prompt": true} }
]

```


### Format Examples

Here are some examples on how the values are interpreted.

For the accepted formatting syntax, see <http://strfti.me/> for an introduction
and [`datetime.strftime()` behavior][strftime] for all details.

For the exact accepted

| Format string              | Parameters                         | Resulting string                     |
| :------------------------- | :--------------------------------- | :----------------------------------- |
| `%d/%m/%Y %I:%M %p`        |                                    | 12/08/2014 08:55                     |
| `%d. %b %y`                |                                    | 12. Aug 14                           |
| `%H:%M:%S.%f%z`            |                                    | 20:55:00.473603+0200                 |
| `%Y-%m-%dT%H:%M:%S.%f%z`   |                                    | 2014-08-12T20:55:00.473603+0200      |
| `iso`                      | `{'tz_out': 'UTC'}`                | 2014-08-12T18:55:00+00:00            |
| `%c UTC%z`                 | `{'tz_in': 'local'}`               | 12.08.2014 20:55:00 UTC+0200         |
| `%X %Z`                    | `{'tz_in': 'Europe/Berlin'}`       | 20:55:00 CEST                        |
| `%d/%m/%Y %I:%M %Z`        | `{'tz_in': 'America/St_Johns'}`    | 12/08/2014 08:55 NDT                 |
| `%c %Z (UTC%z)`            | `{'tz_out': 'EST'}`                | 12.08.2014 13:55:00 EST (UTC-0500)   |
| `%x %X %Z (UTC%z)`         | `{'tz_out': 'America/New_York'}`   | 12.08.2014 14:55:00 EDT (UTC-0400)   |
| `unix`                     |                                    | 1407869700                           |


*Notes*:

- `Europe/Berlin` is my actual timezone.
- `%c`, `%x` and `%X` are representative for *Locale’s appropriate time
  representation*.
- `%p` also corresponds to the locale's setting, thus using `%p` e.g. on a
  German system gives an empty string.


### Snippet Macros

You can use the `insert_date` command in combination with snippets using
macros. Here is an example:

```json
[
    { "command": "insert_snippet", "args": {"contents": "Date: $1\nTime: $2\nSomething else: $0"} },
    { "command": "insert_date", "args": {"format": "%x"} },
    { "command": "next_field" },
    { "command": "insert_date", "args": {"format": "%X"} },
    { "command": "next_field" }
]
```

Check the documentation for [Macros][doc-macros] and [Commands][doc-commands] for further information.


### Command Reference

***insert_date_panel***

Open a quick panel with pre-defined format settings


***insert_date***

Insert the current date/time with specified formatting

*Parameters*

- **format** (str) - *Default*: `'%c'` (configurable in settings)

  A format string which is used to display the current time. See
  <http://strfti.me/> for an introduction and [`datetime.strftime()`
  behavior][strftime] for all details.

- **prompt** (bool) - *Default*: `False`

  If `True` a small popup window will be displayed where you can specify the
  format string manually. The string passed in `format` will be used as default
  text if available.

- **tz_in** (str) - *Default*: `'local'` (configurable in settings and
  recommended to change)

  Defines in which timezone the current time (read from your system) will be
  interpreted.

   May
  be one of [these][timezones] values or `'local'`.

- **tz_out** (str) - *Default*: `None`

  Defines on which timezone the output time should be based.

  By default, uses the same timezone as `tz_in`. May be one of
  [these][timezones] values or `'local'` (which does not support `%Z`, but
  `%z`).


### Settings ###

Settings can be accessed using the menu (*Preferences > Package Settings >
InsertDate > Settings - User/Default*) or the command palette ("Preferences:
InsertDate Settings - User/Default").

Here is an excerpt of the [default settings][settings]:

```js
{
    // This is the format that will be used as default when no format has been
    // specified when calling the command. Also used for the "InsertDate:
    // Default" command from the command palette.
    // Default: '%c'
    "format": "%c",

    // Similar to above, this is the default timezone that will be used when
    // there was no other incoming timezone specified. Because the default is
    // set to 'local' it will be interpreted as the timezone of your machine. As
    // of now, 'local' does not support the `%Z` named timezone representation
    // and it is HIGHLY RECOMMENDED to specify your a "pytz timezone" here.
    // See the readme for a link to the available timezones.
    // Default: 'local'
    "tz_in": "local",

    // A set of pre-defined settings that are prompted by "promt_insert_time"
    // and previewed. You can modify this list in your User settings, but be
    // aware that you remove ALL entries when overriding "prompt_config"!
    // Use "user_prompt_config" if you just want to add a few entries.
    //
    // `$default` is replaced by the "format" setting above, unspecified values
    // remain default.
    "prompt_config": [ //...
    ],

    // Works similar to "prompt_config" but is added to the above list.
    // Supposed to be used by you when you just want to add some entries to the
    // list.
    "user_prompt_config": []
}
```


## Libraries

- ***[pytz-2013b][pytz]*** ([ext. download][pytz-down])

  **pytz** by Stuart Bishop is used for displaying and conversion between
  timezones. **MIT license**


## License

The MIT License (MIT)

Copyright (c) 2014 FichteFoll

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.


## ToDo

- Shift times with a `shift` parameter (`datetime.timedelta(**shift)`)
- `locale` option to modify `%c %x %X %p` representation?


<!-- Links -->

[st]: http://sublimetext.com/

[pck-ctrl]: http://wbond.net/sublime_packages/package_control "Sublime Package Control by wbond"
[pck-browse]: https://sublime.wbond.net/packages/InsertDate "InsertDate - Packages - Package Control"

[pytz]: http://pytz.sourceforge.net/ "pytz - World Timezone Definitions for Python"
[strftime]: http://docs.python.org/3/library/datetime.html#strftime-strptime-behavior "Python docs: 8.1.8. strftime() and strptime() Behavior"
[pytz-down]: http://pypi.python.org/pypi/pytz#downloads "pytz : Python Package Index"

[scr-panel]: http://i.imgur.com/hObkE27.png
[scr-panel-thumb]: http://i.imgur.com/hObkE27l.png

[keymap]: Default.sublime-keymap "Default.sublime-keymap"
[keymap-osx]: Default%20%28OSX%29.sublime-keymap "Default (OSX).sublime-keymap"
[settings]: insert_date.sublime-settings "insert_date.sublime-settings"

[doc-macros]: http://docs.sublimetext.info/en/latest/extensibility/macros.html
[doc-commands]: http://docs.sublimetext.info/en/latest/reference/commands.html

[timezones]: https://github.com/FichteFoll/sublimetext-insertdate/blob/c879a70e12fb38c86a893b2be7979b4f7111b342/pytz/__init__.py#L527-L1101 "List of available timezones in source"
