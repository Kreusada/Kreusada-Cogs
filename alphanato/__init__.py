from .alphanato import AlphaNato, __red_end_user_data_statement__


def setup(bot):
    cog = AlphaNato(bot)
    bot.add_cog(cog)
