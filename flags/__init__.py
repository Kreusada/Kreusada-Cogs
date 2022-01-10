from .flags import Flags, __red_end_user_data_statement__


def setup(bot):
    bot.add_cog(Flags(bot))
