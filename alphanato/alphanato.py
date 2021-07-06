import contextlib

import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import box

from .alphabet import NATO_ALPHABET

_remove_whitespace = lambda x: x.replace(" ", "")


class AlphaNato(commands.Cog):
    """
    Get the names of the NATO phonetics through easy-to-use syntax.
    """

    __author__ = ["Kreusada"]
    __version__ = "0.3.1"

    def __init__(self, bot):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    async def initialize(self) -> None:
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("alphanato", lambda x: self)

    @commands.command(usage="<letters...>")
    async def nato(self, ctx, *, letter: str):
        """
        Get the nato phonetic name from a letter.

        You may provide multiple letters.
        NOTE: Use `[p]nato all` to get all the NATO phonetics.

        **Example Usage:**
        `[p]nato a, b, c`
        `[p]nato agz`
        `[p]nato z`
        `[p]nato all`

        **Returns:**
        The NATO alphabet name for the provided characters.
        """
        if not letter.isalpha():
            return await ctx.send_help()
        factory = {}
        for x in NATO_ALPHABET:
            if letter.lower().strip() == "all":
                factory[x[0].lower()] = x
            else:
                for let in tuple(_remove_whitespace(letter)):
                    if x[0].lower() == let and let.isalpha():
                        factory[let] = x
        msg = "\n".join("'{}' = {}".format(k, v) for k, v in sorted(factory.items()))
        await ctx.send(box(msg, lang="ml"))
