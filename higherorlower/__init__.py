from .core import HigherOrLower as COG

def setup(bot):
    bot.add_cog(COG(bot))