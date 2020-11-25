from redbot.core.bot import Red
from .alliance import Alliance

__red_end_user_data_statement__ = (
    "This cog does not persistently store data or metadata about users."
)


def setup(bot: Red):
    cog = Alliance(bot)
    bot.add_cog(cog)
