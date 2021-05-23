import json
from pathlib import Path

from .dehoister import Dehoister

with open(Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


async def setup(bot):
    cog = Dehoister(bot)
    await cog.initialize()
    bot.add_cog(cog)
