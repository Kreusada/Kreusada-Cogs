from abc import ABC

from redbot.core import Config
from redbot.core.bot import Red


class RaffleMixin(ABC):
    """ABC Mixin used to mix the command files together."""

    # Would like to eventually use this mixin to separate raffle.py further
    def __init__(self, *args):
        self.bot: Red
        self.config: Config
