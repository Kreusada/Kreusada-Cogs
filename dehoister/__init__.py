from .dehoister import __red_end_user_data_statement__, Dehoister


def setup(bot):
    cog = Dehoister(bot)
    bot.add_cog(cog)
