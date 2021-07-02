import discord

from redbot.core import commands
from redbot.core.bot import Red
from .enums import PingOverrideVariables


class PingObject(object):
    """Superclass for objects."""

    def __getattr__(self, arg):
        raise commands.BadArgument(arg)


class Latency(PingObject):
    """Formats latency variables."""

    def __init__(self, latency: Red):
        self.bot = round(latency.latency * 1000, 2)

    def __str__(self):
        return self.bot

    def __getattr__(self, arg):
        return super().__getattr__(arg)


class Member(PingObject):
    """SafeMember object for formatting."""

    def __init__(self, member: discord.Member):
        for attr in PingOverrideVariables:
            setattr(self, attr.name.lower(), attr.value[1](member))

    def __str__(self):
        return self.name_and_discriminator

    def __getattr__(self, arg):
        return super().__getattr__(arg)