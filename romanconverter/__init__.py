from .romanconverter import RomanConverter

def setup(bot):
    bot.add_cog(RomanConverter(bot))