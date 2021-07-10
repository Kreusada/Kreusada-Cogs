import contextlib

import psutil
from redbot.core import commands
from redbot.core.utils.chat_formatting import box


class RAM(commands.Cog):
    """Get [botname]'s ram."""

    __author__ = ["Kreusada"]
    __version__ = "1.0.2"

    def __init__(self, bot):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    def cog_unload(self):
        with contextlib.suppress(Exception):
            self.bot.remove_dev_env_value("ram")

    async def initialize(self) -> None:
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("ram", lambda x: self)

    @commands.command()
    @commands.is_owner()
    async def ram(self, ctx):
        """Get [botname]'s ram."""
        m = psutil.virtual_memory()
        await ctx.send(
            box(
                f"Percentage: [{m.percent}%]\n"
                f"Scaled: [{str(round(m.used / 1024 / 1024))}M/"
                f"{str(round(m.total / 1024 / 1024))}M]",
                lang="apache",
            )
        )
