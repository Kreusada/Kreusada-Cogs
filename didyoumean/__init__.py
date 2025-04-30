import discord
import rapidfuzz
import operator

from redbot.core import Config, commands
from redbot.core.bot import Red
from redbot.core.utils import get_end_user_data_statement
from redbot.core.utils.views import ConfirmView

__red_end_user_data_statement__ = get_end_user_data_statement(__file__)

class DidYouMean(commands.Cog):
    """Provides command suggestions for mistyped commands using Levenshtein distance."""

    __version__ = "1.0.0"
    __author__ = "Kreusada"

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, 719988449867989142, force_registration=True)
        self.config.register_global(threshold=70)

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    @commands.group()
    @commands.is_owner()
    async def dymset(self, ctx: commands.Context):
        """Configure DidYouMean."""

    @dymset.command(name="threshold")
    async def dymset_threshold(self, ctx: commands.Context, threshold: commands.Range[int, 50, 80]):
        """Configure the threshold. Must be between 50 and 80."""
        await self.config.threshold.set(threshold)
        self.threshold = threshold
        await ctx.send("Threshold set.")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandNotFound):
            best_match = None
            highest_ratio = 0

            for cmd in map(operator.attrgetter("qualified_name"), self.bot.commands):
                ratio = rapidfuzz.fuzz.ratio(ctx.invoked_with, cmd)
                if ratio > highest_ratio:
                    highest_ratio = ratio
                    best_match = cmd

            if best_match and highest_ratio >= await self.config.threshold():
                view = ConfirmView(ctx.author, timeout=30)
                to_execute = ctx.message.content.replace(ctx.invoked_with, best_match, 1)
                message = f"Could not find a top-level command named `{ctx.invoked_with}`. Perhaps you meant `{best_match}`?" \
                f"\nConfirming will execute `{to_execute}`."
                view.message = await ctx.send(message, view=view, delete_after=30)
                await view.wait()
                if view.result:
                    ctx.message.content = to_execute
                    await self.bot.process_commands(ctx.message)

                try:
                    await view.message.delete()
                except discord.NotFound:
                    pass


async def setup(bot: Red):
    cog = DidYouMean(bot)
    await bot.add_cog(cog)
