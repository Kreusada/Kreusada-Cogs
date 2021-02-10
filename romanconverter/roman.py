import roman
from redbot.core import commands

class RomanConverter(commands.Cog):
    """
    Convert roman numerals to numbers and vise versa.
    """

    def __init__(self, bot):
        self.bot = bot
        self.invalid = "Invalid Roman numeral: `{roman_numeral}`"
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

    @commands.command()
    async def number(self, ctx, roman_numeral: str):
        """Convert a number to a roman numeral."""
        try:
            await ctx.send(roman.fromRoman(roman_numeral))
        except roman.InvalidRomanNumeralError:
            return await ctx.send(self.invalid.format(roman_numeral=roman_numeral))
