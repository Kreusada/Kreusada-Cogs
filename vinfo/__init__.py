import json
from pathlib import Path

from .vinfo import Vinfo, data_statement

__red_end_user_data_statement__ = data_statement

async def setup(bot):
    cog = Vinfo(bot)
    await cog.initialize()
    bot.add_cog(cog)