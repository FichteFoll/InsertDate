========================
SublimeText - InsertDate
========================

A plugin for Sublime Text 2 that inserts the current date and/or time according to the format specified and supports named timezones (preferrably using [pytz][pytz], but can interpret the locale's timezone settings if necessary).

For more information about the accepted formatting syntax, see [`datetime.strftime()` behavior][strptime].


Install
-------

### Package Control ###

You can install this package with [Package Control][pck-ctrl] under `InsertDate`.

### Alternative ###

Browse the [Packages][packages-dir] sub-folder of your [Data directory][data-dir] and clone the repo:

    git clone git://github.com/FichteFoll/sublimetext-insertdate.git InsertDate

Alternatively you can download a recent [zip archive][releases] and extract it into an "InsertDate" sub-directory of the Packages dir mentioned above.


Usage
-----

### Command Examples ###

These are the [default key bindings][keymap] (on [OSX][keymap-osx]: `super` instead of `ctrl`):

```js
[
// Insert datetime using default format text
  { "keys": ["f5"],
    "command": "insert_date" },

// Insert datetime using the specified format
  // Locale date
  { "keys": ["ctrl+f5", "ctrl+d"],
    "command": "insert_date",
    "args": {"format": "%x"} },
  // iso date (YYYY-MM-DD)
  { "keys": ["ctrl+shift+f5", "ctrl+shift+d"],
    "command": "insert_date",
    "args": {"format": "%Y-%m-%d"} },
  // Locale time
  { "keys": ["ctrl+f5", "ctrl+t"],
    "command": "insert_date",
    "args": {"format": "%X"} },
  // iso time (HH:MM:SS)
  { "keys": ["ctrl+shift+f5", "ctrl+shift+t"],
    "command": "insert_date",
    "args": {"format": "%H:%M:%S"} },
  // Locale date and time with timezone name (not for 'local' timezone)
  { "keys": ["ctrl+f5", "ctrl+z"],
    "command": "insert_date",
    "args": {"format": "%x %X %Z"} },
  // Full iso date and time
  { "keys": ["ctrl+f5", "ctrl+i"],
    "command": "insert_date",
    "args": {"format": "iso"} },
  // Locale date and time converted to UTC (with timezone name)
  { "keys": ["ctrl+f5", "ctrl+u"],
    "command": "insert_date",
    "args": {"format": "%x %X %Z", "tz_out": "UTC"} },

// Prompt for user input, "format" would behave as default text,
// and insert the datetime using that format string
  { "keys": ["alt+f5"],
    "command": "insert_date",
    "args": {"prompt": true} }
]
```


### Format Examples ###

Here are some examples on how the values are interpreted.

For more information about the accepted formatting syntax, see [`datetime.strftime()` behavior][strptime].

| Format string            | Parameters                       | Resulting string                   |
|:-------------------------|:---------------------------------|:-----------------------------------|
| `%d/%m/%Y %I:%M %p`      |                                  | 13/05/2012 03:45                   |
| `%d. %b %y`              |                                  | 13. Mai 12                         |
| `%H:%M:%S.%f%z`          |                                  | 15:45:26.598000+0200               |
| `%Y-%m-%dT%H:%M:%S.%f%z` |                                  | 2012-05-13T15:45:26.598000+0200    |
| `iso`                    | `{'tz_out': 'UTC'}`              | 2012-05-13T13:45:26.598000+00:00   |
| `%x %X UTC%z`            | `{'tz_in': 'local'}`             | 13.05.2012 15:45:26 UTC+0200       |
| `%X %Z`                  | `{'tz_in': 'Europe/Berlin'}`     | 15:45:26 CEST                      |
| `%d/%m/%Y %I:%M %Z`      | `{'tz_in': 'America/St_Johns'}`  | 13/05/2012 03:45 NDT               |
| `%x %X %Z (UTC%z)`       | `{'tz_out': 'EST'}`              | 13.05.2012 08:45:26 EST (UTC-0500) |
| `%x %X %Z (UTC%z)`       | `{'tz_out': 'America/New_York'}` | 13.05.2012 09:45:26 EDT (UTC-0400) |


*Notes*:

- `Europe/Berlin` is my actual timezone.
- `%x` and `%X` are representative for *Locale’s appropriate time representation*.
- `%p` also corresponds to the locale's setting, thus using `%p` e.g. on a German system gives an empty string.


### Command Reference ###

***insert_date***

*Parameters*

- **format** (str) - *Default*: `'%x %X'`

  A format string which is used to display the current time. See [`datetime.strftime()` behavior][strptime] for reference.

- **prompt** (bool) - *Default*: `False`

  If `True` a small popup window will be displayed where you can specify the format string manually.
  The string passed in `format` will be used as default text if available.

- **tz_in** (str) - *Default*: `'local'`

  Defines in which timezone the current time (read from your system) will be interpreted. Required if you want `%Z` (your timezone's name).
  May be one of [these][timezones] values or `'local'`.

- **tz_out** (str) - *Default*: `None`

  Defines on which timezone the output time should be based.<br />
  May be one of [these][timezones] values or `'local'` (which does not support `%Z` yet, but `%z`).


### Settings ###

Settings have to be in a corresponding `insert_date.sublime-settings` file.
Here is an excerpt of the [default settings][settings]:

```js
{
    // This is the format that will be used when no format has been specified
    // when calling the command. Also used for the "InsertDate: Default"
    // command from the command palette.
    // Default: '%x %X'
    "format": "%x %X",

    // Similar to above, this is the default timezone that will be used when
    // there was no other incoming timezone specified. Because the default is
    // set to 'local' it will be interpreted the timezone of your machine. As
    // of now, 'local' does not support the `%Z` named timezone representation
    // and it is HIGHLY RECOMMENDED to specify your local pytz timezone here.
    // Default: 'local'
    "tz_in": "local"
}
```


Libraries
---------

- ***[pytz-2012c-py2.6][pytz]*** ([ext. download][pytz-down])<br />
     **pytz** by Stuart Bishop is used for displaying and conversion between timezones. **MIT license**


License
-------

The MIT License (MIT)

Copyright (c) 2013 FichteFoll

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


ToDo
----

- Support `%Z` with `tz_in="local"`
- Default (fallback) format string to be configured in settings
- `shift` parameter (`datetime.timedelta(**shift)`)
- `locale` option to modify `%x %X %p` representation?
- Keep history of recently used format strings and display in a quick panel


<!-- Links -->

[github]: https://github.com/FichteFoll/sublimetext-insertdate "Github.com: FichteFoll/sublime-insertdate"
[zipball]: https://github.com/FichteFoll/sublimetext-insertdate/zipball/master
[releases]: https://github.com/FichteFoll/sublimetext-insertdate/releases "Releases - FichteFoll/sublime-insertdate"

[pck-ctrl]: http://wbond.net/sublime_packages/package_control "Sublime Package Control by wbond"
[data-dir]: http://docs.sublimetext.info/en/latest/basic_concepts.html#the-data-directory
[packages-dir]: http://docs.sublimetext.info/en/latest/basic_concepts.html#the-packages-directory

[pytz]: http://pytz.sourceforge.net/ "pytz - World Timezone Definitions for Python"
[strptime]: http://docs.python.org/py3k/library/datetime.html#strftime-strptime-behavior "Python docs: 7.1.8. strftime() and strptime() Behavior"
[pytz-down]: http://pypi.python.org/pypi/pytz#downloads "pytz : Python Package Index"

[keymap]: Default.sublime-keymap "Default.sublime-keymap"
[keymap-osx]: Default%20%28OSX%29.sublime-keymap "Default (OSX).sublime-keymap"
[settings]: insert_date.sublime-settings "insert_date.sublime-settings"

[timezones]: https://github.com/FichteFoll/sublimetext-insertdate/blob/c879a70e12fb38c86a893b2be7979b4f7111b342/pytz/__init__.py#L527-L1101 "List of timezones in source"
