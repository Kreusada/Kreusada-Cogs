from .alliance import Alliance

__red_end_user_data_statement__ = "This cog does not store user data or metadata."


def setup(bot):
    bot.add_cog(Alliance(bot))
