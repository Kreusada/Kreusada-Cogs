from names import get_full_name as full, get_first_name as first, get_last_name as last
from redbot.core import commands

class NameGenerator(commands.Cog):
    """Generates random names."""

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def name(self, ctx):
        """Commands for NameGenerator."""

    @name.command()
    async def full(self, ctx, gender: str = None):
        """
        Generates a full name.
        
        Optional arguments:
        `gender`: Provides the gender of the name.
        """
        if gender is not None:
            await ctx.send(full(gender=gender))
        else:
            await ctx.send(full())

    @name.command()
    async def first(self, ctx, gender: str = None):
        """
        Generates a first name.
        
        Optional arguments:
        `gender`: Provides the gender of the name.
        """
        if gender is not None:
            await ctx.send(first(gender=gender))
        else:
            await ctx.send(first())

    @name.command()
    async def last(self, ctx, gender: str = None):
        """
        Generates a last name.
        
        Optional arguments:
        `gender`: Provides the gender of the name.
        """
        if gender is not None:
            await ctx.send(last(gender=gender))
        else:
            await ctx.send(last())
