from abc import ABC

from redbot.core import Config
from redbot.core.bot import Red


class RaffleMixin(ABC):
    """Base class for well behaved type
    hint detection with composite class."""

    def __init__(self, *nargs):
        self.config: Config
        self.bot: Red
