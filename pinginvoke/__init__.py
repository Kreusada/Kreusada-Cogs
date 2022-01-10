from .pingi import __red_end_user_data_statement__, PingInvoke


def setup(bot):
    cog = PingInvoke(bot)
    bot.add_cog(cog)
