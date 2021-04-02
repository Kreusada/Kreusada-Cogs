import psutil
from redbot.core import commands
from redbot.core.utils.chat_formatting import box

## Thanks Kagami for the .total addon

class RAM(commands.Cog):
    """Get [botname]'s ram."""

    __author__ = ["Kreusada", ]
    __version__ = "1.0.1"

    def __init__(self, bot):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad."""
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    @commands.command()
    @commands.is_owner()
    async def ram(self, ctx):
        """Get [botname]'s ram."""
        await ctx.send(
            box(
                text = (
                    f"Percentage: [{psutil.virtual_memory().percent}%]\n"
                    f"Scaled: [{str(round(psutil.virtual_memory().used / 1024 / 1024))}M/"
                    f"{str(round(psutil.virtual_memory().total / 1024 / 1024))}M]"
                ),
                lang="apache"
            )
        )
