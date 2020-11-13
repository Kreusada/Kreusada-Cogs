from .kreustools import Kreustools


def setup(bot):
    cog = Kreustools(bot)
    bot.add_cog(cog)
