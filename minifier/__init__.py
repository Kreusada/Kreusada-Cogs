import json
import pathlib

from .minifier import Minifier


def setup(bot):
    cog = Minifier(bot)
    bot.add_cog(cog)
