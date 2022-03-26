import contextlib
import datetime
import json
import pathlib

import dateparser
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.commands import BadArgument, Cog, Context, Converter

with open(pathlib.Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


class DateConverter(Converter):
    """Date converter which uses dateparser.parse()."""

    async def convert(self, ctx: Context, arg: str) -> datetime.datetime:
        parsed = dateparser.parse(arg)
        if parsed is None:
            raise BadArgument("Unrecognized date/time.")
        return parsed


class TimeStamps(Cog):
    """Retrieve timestamps for certain dates."""

    __author__ = "Kreusada"
    __version__ = "1.0.3"

    def __init__(self, bot):
        self.bot: Red = bot
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(RuntimeError, ValueError):
                self.bot.add_dev_env_value(self.__class__.__name__.lower(), lambda x: self)

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    async def cog_unload(self):
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(KeyError):
                await self.bot.remove_dev_env_value(self.__class__.__name__.lower())

    async def red_delete_data_for_user(self, **kwargs):
        """
        Nothing to delete
        """
        return

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
        message = f"Timestamps for **<t:{ts}:F>**\n\n"
        for i in "fdt":
            message += f"`<t:{ts}:{i.upper()}>`: <t:{ts}:{i.upper()}>\n"
            message += f"`<t:{ts}:{i.lower()}>`: <t:{ts}:{i.lower()}>\n"
        message += f"`<t:{ts}:R>`: <t:{ts}:R>\n"
        await ctx.tick()
        await ctx.maybe_send_embed(message)
