from .names import NameGenerator


def setup(bot):
    cog = NameGenerator(bot)
    bot.add_cog(cog)
