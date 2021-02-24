import discord

from redbot.core import commands
from redbot.core.utils.chat_formatting import spoiler

class BubbleWrap(commands.Cog):
    """
    Get some bubblewrap.
    """
    
    async def red_delete_data_for_user(self, **kwargs):
        """ Nothing to delete """
        return

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["bubble"])
    async def bubblewrap(self, ctx):
        """
        Get some bubblewrap.
        """
        pre_processed = f"{spoiler('pop')}" * 12
        processed = f"{pre_processed}\n" * 12
        if await ctx.embed_requested():
            embed = discord.Embed(
                title="Bubblewrap!",
                description=processed,
                color=await ctx.embed_colour(),
            )
            return await ctx.send(embed=embed)
        await ctx.send(processed)