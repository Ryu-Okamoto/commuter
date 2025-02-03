import re


HOURS_PATTERN = r'[01][0-9]|2[0-3]'
MINUTES_PATTERN = r'[0-5][0-9]'
SECONDS_PATTERN = r'[0-5][0-9]'

MINUTES_PER_HOUR = 60
SECONDS_PER_MINUTES = 60

MAX_SECONDS = \
    SECONDS_PER_MINUTES * MINUTES_PER_HOUR * 23 \
    + SECONDS_PER_MINUTES * 59 \
    + 59


def validate_hhmmss(hhmmss: str) -> bool:
    HHMMSS_PATTERN = f'{HOURS_PATTERN}{MINUTES_PATTERN}{SECONDS_PATTERN}'
    return bool(re.match(HHMMSS_PATTERN, hhmmss))


# convert datetime formatted "%H%M%S" to seconds from 00:00:00
def serialize(hhmmss: str) -> int:
    assert validate_hhmmss(hhmmss)
    hours = int(hhmmss[:2])
    minutes = int(hhmmss[2:4])
    seconds = int(hhmmss[4:])
    return \
        SECONDS_PER_MINUTES * MINUTES_PER_HOUR * hours \
        + SECONDS_PER_MINUTES * minutes \
        + seconds


# convert seconds from 00:00:00 to datetime formatted "%H%M%S"
def deserialize(sec_from_000000: int) -> str:
    assert sec_from_000000 >= 0 and sec_from_000000 <= MAX_SECONDS
    hours = (sec_from_000000 // SECONDS_PER_MINUTES) // MINUTES_PER_HOUR
    minutes = (sec_from_000000 // SECONDS_PER_MINUTES) % MINUTES_PER_HOUR
    seconds = sec_from_000000 % SECONDS_PER_MINUTES
    return str(hours).zfill(2) + str(minutes).zfill(2) + str(seconds).zfill(2)