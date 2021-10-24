import contextlib
import datetime
import json
import pathlib

import dateparser
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.commands import BadArgument, Cog, Context, Converter
from redbot.core.utils.chat_formatting import humanize_list

with open(pathlib.Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


class DateConverter(Converter):
    """Date converter which uses dateparser.parse()."""

    async def convert(self, ctx: Context, arg: str) -> datetime.datetime:
        parsed = dateparser.parse(arg)
        if parsed is None:
            raise BadArgument("Unrecognized date/time.")
        return parsed

    @staticmethod
    def get_superscript(number: int) -> str:
        suffixes = {0: "th", 1: "st", 2: "nd", 3: "rd"}
        for i in range(4, 10):
            suffixes[i] = "th"
        return str(number) + suffixes[int(str(number)[-1])]


class TimeStamps(Cog):
    """Retrieve timestamps for certain dates."""

    __author__ = ["Kreusada"]
    __version__ = "1.0.1"

    def __init__(self, bot):
        self.bot: Red = bot
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(RuntimeError, ValueError):
                self.bot.add_dev_env_value(self.__class__.__name__.lower(), lambda x: self)

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = humanize_list(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    def cog_unload(self):
        with contextlib.suppress(KeyError):
            self.bot.remove_dev_env_value(self.__class__.__name__.lower())

    @commands.command(usage="<date_or_time>")
    async def timestamp(self, ctx: Context, *, dti: DateConverter):
        """Produce a Discord timestamp.

        Timestamps are a feature added to Discord in the summer of 2021,
        which allows you to send timestamps will which update accordingly
        with any user's date time settings.

        **Example Usage**

        - `[p]timestamp 1st of october, 2021`
        - `[p]timestamp 20 hours ago`
        - `[p]timestamp in 50 minutes`
        - `[p]timestamp 01/10/2021`
        - `[p]timestamp now`
        """
        ts = int(dti.timestamp())
        superscript = DateConverter.get_superscript(int(dti.strftime("%d").lstrip("0")))
        message = f"Timestamps for **<t:{ts}:F>**\n\n"
        for i in "fdt":
            message += f"`<t:{ts}:{i.upper()}>`: <t:{ts}:{i.upper()}>\n"
            message += f"`<t:{ts}:{i.lower()}>`: <t:{ts}:{i.lower()}>\n"
        message += f"`<t:{ts}:R>`: <t:{ts}:R>\n"
        await ctx.tick()
        await ctx.maybe_send_embed(message)
