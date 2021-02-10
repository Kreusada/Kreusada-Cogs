import roman
from redbot.core import commands

class RomanConverter(commands.Cog):
    """
    Convert to roman numerals.
    """

    def __init__(self, bot):
        self.bot = bot
        self.out_of_range = "`{number}` is out of range. It must be between 1, and 4999."

    @commands.group()
    async def roman(self, ctx, number: int):
        """
        Convert a number to a roman numeral.

        `<number>` must be between 1, and 4999.
        """
        try:
            await ctx.send(roman.toRoman(number))
        except roman.OutOfRangeError:
            return await ctx.send(self.out_of_range.format(number=number))