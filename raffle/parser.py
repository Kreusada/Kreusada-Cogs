import discord

from redbot.core.commands import BadArgument, Context

from .log import log
from .safety import RaffleSafeMember
from .checks import server_join_age_checker, account_age_checker, now

from .exceptions import (
    RequiredKeyError, 
    UnknownEntityError, 
    RaffleSyntaxError, 
    UnidentifiedKeyError,
    RaffleDeprecationWarning
)

from .enums import RaffleComponents


class RaffleManager(object):
    """Parses the required and relevant yaml data to ensure
    that it matches the specified requirements."""

    def __init__(self, data):
        super().__init__()
        self.data = data
        self.name = data.get("name", None)
        self.description = data.get("description", None)
        self.account_age = data.get("account_age", None)
        self.server_join_age = data.get("server_join_age", None)
        self.maximum_entries = data.get("maximum_entries", None)
        self.roles_needed_to_enter = data.get("roles_needed_to_enter", None) 
        self.prevented_users = data.get("prevented_users", None)
        self.allowed_users = data.get("allowed_users", None)
        self.join_message = data.get("join_message", None)
        self.end_message = data.get("end_message", None)
        self.on_end_action = data.get("on_end_action", None)

        # dep warnings come first
        if "join_age" in self.data.keys():
            raise RaffleDeprecationWarning("\"join_age\" has been deprecated in favour of \"server_join_age\". Please use this condition instead.")

        # now if something isn't recognised
        for key in self.data.keys():
            if not key in [x.name for x in RaffleComponents]:
                raise UnidentifiedKeyError(f"\"{key}\" is not a documented condition/block")

    @classmethod
    def shorten_description(cls, description, length=50):
        if len(description) > length:
            return description[:length].rstrip() + '...'
        return description

    @classmethod
    def parse_accage(cls, accage: int):
        if not account_age_checker(accage):
            raise BadArgument("Days must be less than Discord's creation date")

    @classmethod
    def parse_serverjoinage(cls, ctx: Context, new_join_age: int):
        guildage = (now - ctx.guild.created_at).days
        if not server_join_age_checker(ctx, new_join_age):
            raise BadArgument(
                "Days must be less than this guild's creation date ({} days)".format(
                    guildage
                )
            )

    def parser(self, ctx: Context):
        if self.account_age:
            if not isinstance(self.account_age, int):
                raise BadArgument("(account_age) days must be a number")
            if not account_age_checker(self.account_age):
                raise BadArgument("(account_age) days must be less than Discord's creation date")


        if self.server_join_age:
            if not isinstance(self.server_join_age, int):
                raise BadArgument("(server_join_age) days must be a number")
            if not server_join_age_checker(ctx, self.server_join_age):
                raise BadArgument("(server_join_age) days must be less than this servers's creation date")


        if self.maximum_entries:
            if not isinstance(self.maximum_entries, int):
                raise BadArgument("(maximum_entries) Maximum entries must be a number")


        if self.name:
            if not isinstance(self.name, str):
                raise BadArgument("(name) Name must be in quotation marks")
            if len(self.name) > 25:
                raise BadArgument("(name) Name must be under 25 characters, your raffle name had {}".format(len(self.name)))
            for char in self.name:
                if char == "_":
                    # We want to allow underscores
                    continue
                if not char.isalnum():
                    index = self.name.index(char)
                    marker = (
                        f"{self.name}\n{' ' * (index)}^\n"
                        f"Characters must be alphanumeric or underscores, not \"{char}\""
                    )
                    raise RaffleSyntaxError(f"In \"name\" field, character {index+1}\n\n{marker}")
        else:
            raise RequiredKeyError("name")


        if self.description:
            if not isinstance(self.description, str):
                raise BadArgument("(description) Description must be in quotation marks")


        if self.roles_needed_to_enter:
            if not isinstance(self.roles_needed_to_enter, list):
                raise BadArgument("(roles_needed_to_enter) Roles must be a list of Discord role IDs")
            for r in self.roles_needed_to_enter:
                if not ctx.guild.get_role(r):
                    raise UnknownEntityError(r, "role")


        if self.prevented_users:
            if not isinstance(self.prevented_users, list):
                raise BadArgument("(prevented_users) Prevented users must be a list of Discord user IDs")
            for u in self.prevented_users:
                if not ctx.bot.get_user(u):
                    raise UnknownEntityError(u, "user")

        if self.allowed_users:
            if not isinstance(self.allowed_users, list):
                raise BadArgument("(allowed_users) Allowed users must be a list of Discord user IDs")
            for u in self.allowed_users:
                if not ctx.bot.get_user(u):
                    raise UnknownEntityError(u, "user")

        if self.end_message:
            if not isinstance(self.end_message, (list, str)):
                raise BadArgument("(end_message) End message must be in quotation marks, by itself or inside a list")
            kwargs = {
                "winner": RaffleSafeMember(discord.Member, "winner"),
                "raffle": r"{raffle}",
            }
            if isinstance(self.end_message, str):
                try:
                    # This will raise BadArgument
                    self.end_message.format(**kwargs)
                except KeyError as e:
                    raise BadArgument(f"(end_message) {e} was an unexpected argument")
            else:
                for m in self.end_message:
                    try:
                        m.format(**kwargs)
                    except KeyError as e:
                        raise BadArgument(f"(end_message) {e} was an unexpected argument")

        if self.join_message:
            if not isinstance(self.join_message, (list, str)):
                raise BadArgument("(join_message) Join message must be in quotation marks, by itself or inside a list")
            kwargs = {
                "user": RaffleSafeMember(discord.Member, "user"),
                "raffle": r"{raffle}",
                "entry_count": r"{entry_count}"
            }
            if isinstance(self.join_message, str):
                try:
                    self.join_message.format(**kwargs)
                except KeyError as e:
                    raise BadArgument(f"(join_message) {e} was an unexpected argument")
            else:
                for m in self.join_message:
                    try:
                        m.format(**kwargs)
                    except KeyError as e:
                        raise BadArgument(f"(join_message) {e} was an unexpected argument")


        if self.on_end_action:
            valid_actions = ("end", "remove_winner", "keep_winner")
            if not isinstance(self.on_end_action, str) or self.on_end_action not in valid_actions:
                raise BadArgument("(on_end_action) must be one of 'end', 'remove_winner', or 'keep_winner'")