import contextlib
import datetime
import json
import pathlib

import discord

try:
    import tabulate
except ModuleNotFoundError:
    tabulate = None

from redbot.core import commands
from redbot.core.commands import Cog, Context
from redbot.core.utils.chat_formatting import box
from redbot.core.utils.menus import close_menu, menu

from .converters import CountryConverter
from .functions import format_attr

with open(pathlib.Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


class Flags(Cog):
    """Get flags from country names."""

    __version__ = "1.1.3"
    __author__ = "Kreusada"

    def __init__(self, bot):
        self.bot = bot
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(RuntimeError, ValueError):
                self.bot.add_dev_env_value(self.__class__.__name__.lower(), lambda x: self)

    def format_help_for_context(self, ctx: Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    def cog_unload(self):
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(KeyError):
                self.bot.remove_dev_env_value(self.__class__.__name__.lower())

    @commands.command()
    async def flag(self, ctx: Context, *, argument: CountryConverter):
        """Get the flag for a country.

        Either the country name or alpha 2 code can be provided.

        **Examples:**

            - ``[p]flag russia``
            - ``[p]flag brazil``
            - ``[p]flag dk``
            - ``[p]flag se``
        """
        description = argument.get("description", None)
        image = argument.pop("image")
        title = argument.pop("title")

        if description is None:
            if tabulate:
                description = box(
                    tabulate.tabulate(
                        [(format_attr(k), v) for k, v in argument.items()], tablefmt="plain"
                    ),
                    lang="ini",
                )
            else:
                description = box(
                    (f"{format_attr(k)}: {v}" for k, v in argument.items()), lang="yaml"
                )

        embed = discord.Embed(
            title=title,
            description=description,
            color=await ctx.embed_colour(),
            timestamp=datetime.datetime.now(),
        )

        embed.set_image(url=image)
        await menu(ctx, [embed], {"\N{CROSS MARK}": close_menu})
