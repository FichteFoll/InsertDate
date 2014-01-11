InsertDate
==========

Plugin that inserts the current date and/or hour according to the specified
format and supports named timezones (as well as the locale's timezone settings if necessary).


Key Bindings (and Examples)
---------------------------

Browse "Preferences > Package Settings > InsertDate > Key Bindings - Default" for an overview of the default key bindings, which are great examples for usage.


Settings
--------

Browse "Preferences > Package Settings > InsertDate > Settings - Default" for an overview of available settings.

RECOMMENDED: You should adjust your "tz_in" setting so that InsertDate knows what your current timezone is and can represent it when using `%Z`.
For available timezones, check https://github.com/FichteFoll/sublimetext-insertdate/blob/c879a70e12fb38c86a893b2be7979b4f7111b342/pytz/__init__.py#L527-L1101.


Format Examples
---------------

Python docs: 8.1.8. strftime() and strptime() Behavior:
    http://docs.python.org/3/library/datetime.html#strftime-strptime-behavior

Here are some examples on how the values are interpreted.

| Format string            | Parameters                       | Resulting string                   |
|:-------------------------|:---------------------------------|:-----------------------------------|
| `%m/%d/%Y %I:%M %p`      |                                  | 07/13/2013 10:56                   |
| `%d. %b %y`              |                                  | 13. Jul 13                         |
| `%H:%M:%S.%f%z`          |                                  | 22:56:15.333000+0200               |
| `%Y-%m-%dT%H:%M:%S.%f%z` |                                  | 2013-07-13T22:56:15.333000+0200    |
| `iso`                    | `{'tz_out': 'UTC'}`              | 2013-07-13T20:56:15.333000+00:00   |
| `%c UTC%z`               | `{'tz_in': 'local'}`             | 13.07.2013 22:56:15 UTC+0200       |
| `%X %Z`                  | `{'tz_in': 'Europe/Berlin'}`     | 22:56:15 CEST                      |
| `%m/%d/%Y %I:%M %Z`      | `{'tz_in': 'America/St_Johns'}`  | 07/13/2013 10:56 NDT               |
| `%c %Z (UTC%z)`          | `{'tz_out': 'EST'}`              | 13.07.2013 15:56:15 EST (UTC-0500) |
| `%x %X %Z (UTC%z)`       | `{'tz_out': 'America/New_York'}` | 13.07.2013 16:56:15 EDT (UTC-0400) |
| `unix`                   |                                  | 1373748975.33                      |

Notes:

- `Europe/Berlin` is my actual timezone.
- `%c`, `%x` and `%X` are representative for *Locale’s appropriate time representation*.
- `%p` also corresponds to the locale's setting, thus using `%p` e.g. on a German system gives an empty string.


Command Reference
-----------------

***insert_date_panel***

Open a quick panel with pre-defined format settings


***insert_date***

Insert the current date/time with specified formatting

Parameters:

- format (str) - Default: `'%c'` (configurable in settings)

  A format string which is used to display the current time. See below for more information.

- prompt (bool) - Default: `False`

  If `True` a small popup window will be displayed where you can specify the format string manually.
  The string passed in `format` will be used as default text if available.

- tz_in (str) - Default: `'local'` (configurable in settings)

  Defines in which timezone the current time (read from your system) will be interpreted.
  Required if you want %Z (your timezone's name). May be one of the following values or `'local'`:
  https://github.com/FichteFoll/sublimetext-insertdate/blob/c879a70e12fb38c86a893b2be7979b4f7111b342/pytz/__init__.py#L527-L1101

- tz_out (str) - Default: `None`

  Defines on which timezone the output time should be based.
  Supports the same values as tz_in ('local' does not support %Z yet).
