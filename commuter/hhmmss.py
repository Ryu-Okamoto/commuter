from __future__ import annotations
import re


class HHMMSS:
    def __init__(self, hhmmss: str):
        assert validate_hhmmss(hhmmss)
        self._hhmmss = hhmmss
        self.hh = hhmmss[:2]
        self.mm = hhmmss[2:4]
        self.ss = hhmmss[4:]

    @classmethod
    def from_hhmmss(cls, hhmmss: str | None) -> HHMMSS | None:
        if hhmmss is None or not validate_hhmmss(hhmmss):
            return None
        return HHMMSS(hhmmss)
    
    @classmethod
    def from_seconds(cls, seconds: int) -> HHMMSS | None:
        return HHMMSS.from_hhmmss(deserialize(seconds))
    
    def to_str(self) -> str | None:
        if not self._valid:
            return None
        hh = self.hh.lstrip('0')
        mm = self.mm.lstrip('0') if hh == '' else mm
        ss = self.ss.lstrip('0') if mm == '' else ss
        return \
            hh + '時間' if hh != '' else '' + \
            mm + '分' if mm != '' else '' + \
            ss + '秒' if ss != '' else ''
    
    def diff(self, other: HHMMSS) -> HHMMSS | None:
        if not self._valid or not other._valid:
            return None
        return HHMMSS.from_hhmmss(
            subtract_hhmmss(self._hhmmss, other._hhmmss))
    

def validate_hhmmss(hhmmss: str) -> bool:
    HHMMSS_PATTERN = f'{HOURS_PATTERN}{MINUTES_PATTERN}{SECONDS_PATTERN}'
    return bool(re.match(HHMMSS_PATTERN, hhmmss))


def validate_sec_from_000000(sec_from_000000: int) -> bool:
    return sec_from_000000 >= 0 and sec_from_000000 <= MAX_SECONDS


# convert datetime formatted "%H%M%S" to seconds from 00:00:00
def serialize(hhmmss: str) -> int | None:
    if not validate_hhmmss(hhmmss):
        return None
    hours = int(hhmmss[:2])
    minutes = int(hhmmss[2:4])
    seconds = int(hhmmss[4:])
    return \
        SECONDS_PER_MINUTES * MINUTES_PER_HOUR * hours \
        + SECONDS_PER_MINUTES * minutes \
        + seconds


# convert seconds from 00:00:00 to datetime formatted "%H%M%S"
def deserialize(sec_from_000000: int) -> str | None:
    if not validate_sec_from_000000(sec_from_000000):
        return None
    hours = (sec_from_000000 // SECONDS_PER_MINUTES) // MINUTES_PER_HOUR
    minutes = (sec_from_000000 // SECONDS_PER_MINUTES) % MINUTES_PER_HOUR
    seconds = sec_from_000000 % SECONDS_PER_MINUTES
    return str(hours).zfill(2) + str(minutes).zfill(2) + str(seconds).zfill(2)


def subtract_hhmmss(lhnd: str, rhnd: str) -> str | None:
    if not validate_hhmmss(lhnd) or not validate_hhmmss(rhnd):
        return None
    lhnd = serialize(lhnd)
    rhnd = serialize(rhnd)
    if lhnd is None or rhnd is None or lhnd < rhnd:
        return None
    return deserialize(lhnd - rhnd)


HOURS_PATTERN = r'[01][0-9]|2[0-3]'
MINUTES_PATTERN = r'[0-5][0-9]'
SECONDS_PATTERN = r'[0-5][0-9]'

MINUTES_PER_HOUR = 60
SECONDS_PER_MINUTES = 60

MAX_SECONDS = \
    SECONDS_PER_MINUTES * MINUTES_PER_HOUR * 23 \
    + SECONDS_PER_MINUTES * 59 \
    + 59