from .demevents import Demevents


def setup(bot):
    cog = Demevents(bot)
    bot.add_cog(cog)
