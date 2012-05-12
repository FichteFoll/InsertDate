# SublimeText-InsertDate #

A plugin for Sublime Text 2 that inserts the current date and/or hour according to the format specified.
It supports multiple selections (regions) and will replace selected text.

For more information about the accepted formatting syntax, see [`datetime.strftime()` behavior][strptime].

## Usage ##

Example key definitions as follows:

	{ "keys": ["ctrl+f5"],  "command": "insert_date" },
	{ "keys": ["shift+f5"], "command": "insert_date", "args": {"format": "%H:%M:%S"} },
	{ "keys": ["alt+f5"],   "command": "insert_date", "args": {"format": "%d/%m/%Y %I:%M %p", "prompt": true} }

### Format Examples ###

| Format string       | Resulting string                 |
|:--------------------|:---------------------------------|
| `%d/%m/%Y %I:%M %p` | 12/05/2012 03:49 PM              |
| `%d. %b %y`         | 12. May 12                       |
| `%H:%M:%S.%f%z`     | 15:49:55.287000+0200             |
| `%x %X`             | 05/12/12 15:49:55                |
| `iso`               | 2012-05-12T15:49:55.287000+02:00 |


## ToDo ##

- Support `%Z` as named timezone
- Allow output timezone to be specified
- Default (fallback) format string to be configured
- Keep history of recently used format strings and display in a quick panel
- `shift` parameter (in style of `datetime.timedelta`)


[strptime]: http://docs.python.org/py3k/library/datetime.html#strftime-strptime-behavior "Python docs: 7.1.8. strftime() and strptime() Behavior"