from redbot.core.bot import Red
from .birthdays import Birthdays


def setup(bot: Red):
    bot.add_cog(Birthdays(bot))