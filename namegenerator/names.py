import contextlib
import json
import pathlib

import names
from redbot.core import commands

full = names.get_full_name
first = names.get_first_name
last = names.get_last_name

with open(pathlib.Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


class OptionalKwarg(commands.Converter):
    async def convert(self, ctx: commands.Context, argument):
        return {"gender": argument}


class NameGenerator(commands.Cog):
    """
    Generates random names.
    """

    __author__ = "Kreusada"
    __version__ = "2.0.4"

    def __init__(self, bot):
        self.bot = bot
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value(self.__class__.__name__.lower(), lambda x: self)

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    def cog_unload(self):
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(KeyError):
                self.bot.remove_dev_env_value(self.__class__.__name__.lower())

    @commands.group()
    async def name(self, ctx: commands.Context):
        """Commands for NameGenerator."""

    @name.command()
    async def full(self, ctx: commands.Context, gender: OptionalKwarg = {}):
        """
        Generates a full name.

        Optional arguments:
        `gender`: Provides the gender of the name.
        """
        await ctx.send(full(**gender))

    @name.command()
    async def first(self, ctx: commands.Context, gender: OptionalKwarg = {}):
        """
        Generates a first name.

        Optional arguments:
        `gender`: Provides the gender of the name.
        """
        await ctx.send(first(**gender))

    @name.command()
    async def last(self, ctx: commands.Context, gender: OptionalKwarg = {}):
        """
        Generates a last name.

        Optional arguments:
        `gender`: Provides the gender of the name.
        """
        await ctx.send(last(**gender))

    @name.command(usage="<word1> <word2>")
    async def mash(self, ctx, a: str, b: str):
        """
        Mash two words together.
        """
        await ctx.send(a[: len(a) // 2].strip() + b[len(b) // 2 :].strip())
