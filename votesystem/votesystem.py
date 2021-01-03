import discord
import asyncio
from redbot.core import commands

class VoteSystem(commands.Cog):
    """Vote for and against ideas in a channel."""
    
    
    def __init__(self, bot):
        self.bot = bot
        self.emojis = self.bot.loop.create_task(self.init())

    
    def cog_unload(self):
        if self.emojis:
            self.emojis.cancel()

    
    async def init(self):
        await self.bot.wait_until_ready()
        self.votes = {
            "up": discord.utils.get(self.bot.emojis, id=289154420099252224),
            "down": discord.utils.get(self.bot.emojis, id=289154440412266506),
        }

    
    @commands.command()
    async def startvote(self, ctx, channel: discord.TextChannel):
        """
        Start up and down reactions in a channel.

        
        `channel`: The channel where all messages will have up and down arrows added to.

        """

        await ctx.send(
            f"Started. {self.votes['up']} and {self.votes['down']} emojis will "
            f"be added to each message in {channel.mention}.\nYou can discontinue "
            f"this process by typing `stop()` in {channel.mention}."
        )
        c = channel
        def check(m): return m.author in ctx.guild.members and m.channel == channel
        for i in range(1):
            while True:
                s = await self.bot.wait_for("message", check=check)
                if s.content.lower().startswith("stop()"):
                    await s.delete()
                    await c.send("Stopped.", delete_after=2)
                    break
                else:
                    await s.add_reaction(self.votes['up'])
                    await s.add_reaction(self.votes['down'])

