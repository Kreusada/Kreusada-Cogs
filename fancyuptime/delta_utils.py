import datetime
import discord
from typing import Optional, SupportsInt

def humanize_timedelta(
    *, timedelta: Optional[datetime.timedelta] = None, seconds: Optional[SupportsInt] = None
) -> str:

    try:
        obj = seconds if seconds is not None else timedelta.total_seconds()
    except AttributeError:
        raise ValueError("You must provide either a timedelta or a number of seconds")

    seconds = int(obj)
    periods = [
        (("year"), ("years"), 60 * 60 * 24 * 365),
        (("month"), ("months"), 60 * 60 * 24 * 30),
        (("day"), ("days"), 60 * 60 * 24),
        (("hour"), ("hours"), 60 * 60),
        (("minute"), ("minutes"), 60),
        (("second"), ("seconds"), 1),
    ]

    strings = []
    for period_name, plural_period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            if period_value == 0:
                continue
            unit = plural_period_name if period_value > 1 else period_name
            strings.append(f"{period_value} {unit}")

    return ", ".join(strings)
