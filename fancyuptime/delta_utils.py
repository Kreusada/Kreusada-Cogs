import datetime
import discord
from typing import Optional, SupportsInt

def humanize_timedelta(
    *, timedelta: Optional[datetime.timedelta] = None, seconds: Optional[SupportsInt] = None
) -> str:
    """
    Get a locale aware human timedelta representation.
    This works with either a timedelta object or a number of seconds.
    Fractional values will be omitted, and values less than 1 second
    an empty string.
    Parameters
    ----------
    timedelta: Optional[datetime.timedelta]
        A timedelta object
    seconds: Optional[SupportsInt]
        A number of seconds
    Returns
    -------
    str
        A locale aware representation of the timedelta or seconds.
    Raises
    ------
    ValueError
        The function was called with neither a number of seconds nor a timedelta object
    """

    try:
        obj = seconds if seconds is not None else timedelta.total_seconds()
    except AttributeError:
        raise ValueError("You must provide either a timedelta or a number of seconds")

    seconds = int(obj)
    periods = [
        (_("year"), _("years"), 60 * 60 * 24 * 365),
        (_("month"), _("months"), 60 * 60 * 24 * 30),
        (_("day"), _("days"), 60 * 60 * 24),
        (_("hour"), _("hours"), 60 * 60),
        (_("minute"), _("minutes"), 60),
        (_("second"), _("seconds"), 1),
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
