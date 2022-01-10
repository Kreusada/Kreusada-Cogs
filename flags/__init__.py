from .flags import __red_end_user_data_statement__, Flags


def setup(bot):
    bot.add_cog(Flags(bot))
