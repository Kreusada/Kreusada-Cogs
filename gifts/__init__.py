from .gifts import Gifts

__red_end_user_data_statement__ = (
    "This cog does not persistently store data or metadata about users."
)


def setup(bot):
    cog = Gifts(bot)
    bot.add_cog(cog)
