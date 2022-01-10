from .rpsls import RPSLS

def setup(bot):
    cog = RPSLS(bot)
    bot.add_cog(cog)
