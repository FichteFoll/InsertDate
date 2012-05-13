# This loads the actual systems time locale, (None, None) otherwise.
# Required for use with datetime.strftime("%x %x").
import locale
locale.setlocale(locale.LC_TIME, '')

from datetime import datetime, timedelta, tzinfo
import pytz
from pytz.exceptions import *

try:
    basestring
except NameError:  # Python 3.x
    basestring = str


class LocalTimezone(tzinfo):
    """
    Helper class which extends datetime.tzinfo and implements the 'local timezone'
    (a.k.a. 'capturing the platform's idea of local time').
    Used in FormatDate as default fallback if no pytz timezone string is specified.

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


class FormatDate(object):
    """
    The actual processing class where conversation and formatting of datetime
    (between timezones) takes place.

    You can pass your own default values to the constructor which will be used
    if a parameter is missing during the process.

    `FormatDate().parse(format=None, tz_in=None, tz_out=None)`
    is most likely what you'll be using.
    """

    local = LocalTimezone()
    default = dict(
        # TODO: be modifiable from settings
        format="%x %X",
         tz_in="local"
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
        """Generates the according datetime object using given parameters"""
        # gather tzinfo data and raise a few exceptions
        if tz_in is None:
            tz_in = self.default['tz_in']

        if tz_in == "local":
            tz_in = self.local

        if isinstance(tz_in, basestring):
            try:
                tz_in = pytz.timezone(tz_in)
            except UnknownTimeZoneError:
                raise UnknownTimeZoneError("Parameter %r=%r is not a valid timezone name" % ('tz_in', tz_in))

        if not isinstance(tz_in, tzinfo):
            raise TypeError("Parameter 'tz_in' is not instance of datetime.tzinfo")

        try:
            tz_out = pytz.timezone(tz_out) if (tz_out is not None) else tz_in
        except UnknownTimeZoneError:
            raise UnknownTimeZoneError("Parameter %r=%r is not a valid timezone name" % ('tz_out', tz_out))

        # get timedata
        try:
            dt = tz_in.localize(datetime.now())
        except AttributeError:
            dt = datetime.now(tz=tz_in)

        # process timedata
        # TODO: shift datetime here | split into other function(s)
        if tz_out is tz_in:
            return dt

        dt = dt.astimezone(tz_out)
        try:
            return tz_out.normalize(dt)
        except AttributeError:
            pass

        return dt

    def date_format(self, dt, format=None):
        """
        Formats the given datetime object using `format` string.

        Differs from normal datetime.strftime function because I implemented
        some additional values (like 'iso') and a fallback for `format=None`
        is used.
        """
        if format is None:
            format = self.default['format']

        # 'iso:T'
        if format.startswith("iso"):
            sep = 'T'
            if len(format) == 5 and format[3] == ':':
                sep = str(format[-1])  # convert from unicode
            return dt.isoformat(sep)

        return dt.strftime(format)
