from redbot.core.utils import get_end_user_data_statement
from redbot.core.bot import Red
from .black_formatter import BlackFormatter

__red_end_user_data_statement__ = get_end_user_data_statement(__file__)

async def setup(bot: Red):
    await bot.add_cog(BlackFormatter(bot))
