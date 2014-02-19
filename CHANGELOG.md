InsertDate Changelog
====================

v0.5.4 (2014-02-19)
-------------------

- Fixed pytz loading for packed packages in ST3 (#10)


v0.5.3 (2014-01-14)
-------------------

- Fixed the default format (format=None) being ignored (#8)


v0.5.2 (2014-01-12)
-------------------

- Fixed the package not working at all on both ST2 and ST3 (#7)
- Added instructions for usage in macros/snippets


v0.5.1 (2014-01-11)
-------------------

- Added a panel to choose a format from, configurable via settings
- Changed default keybindings a bit (f5 -> ctrl+f5, ctrl+f5; panel on f5)


v0.5.0 (2014-01-11)
-------------------

- **InsertDate is now ST3-compatible!**

- Default to `%c` instead of `%x %X` which is more accurate
- 'unix' format added, representing the seconds since the epoch, in UTC (#2)


v0.4.0 (2013-07-11)
-------------------

- Default settings may now be modified
- Added menu items and command palette entries (#1)
- Fixed a bug with a codepage issue when the result was not utf-8 (#3)
- Updated keymaps and added a separate one for OSX


v0.3 (2012-05-13)
-----------------

- Add timezone support for incoming and outgoing timezone using pytz
  This also added named timezones for `%Z` format
- Updated keymaps


v0.2 (2012-05-12)
-----------------

- Added support for `%z` format (timezone offset)
- Added custom `iso` and `iso:Z` (`Z` could be any char) format
- Updated keymaps


v0.1 (2012-05-12)
-----------------

- Initial working state
