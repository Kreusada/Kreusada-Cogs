from .pingi import PingInvoke, __red_end_user_data_statement__


def setup(bot):
    cog = PingInvoke(bot)
    bot.add_cog(cog)
