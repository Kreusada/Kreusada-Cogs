from redbot.core.utils import get_end_user_data_statement
from .black_formatter import BlackFormatter

__red_end_user_data_statement__ = get_end_user_data_statement(__file__)

async def setup(bot):
    cog = BlackFormatter(bot)
    await bot.add_cog(cog)
