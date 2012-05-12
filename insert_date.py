import sublime_plugin
from datetime import datetime, timedelta, tzinfo
from functools import partial


class LocalDatetime(object):
    """
    Wrapper class that uses the local timezone for formatting a datetime.
    """

    class LocalTimezone(tzinfo):
        import time
        """
        Helper class which extends datetime.tzinfo and supports the local timezone
        (a.k.a. capturing the platform's idea of local time).

        Source: http://docs.python.org/library/datetime.html#tzinfo-objects"""

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
            # TODO: This is buggy (at least for my system)
            # tzname = self.time.tzname
            # print tzname
            # print("tzname: %s" % str(tzname[self._isdst(dt)]))
            # return self.time.tzname[self._isdst(dt)]
            return None

        def _isdst(self, dt):
            tt = (dt.year, dt.month, dt.day,
                  dt.hour, dt.minute, dt.second,
                  dt.weekday(), 0, 0)
            stamp = self.time.mktime(tt)
            tt = self.time.localtime(stamp)
            return tt.tm_isdst > 0

    local = LocalTimezone()

    def __init__(self, dt=None):
        if dt is None:
            dt = datetime.now(tz=self.local)
        if not isinstance(dt, datetime):
            raise TypeError("Parameter is not instance of datetime.datetime")

        self.dt = dt.astimezone(self.local)
        print dt

    @staticmethod
    def _format(dt, format):
        # 'iso:T'
        if format.startswith("iso"):
            sep = 'T'
            if len(format) == 5 and format[3] == ':':
                sep = str(format[-1])  # convert from unicode
            return dt.isoformat(sep)

        return dt.strftime(format)

    def format(self, format):
        return LocalDatetime._format(self.dt, format)

    def __getattr__(self, attr):
        return getattr(self.dt, attr)


class InsertDateCommand(sublime_plugin.TextCommand):
    """Prints Date according to given format string"""
    default_format = "%Y-%m-%d %H:%M"

    def run(self, edit, format=None, prompt=False):
        if prompt:
            self.view.window().show_input_panel(
                "Date format string:",
                format or '',
                # pass this function as callback
                partial(self.run, edit),
                None, None
            )
            return  # call already handled

        elif format is None:
            format = self.default_format

        if not format:
            # emtpy string entered in input panel
            return

        text = LocalDatetime().format(format)

        for r in self.view.sel():
            if r.empty():
                self.view.insert (edit, r.begin(), text)
            else:
                self.view.replace(edit, r, text)
