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

| Format string       | Resulting string    |
|:--------------------|:--------------------|
| `%d/%m/%Y %I:%M %p` | 12/05/2012 12:43 PM |
| `%d. %b %y`         | 12. May 12          |
| `%H:%M:%S.%f`       | 12:43:47.965000     |
| `%x %X`             | 05/12/12 12:43:47   |


## ToDo ##

- Default (fallback) format string to be configured
- Keep history of recently used format strings and display in a quick panel
- `shift` parameter (in style of `datetime.timedelta`)


[strptime]: http://docs.python.org/py3k/library/datetime.html#strftime-strptime-behavior "Python docs: 7.1.8. strftime() and strptime() Behavior"