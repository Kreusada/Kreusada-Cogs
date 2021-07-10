import discord
from redbot.core import commands

from .enums import PingOverrideVariables


class PingObject(object):
    """Superclass for objects."""

    def __getattr__(self, arg):
        raise commands.BadArgument(arg)


class Member(PingObject):
    """SafeMember object for formatting."""

    def __init__(self, member: discord.Member):
        for attr in PingOverrideVariables:
            if attr.name.lower() == "latency":
                continue
            setattr(self, attr.name.lower(), attr.value[0](member))

    def __str__(self):
        return self.name_and_discriminator
