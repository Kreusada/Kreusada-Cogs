import datetime
import os

from redbot.core import commands
from redbot.core.bot import Red

class ConsoleClearer(commands.Cog):
    """Clear your console."""

    __author__ = "Kreusada"
    __version__ = "1.2.0"

    def __init__(self, bot: Red):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        return

    @commands.is_owner()
    @commands.command(aliases=["cleanconsole", "consoleclear", "consoleclean"])
    async def clearconsole(self, ctx: commands.Context):
        """
        Completely clears [botname]'s console.
        """
        os.system("clear" if os.name == "posix" else "cls")
        print(f"Red console cleared | {datetime.datetime.utcnow().strftime('%b %d %Y %H:%M:%S')} (UTC)")
        await ctx.send("Red console cleared.")
