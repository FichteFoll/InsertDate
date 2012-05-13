import sublime
import sublime_plugin
from datetime import datetime, timedelta, tzinfo
from functools import partial
import pytz
from pytz.exceptions import *


class LocalTimezone(tzinfo):
    """
    Helper class which extends datetime.tzinfo and implements the 'local timezone'
    (a.k.a. 'capturing the platform's idea of local time').

    Source: http://docs.python.org/library/datetime.html#tzinfo-objects
    """

    import time

    STDOFFSET = timedelta(seconds=-time.timezone)
    if time.daylight:
        DSTOFFSET = timedelta(seconds=-time.altzone)
    else:
        DSTOFFSET = STDOFFSET

    DSTDIFF = DSTOFFSET - STDOFFSET

    def utcoffset(self, dt):
        if self._isdst(dt):
            return self.DSTOFFSET
        else:
            return self.STDOFFSET

    def dst(self, dt):
        if self._isdst(dt):
            return self.DSTDIFF
        else:
            return timedelta(0)

    def tzname(self, dt):
        # TODO: This is buggy (I hate ASCII)
        # print self.time.tzname
        # print unicode(self.time.tzname[0])
        # return self.time.tzname[self._isdst(dt)].decode('utf-8')
        return None

    def _isdst(self, dt):
        tt = (dt.year, dt.month, dt.day,
              dt.hour, dt.minute, dt.second,
              dt.weekday(), 0, 0)
        stamp = self.time.mktime(tt)
        tt = self.time.localtime(stamp)
        return tt.tm_isdst > 0


class InsertDate(object):
    local = LocalTimezone()
    default = dict(
        # TODO: be modifiable from settings
        format="%Y-%m-%d %H:%M",
         tz_in="Europe/Berlin"
    )

    def __init__(self, local=None, default=None):
        if not local is None:
            if isinstance(local, tzinfo):
                self.local = local
            else:
                raise TypeError("Parameter 'local' is not instance of datetime.tzinfo")

        if not default is None:
            try:
                self.default.update(default)  # just raise the error if it appears
            except ValueError:
                raise ValueError("Parameter 'default' is not iterable")

    def parse(self, format=None, tz_in=None, tz_out=None):
        dt = self.date_gen(tz_in, tz_out)
        return self.date_format(dt, format)

    def date_gen(self, tz_in=None, tz_out=None):
        # gather tzinfo data and raise a few exceptions
        if tz_in is None:
            tz_in = self.default['tz_in']

        if tz_in == "local":
            tz_in = self.local

        if isinstance(tz_in, basestring):
            try:
                tz_in = pytz.timezone(tz_in)
            except UnknownTimeZoneError:
                raise UnknownTimeZoneError("Parameter %r=%r is not a valid timezone string" % ('tz_in', tz_in))

        if not isinstance(tz_in, tzinfo):
            raise TypeError("Parameter 'tz_in' is not instance of datetime.tzinfo")

        try:
            tz_out = pytz.timezone(tz_out) if (tz_out is not None) else tz_in
        except UnknownTimeZoneError:
            raise UnknownTimeZoneError("Parameter %r=%r is not a valid timezone string" % ('tz_out', tz_out))

        # get timedata
        try:
            dt = tz_in.localize(datetime.now())
        except AttributeError:
            dt = datetime.now(tz=tz_in)

        # process timedata
        # TODO: shift datetime here
        if tz_out is tz_in:
            return dt

        dt = dt.astimezone(tz_out)
        try:
            return tz_out.normalize(dt)
        except AttributeError:
            pass

        return dt

    def date_format(self, dt, format=None):
        if format is None:
            format = self.default['format']

        # 'iso:T'
        if format.startswith("iso"):
            sep = 'T'
            if len(format) == 5 and format[3] == ':':
                sep = str(format[-1])  # convert from unicode
            return dt.isoformat(sep)

        return dt.strftime(format)


class InsertDateCommand(sublime_plugin.TextCommand, InsertDate):
    """Prints Date according to given format string"""

    def run(self, edit, format=None, prompt=False, tz_in=None, tz_out=None):
        if prompt:
            self.view.window().show_input_panel(
                "Date format string:",
                str(format) if format else '',
                # pass this function as callback
                partial(self.run, edit, tz_in=tz_in, tz_out=tz_out),
                None, None
            )
            return  # call already handled

        if format == '' or (isinstance(format, basestring) and format.isspace()):
            # emtpy string or whitespaces entered in input panel
            return

        # do the actual parse action
        try:
            text = self.parse(format, tz_in, tz_out)
        except Exception as e:
            sublime.error_message("[InsertDate]\n%s: %s" % (type(e).__name__, e))
            return

        if text == '' or text.isspace():
            # don't bother replacing selections with actually nothing
            return

        if type(text) == str:
            print text
            text = text.decode('utf-8')

        for r in self.view.sel():
            if r.empty():
                self.view.insert (edit, r.a, text)
            else:
                self.view.replace(edit, r,   text)
