import json
import pathlib

from .black_formatter import BlackFormatter

with open(pathlib.Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


def setup(bot):
    cog = BlackFormatter(bot)
    bot.add_cog(cog)
