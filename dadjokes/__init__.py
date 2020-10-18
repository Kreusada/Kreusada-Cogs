from .dadjokes import DadJokes


def setup(bot):
    cog = DadJokes(bot)
    bot.add_cog(cog)
