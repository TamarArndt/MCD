from datetime import datetime
import pytz

# how this works:
"""
timestamp in msec
 | utc.localize(datetime.utcfromtimestamp( timestampobject )
 v
UTC
 | cet.normalize( utcobject )
 v
CET
 | utc.normalize( cetobject )
 v
UTC
 | int( utcobject - epoch ).total_seconds() * 1000 )
 v
timestamp in msec
"""

# timezones
utc = pytz.utc
cet = pytz.timezone("Europe/Berlin") # includes as well cet as cest


def timestamp_to_utc(_timestamp):
    return utc.localize(datetime.utcfromtimestamp(_timestamp/1000))


def utc_to_cet(_utc):
    return utc_to_giventimezone(_utc, cet)


def utc_to_giventimezone(_utc, pytztimezone):
    """ pytztimezone is one of utc, cet, ... """
    return pytztimezone.normalize(_utc)


def cet_to_utc(_cet):
    return utc.normalize(_cet)


def utc_to_timestamp(_utc):
    epoch = utc.localize(datetime(1970,1,1))
    return int((_utc - epoch).total_seconds() * 1000 )


def cetdatetime_to_timestamp(_cetdatetime):
    ''' input _cetdatetime must not be offset-aware/tz-aware '''
    return utc_to_timestamp(cet_to_utc(cet.localize(_cetdatetime)))

def utcdatetime_to_timestamp(_utcdatetime):
    return utc_to_timestamp(utc.localize(_utcdatetime))

def timestamp_to_cet(_timestamp):
    return utc_to_cet(timestamp_to_utc(_timestamp))

