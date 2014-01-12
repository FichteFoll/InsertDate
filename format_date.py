# This loads the actual systems time local_tze, (None, None) otherwise.
# Required for use with datetime.strftime("%c %x %X").
import locale
locale.setlocale(locale.LC_TIME, '')

from datetime import datetime, timedelta, tzinfo
import time

try:
    from . import pytz
    from .pytz.exceptions import UnknownTimeZoneError
except ValueError:
    import pytz
    from pytz.exceptions import UnknownTimeZoneError

# Not using sublime.version here because it's supposed to be used externally too
import sys
ST2 = sys.version_info[0] == 2

if not ST2:
    basestring = str


class LocalTimezone(tzinfo):
    """Helper class which extends datetime.tzinfo and implements the 'local timezone'.
    (Read: captures the platform's idea of local time.)
    Used in FormatDate as default fallback if no pytz timezone string is specified.

    Source: http://docs.python.org/library/datetime.html#tzinfo-objects
    """

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
        # print time.tzname
        # print unicode(time.tzname[0])
        # return time.tzname[self._isdst(dt)].decode('utf-8')
        return None

    def _isdst(self, dt):
        tt = (dt.year, dt.month, dt.day,
              dt.hour, dt.minute, dt.second,
              dt.weekday(), 0, 0)
        stamp = time.mktime(tt)
        tt = time.localtime(stamp)
        return tt.tm_isdst > 0


class FormatDate(object):
    """The actual processing class where conversation and formatting of datetime (between timezones)
    takes place.

    You can pass your own default values to the constructor which will be used as default values if
    a parameter is missing during the process.

    `FormatDate().parse(format=None, tz_in=None, tz_out=None)` is most likely what you'll be using.
    """

    local_tz = LocalTimezone()
    default = dict(
        format="%c",
        tz_in="local"
    )

    def __init__(self, local_tz=None, default=None):
        if local_tz:
            if isinstance(local_tz, tzinfo):
                self.local_tz = local_tz
            else:
                raise TypeError("Parameter 'local' is not an instance of datetime.tzinfo")

        if not default is None:
            self.set_default(default)

    def set_default(self, update):
        # Update only the keys that are defined in self.default
        for k, v in update.items():
            if k in self.default:
                self.default[k] = v

    def parse(self, format=None, tz_in=None, tz_out=None):
        # 'unix'
        if format == "unix":
            return str(time.time())

        # anything else
        dt = self.date_gen(tz_in, tz_out)
        text = self.date_format(dt, format)

        # Fix potential unicode/codepage issues
        if ST2 and isinstance(text, str):
            try:
                text = text.decode(locale.getpreferredencoding())
            except UnicodeDecodeError:
                text = text.decode('utf-8')

        return text

    def check_tzparam(self, tz, name):
        if isinstance(tz, basestring):
            try:
                return pytz.timezone(tz)
            except UnknownTimeZoneError:
                raise UnknownTimeZoneError("Parameter %r = %r is not a valid timezone name"
                                           % (name, tz))

        if tz is not None and not isinstance(tz, tzinfo):
            raise TypeError("Parameter %r = %r is not an instance of datetime.tzinfo"
                            % (name, tz))

        # Nothing else to be done
        return tz

    def date_gen(self, tz_in=None, tz_out=None):
        """Generates the according datetime object using given parameters"""
        # Check parameters and gather tzinfo data (and raise a few exceptions)
        if tz_in is None:
            tz_in = self.default['tz_in']

        if tz_in == "local":
            tz_in = self.local_tz

        tz_in  = self.check_tzparam(tz_in,  'tz_in')
        tz_out = self.check_tzparam(tz_out, 'tz_out')

        # Get timedata
        try:
            dt = tz_in.localize(datetime.now())
        except AttributeError:
            # Fallback for non-pytz timezones ('local')
            dt = datetime.now(tz=tz_in)

        # Process timedata
        # TODO: shift datetime here | split into other function(s)
        if not tz_out:
            return dt

        # Adjust timedata for target timezone
        dt = dt.astimezone(tz_out)
        try:
            return tz_out.normalize(dt)
        except AttributeError:
            # Fallback for non-pytz timezones ('local')
            return dt

    def date_format(self, dt, format=None):
        """Formats the given datetime object using `format` string.

        Differs from normal datetime.strftime function because I implemented
        some additional values (like 'iso') and a fallback for `format=None`
        is used.
        """
        if format is None:
            format = self.default['format']

        # 'iso', 'iso:T'
        if format.startswith("iso"):
            sep = 'T'
            if len(format) == 5 and format[3] == ':':
                sep = str(format[-1])  # convert from unicode (ST2)
            return dt.isoformat(sep)

        return dt.strftime(format)
