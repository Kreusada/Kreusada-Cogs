import contextlib
import datetime

import discord

try:
    import tabulate
except ModuleNotFoundError:
    tabulate = None

from redbot.core import commands
from redbot.core.commands import Cog, Context
from redbot.core.utils.chat_formatting import box, humanize_list
from redbot.core.utils.menus import close_menu, menu

from .converters import CountryConverter
from .functions import format_attr


class Flags(Cog):
    """Get flags from country names."""

    __version__ = "1.0.0"
    __author__ = ["Kreusada"]

    def __init__(self, bot):
        self.bot = bot

    def format_help_for_context(self, ctx: Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = humanize_list(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    def cog_unload(self):
        with contextlib.suppress(Exception):
            self.bot.remove_dev_env_value("flags")

    async def initialize(self) -> None:
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("flags", lambda x: self)

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
        image = argument["image"]
        title = argument["title"]

        del argument["image"]
        del argument["title"]

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
