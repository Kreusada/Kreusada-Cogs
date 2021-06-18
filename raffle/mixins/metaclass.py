from abc import ABC
from redbot.core.commands import Cog

class MetaClass(type(Cog), type(ABC)):
    """Composite meta class for Raffle."""
    pass
