import discord

from redbot.core.commands import BadArgument

class RaffleSafeMember(object):
    """Used for formatting `discord.Member` attributes safely."""

    def __init__(self, member: discord.Member):
        self.name = member.name
        self.mention = member.mention
        self.id = member.id
        self.display_name = member.display_name
        self.discriminator = member.discriminator
        self.name_and_descriminator = f"{self.name}#{self.discriminator}"

    def __str__(self):
        return self.name

    def __getattr__(self, *_args):
        raise BadArgument(r"Your `{winner}` received an unexpected attribute")