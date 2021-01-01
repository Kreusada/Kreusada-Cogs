import discord
from redbot.core import commands

class RomanConverter(commands.Cog):
    """Convert integers to roman numerals."""

    def __init__(self, bot):
        self.bot = bot

    async def roman(self, number):
        val = [
            1000, 900, 500, 400,
            100, 90, 50, 40,
            10, 9, 5, 4,
            1
            ]
        syb = [
            "M", "CM", "D", "CD",
            "C", "XC", "L", "XL",
            "X", "IX", "V", "IV",
            "I"
            ]
        output = ''
        i = 0
        while number > 0:
            for _ in range(number // val[i]):
                output += syb[i]
                number -= val[i]
            i += 1
        return output

    async def number(self, roman_numeral):
        rom_val = {'I': 1, 'i': 1, 'V': 5, 'v': 5, 'X': 10, 'x': 10, 'L': 50, 'l': 50, 'C': 100, 'c': 100, 'D': 500, 'd': 500, 'M': 1000, 'm': 1000}
        output = 0
        rn = roman_numeral
        for i in range(len(rn)):
            try:
                if i > 0 and rom_val[rn[i]] > rom_val[rn[i - 1]]:
                    output += rom_val[rn[i]] - 2 * rom_val[rn[i - 1]]
                else:
                    output += rom_val[rn[i]]
            except KeyError:
                msg = "That doesn't look like roman numerals."
                return msg
        return output

    @commands.command()
    async def romanize(self, ctx, number: int):
        """
        Attempts to convert a number to a roman numeral.
        Results may become unprecedented above 10,000.
        """
        output = await self.roman(number)
        try:
            await ctx.send(output)
        except discord.HTTPException:
            await ctx.send("This numeral i've generated exceeds the 2000 character limit!")
    
    @commands.command()
    async def numberize(self, ctx, roman_numeral: str):
        """
        Attempts to convert a roman numeral to a number.
        Results may become unprecedented above 10,000.
        """
        output = await self.number(roman_numeral)
        await ctx.send(output)
