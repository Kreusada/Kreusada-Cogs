from redbot.core import commands

class Drills(commands.Cog):
    """Posts drills"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def drills(self, ctx):
        """Posts drills."""
        await ctx.send("http://i.imgur.com/DewESrv.jpg")
