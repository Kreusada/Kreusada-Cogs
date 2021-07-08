import contextlib

from redbot.core import commands

from .converters import AlphaConverter


class AlphaNato(commands.Cog):
    """
    Get the names of the NATO phonetics through easy-to-use syntax.
    """

    __author__ = ["Kreusada"]
    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot
        self.bot_add_dev_env_value("alphanato", lambda x: self)

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
    async def nato(self, ctx, *, letters: AlphaConverter):
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
        # Oh boy, I love converters :P
        await ctx.send(letters)
