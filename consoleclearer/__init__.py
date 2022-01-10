from .consoleclearer import ConsoleClearer


def setup(bot):
    cog = ConsoleClearer(bot)
    bot.add_cog(cog)
