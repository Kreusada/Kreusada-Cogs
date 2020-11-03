from .collectables import Collectables


def setup(bot):
    cog = Collectables(bot)
    bot.add_cog(cog)
