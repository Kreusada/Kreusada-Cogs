import discord
import asyncio
from redbot.core import commands

class Relax(commands.Cog):
    """Allow yourself to take a break for a specified amount of time."""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["break"])
    async def relax(self, ctx, minutes: int):
        """Take a break..."""
        asynciosleep = minutes * 60
        await ctx.send(f"Okay {ctx.author.name}, I'll remind you that your break is over in {minutes} minutes.")
        await asyncio.sleep(asynciosleep)
        await ctx.author.send(f"Your {minutes} minute break is over!")
