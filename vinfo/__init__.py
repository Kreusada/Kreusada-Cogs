from .vinfo import Vinfo, __red_end_user_data_statement__


def setup(bot):
    cog = Vinfo(bot)
    bot.add_cog(cog)
