# InsertDate - Sublime Text Plugin

A plugin for [Sublime Text][st] 2 and 3 that inserts the current date and/or
time according to the format specified, supporting named timezones.

![insertdate](https://cloud.githubusercontent.com/assets/931051/9400476/e64b49f8-47c1-11e5-9088-e4f0f0778011.gif)

For a brief introduction about the accepted formatting syntax, see
<http://strfti.me/>. *Might yield different results, see
[below](#format-examples).*


## Installation

You **must** install this package with [Package Control][pck-ctrl], under
[`InsertDate`][pck-browse].

Upon installation, you will be asked to select your local timezone. This is
required for pretty formatting of the `%Z` variable and should be set, but
InsertDate will work without it.
You can change this setting at any time with the "InsertDate: Select Timezone"
command from the command palette.


## Usage

The quick panel (see gif) opens on <kbd>F5</kbd> and shows a selection of
pre-defined settings that can be modified. See [Settings](#settings) on how to do that.

However, there are many more default key bindings available to provide you with
the most-needed formats and a command that allows you to insert your own
format and output timezone on the fly.


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

// Prompt for user input ("format" behaves as default text)
// and output timezone, if none provided,
// and then insert the datetime with these parameters
  { "keys": ["alt+f5"],
    "command": "insert_date_prompt" },

// Show the panel with pre-defined options from settings
  { "keys": ["f5"],
    "command": "insert_date_panel" }
]

```


### Settings ###

Settings can be accessed using the menu (*Preferences > Package Settings >
InsertDate > Settings - User/Default*) or the command palette ("Preferences:
InsertDate Settings - User/Default").

You can also view the default settings [here][settings].


### Format Examples

For the accepted formatting syntax, see <http://strfti.me/> for an introduction
and [`datetime.strftime()` behavior][strftime] for all details. Note that the
introduction uses a different library and thus *may yield different results*.

Here are some examples on how the values are interpreted:

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

- `CET` is my actual timezone.
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


***insert_date_prompt***

Open a small panel where you can specify the format string manually. The string
passed in `format` will be used as default text if available. Accepts the same parameters as ***insert_date***.

<!-- Links -->

[st]: http://sublimetext.com/

[pck-ctrl]: http://wbond.net/sublime_packages/package_control "Sublime Package Control by wbond"
[pck-browse]: https://sublime.wbond.net/packages/InsertDate "InsertDate - Packages - Package Control"

[strftime]: http://docs.python.org/3/library/datetime.html#strftime-strptime-behavior "Python docs: 8.1.8. strftime() and strptime() Behavior"

[scr-panel]: http://i.imgur.com/hObkE27.png
[scr-panel-thumb]: http://i.imgur.com/hObkE27l.png

[keymap]: Default.sublime-keymap "Default.sublime-keymap"
[keymap-osx]: Default%20%28OSX%29.sublime-keymap "Default (OSX).sublime-keymap"
[settings]: insert_date.sublime-settings "insert_date.sublime-settings"

[doc-macros]: http://docs.sublimetext.info/en/latest/extensibility/macros.html
[doc-commands]: http://docs.sublimetext.info/en/latest/reference/commands.html

[timezones]: https://github.com/FichteFoll/sublimetext-insertdate/blob/a940b4c4394022725ba933c7db0deb1fb8d21efe/format_date/pytz/__init__.py#L1090-L1520 "List of common timezones (in source)"
