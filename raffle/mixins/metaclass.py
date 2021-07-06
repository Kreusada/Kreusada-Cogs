from abc import ABC

from redbot.core.commands import Cog


class MetaClass(type(ABC), type(Cog)):
    pass
