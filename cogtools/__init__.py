from redbot.core.bot import Red
from .cogtools import Cogtools

__red_end_user_data_statement__ = (
    "This cog does not persistently store data or metadata about users."
)


def setup(bot: Red):
    cog = Cogtools(bot)
    bot.add_cog(cog)
