import abc

from redbot.core import Config
from redbot.core.bot import Red


class MixinMeta(abc.ABC):
    def __init__(self, *args):
        self.bot: Red
        self.config: Config
