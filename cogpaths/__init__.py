from .cogpaths import CogPaths, __red_end_user_data_statement__


def setup(bot):
    cog = CogPaths(bot)
    bot.add_cog(cog)
