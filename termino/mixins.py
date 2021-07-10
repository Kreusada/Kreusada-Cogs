from abc import ABC

from redbot.core import Config, commands
from redbot.core.bot import Red


class MixinMeta(ABC):
    def __init__(self, *nargs):
        self.bot: Red
        self.config: Config


class CompositeMetaClass(type(ABC), type(commands.Cog)):
    pass
