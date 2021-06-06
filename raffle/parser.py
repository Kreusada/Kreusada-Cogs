import discord

from redbot.core.commands import BadArgument, Context

from .safety import RaffleSafeMember
from .exceptions import RequiredKeyError, UnknownEntityError
from .checks import join_age_checker, account_age_checker, now


class RaffleManager(object):
    """Parses the required and relevant yaml data to ensure
    that it matches the specified requirements."""

    def __init__(self, data):
        super().__init__()
        self.data = data
        self.name = data.get("name", None)
        self.description = data.get("description", None)
        self.account_age = data.get("account_age", None)
        self.join_age = data.get("join_age", None)
        self.maximum_entries = data.get("maximum_entries", None)
        self.roles_needed_to_enter = data.get("roles_needed_to_enter", None) 
        self.prevented_users = data.get("prevented_users", None)
        self.allowed_users = data.get("allowed_users", None)
        self.end_message = data.get("end_message", None)
        self.on_draw_action = data.get("on_draw_action", None)

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
    def parse_joinage(cls, ctx: Context, new_join_age: int):
        guildage = (now - ctx.guild.created_at).days
        if not join_age_checker(ctx, new_join_age):
            raise BadArgument(
                "Days must be less than this guild's creation date ({} days)".format(
                    guildage
                )
            )

    def parser(self, ctx: Context):
        if self.account_age:
            if not isinstance(self.account_age, int):
                raise BadArgument("Account age days must be int, not {}".format(type(self.account_age).__name__))
            if not account_age_checker(self.account_age):
                raise BadArgument("Account age days must be less than Discord's creation date")


        if self.join_age:
            if not isinstance(self.join_age, int):
                raise BadArgument("Join age days must be int, not {}".format(type(self.join_age).__name__))
            if not join_age_checker(ctx, self.join_age):
                raise BadArgument("Join age days must be less than this guild's creation date")


        if self.maximum_entries:
            if not isinstance(self.maximum_entries, int):
                raise BadArgument("Maximum entries must be int, not {}".format(type(self.maximum_entries).__name__))


        if self.name:
            if not isinstance(self.name, str):
                raise BadArgument("Name must be str, not {}".format(type(self.name).__name__))
            if len(self.name) > 15:
                raise BadArgument("Name must be under 15 characters, your raffle name had {}".format(len(self.name)))
            for char in self.name:
                if char == "_":
                    # We want to allow underscores
                    continue
                if not char.isalnum():
                    index = self.name.index(char)
                    marker = f"{self.name}\n{' ' * (index+19)}^"
                    raise BadArgument(
                        "Name must only contain alphanumeric characters, "
                        "found {}.\nInvalid character: {}".format(char, marker)
                    )
        else:
            raise RequiredKeyError("name")


        if self.description:
            if not isinstance(self.description, str):
                raise BadArgument("Description must be str, not {}".format(type(self.description).__name__))


        if self.roles_needed_to_enter:
            if not isinstance(self.roles_needed_to_enter, list):
                raise BadArgument("Roles must be a list of Discord role IDs, not {}".format(type(self.roles_needed_to_enter).__name__))
            for r in self.roles_needed_to_enter:
                if not ctx.guild.get_role(r):
                    raise UnknownEntityError(r, "role")


        if self.prevented_users:
            if not isinstance(self.prevented_users, list):
                raise BadArgument("Prevented users must be a list of Discord user IDs, not {}".format(type(self.prevented_users).__name__))
            for u in self.prevented_users:
                if not ctx.bot.get_user(u):
                    raise UnknownEntityError(u, "user")

        if self.allowed_users:
            if not isinstance(self.allowed_users, list):
                raise BadArgument("Allowed users must be a list of Discord user IDs, not {}".format(type(self.allowed_users).__name__))
            for u in self.allowed_users:
                if not ctx.bot.get_user(u):
                    raise UnknownEntityError(u, "user")

        if self.end_message:
            if not isinstance(self.end_message, str):
                # Will render {} without quotes, best not to include the type.__name__ here
                raise BadArgument("End message must be str")
            try:
                # This will raise BadArgument
                self.end_message.format(winner=RaffleSafeMember(discord.Member), raffle=r"{raffle}")
            except KeyError as e:
                raise BadArgument(f"{e} was an unexpected argument in your end_message block")

        if self.on_draw_action:
            valid_actions = ("end", "remove_winner", "keep_winner")
            if not isinstance(self.on_draw_action, str) or self.on_draw_action not in valid_actions:
                raise BadArgument("on_draw_action must be one of 'end', 'remove_winner', or 'keep_winner'")