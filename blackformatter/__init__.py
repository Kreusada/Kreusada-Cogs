import json
import pathlib

from .black_formatter import __red_end_user_data_statement__, BlackFormatter


def setup(bot):
    cog = BlackFormatter(bot)
    bot.add_cog(cog)
