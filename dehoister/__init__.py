from .dehoister import Dehoister, __red_end_user_data_statement__


def setup(bot):
    cog = Dehoister(bot)
    bot.add_cog(cog)
