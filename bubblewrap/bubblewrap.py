import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import spoiler


class BubbleWrap(commands.Cog):
    """
    Get some bubblewrap.

    This will not work if you have spoilers turned
    off in your user settings.
    """

    __author__ = ["Kreusada", ]
    __version__ = "1.0.0"
    
    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad."""
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["bubble"])
    async def bubblewrap(self, ctx):
        """
        Get some bubblewrap.

        This will not work if you have spoilers turned
        off in your user settings.
        """
        pre_processed = f"{spoiler('pop')}" * 7
        processed = f"{pre_processed}\n" * 7
        if await ctx.embed_requested():
            embed = discord.Embed(
                title="Bubblewrap!",
                description=processed,
                color=await ctx.embed_colour(),
            )
            return await ctx.send(embed=embed)
        await ctx.send(processed)