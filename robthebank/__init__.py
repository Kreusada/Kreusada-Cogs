from redbot.core.bot import Red
from .robthebank import RobTheBank

__red_end_user_data_statement__ = (
    "This cog does not persistently store data or metadata about users."
)


def setup(bot: Red):
    cog = RobTheBank(bot)
    bot.add_cog(cog)
