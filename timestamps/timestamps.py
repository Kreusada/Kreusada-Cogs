from datetime import datetime

import dateparser
import discord
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.commands import BadArgument, Cog, Context, Converter, FlagConverter
from typing import Optional

timestamp_formats = {
    "t": "Short Time",
    "T": "Long Time",
    "d": "Short Date",
    "D": "Long Date",
    "f": "Short Date and Time",
    "F": "Long Date and Time",
    "R": "Relative Time"
}


def date_parse_logic(arg: str) -> datetime:
    parsed = dateparser.parse(arg)
    if parsed is None:
        raise BadArgument("Unrecognized date/time.")
    return parsed

class DateConverter(Converter):
    """Date converter which uses dateparser.parse()."""

    async def convert(self, ctx: Context, arg: str) -> datetime:
        return date_parse_logic(arg)
    
class TimeStampFormatConverter(Converter):
    async def convert(self, ctx: Context, argument: str):
        if argument not in timestamp_formats:
            raise commands.BadFlagArgument(
                f"Invalid timestamp format. Available formats: {', '.join(timestamp_formats)}"
            )
        return argument


class TimeStampArgumentConverter(FlagConverter):
    format: Optional[str] = commands.flag(name="format", default=None, converter=TimeStampFormatConverter, aliases=["f"])
    content: Optional[str] = commands.flag(name="content", default=lambda c: date_parse_logic("now"), converter=DateConverter, aliases=["c"], positional=True)
    raw: Optional[str] = commands.flag(name="raw", default=False, converter=bool, aliases=["r"])

    async def convert(self, ctx: commands.Context, argument: str):
        try:
            return await super().convert(ctx, argument)
        except commands.BadFlagArgument as e:
            raise commands.UserFeedbackCheckFailure(
                f"Invalid value for the {e.flag.attribute!r} option."
            )
        except commands.MissingFlagArgument as e:
            raise commands.UserFeedbackCheckFailure(
                f"No value provided for the {e.flag.attribute!r} option."
            )
        except commands.TooManyFlags as e:
            raise commands.UserFeedbackCheckFailure(
                f"Too many values provided for the {e.flag.attribute!r} option."
            )
        
    def to_dict(self):
        """debugging"""
        return {
            "format": self.format,
            "content": self.content,
            "raw": self.raw,
        }

class TimeStamps(Cog):
    """Retrieve timestamps for certain dates."""

    __author__ = "Kreusada"
    __version__ = "1.2.0"

    def __init__(self, bot: Red):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        return

    @commands.command(usage="<date_or_time>", aliases=["timestamps"])
    async def timestamp(self, ctx: Context, *, tac: TimeStampArgumentConverter):
        """Produce a Discord timestamp.

        Timestamps are a feature added to Discord in the summer of 2021,
        which allows you to send timestamps will which update accordingly
        with any user's date time settings.

        **Example Usage**

        - `[p]timestamp 1st of october 2021`
        - `[p]timestamp 20 hours ago raw:true`
        - `[p]timestamp in 50 minutes`
        - `[p]timestamp 01/10/2021 format:f`
        - `[p]timestamp now raw:true format:R`
        """
        try:
            ts = int(tac.content.timestamp())
        except OSError:
            return await ctx.send(
                "An operating system error occured whilst attempting to get "
                "information for this timestamp."
            )
        if tac.raw:
            message = ""
        else:
            message = "### "
            if tac.format:
                message += f"**{timestamp_formats[tac.format]}** (`{tac.content}`)"
            else:
                message += f"**Timestamps** (`{tac.content}`)"
            message += "\n\n"
        # I'm aware that discord.utils.format_dt exists, but I prefer this layout
        # for readability purposes (and its more efficient for this specific use case)
        delim = " " if tac.format else "\n"
        if not tac.format:
            for i in "fFdDtTR":
                if not tac.raw:
                    message += f"`<t:{ts}:{i}>`: "
                message += f"<t:{ts}:{i}>{delim}"
        else:
            if not tac.raw:
                message += f"`<t:{ts}:{tac.format}>`: "
            message += f"<t:{ts}:{tac.format}>"
        if await ctx.embed_requested() and not tac.raw:
            embed = discord.Embed(description=message, colour=(await ctx.embed_colour()))
            await ctx.send(embed=embed)
        else:
            await ctx.send(message)
