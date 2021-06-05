import asyncio
import contextlib
import datetime
import enum
import json
import logging
import pathlib
import random

import discord
import yaml

from typing import List, Literal, Optional, Union

from redbot.core import commands, Config
from redbot.core.commands import BadArgument, Context
from redbot.core.utils.predicates import MessagePredicate, ReactionPredicate
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS, close_menu, start_adding_reactions

from redbot.core.utils.chat_formatting import (
    box,
    inline,
    italics, 
    humanize_list, 
    humanize_number,
    pagify
)

from yaml.parser import (
    ParserError as YAMLParserError,
    ScannerError as YAMLScannerError,
    MarkedYAMLError as YAMLMarkedError
)

with open(pathlib.Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]

now = datetime.datetime.now()
discord_creation_date = datetime.datetime(2015, 5, 13)

account_age_checker = lambda x: x < (now - discord_creation_date).days
join_age_checker = lambda ctx, x: x < (now - ctx.guild.created_at).days

log = logging.getLogger("red.kreusada.raffle")


class RaffleError(Exception):
    """Base exception for all raffle exceptions.
    
    These exceptions are raised, but then formatted
    in an except block to create a user-friendly
    error in which the user can read and improve from."""
    pass


class RequiredKeyError(RaffleError):
    """Raised when a raffle key is required."""

    def __init__(self, key):
        self.key = key

    def __str__(self):
        return f"The \"{self.key}\" key is required"


class UnknownEntityError(RaffleError):
    """Raised when an invalid role or user is provided to the parser."""

    def __init__(self, data, _type: Literal["user", "role"]):
        self.data = data
        self.type = _type

    def __str__(self):
        return f"\"{self.data}\" was not a valid {self.type}"

class RaffleSafeMember(object):
    """Used for formatting `discord.Member` attributes safely.
    
    Special thanks to Flame and Kenny for providing this. I
    have modified the original slightly, which you can find here:

    https://github.com/kennnyshiwa/kennnyshiwa-cogs/blob/
    5a84d60018468e5c0346f7ee74b2b4650a6dade7/tickets/core.py#L7
    """

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


class RaffleComponents(enum.Enum):
    """All of the components which can be
    used in a raffle. This class is mainly
    used for the ``[p]raffle conditions`` command.
    """

    name = (
        str, 
        "The name of the raffle. This is the only REQUIRED field."
    )

    description = (
        str, 
        "The description for the raffle. This information appears in the raffle info command."
    )

    end_message = (
        str,
        "The message used to end the raffle. Defaults to \"Congratulations {winner.mention}, you have won the {raffle} raffle!\""
    )

    account_age = (
        int, 
        "The account age requirement for the user who joins the raffle. This must be specified in days."
    )

    join_age = (
        int, 
        "The number of days the user needs to be in the server for in order to join the raffle."
    )

    roles_needed_to_enter = (
        list, 
        "A list of discord roles which the user must have in order to join the raffle. These MUST be specified using IDs."
    )

    prevented_users = (
        list, 
        "A list of discord users who are not allowed to join the raffle. These MUST be specified using IDs."
    )

    allowed_users = (
        list,
        "A list of discord users who are allowed to join the raffle. If this condition exists, no one will be able to join apart from those in the list."
    )

    maximum_entries = (
        int, 
        "The maximum number of entries allowed for a raffle."
    )


class Raffle(commands.Cog):
    """Create raffles for your server."""

    __author__ = ["Kreusada"]
    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 583475034985340, force_registration=True)
        self.config.register_guild(raffles={})
        self.docs = "https://kreusadacogs.readthedocs.io/en/latest/cog_raffle.html"

    @staticmethod
    def format_traceback(exc) -> str:
        boxit = lambda x, y: box(f"{x}: {y}", lang="yaml")
        return boxit(exc.__class__.__name__, exc)

    @staticmethod
    def cleanup_code(content) -> str:
        # From redbot.core.dev_commands, thanks will :P
        if content.startswith("```") and content.endswith("```"):
            return "\n".join(content.split("\n")[1:-1])
        return content.strip("` \n")

    @staticmethod
    def validator(data) -> Union[bool, dict]:
        try:
            loader = yaml.full_load(data)
        except (YAMLParserError, YAMLScannerError, YAMLMarkedError):
            return False
        if not isinstance(loader, dict):
            return False
        return loader

    async def replenish_cache(self, ctx: Context) -> None:
        async with self.config.guild(ctx.guild).raffles() as r:

            for v in list(r.values()):

                getter = v.get("entries")
                for userid in getter:
                    if not self.bot.get_user(userid):
                        getter.remove(userid)

                getter = v.get("prevented_users", None)
                if getter:
                    for userid in getter:
                        if not ctx.guild.get_member(userid):
                            getter.remove(userid)

                getter = v.get("roles_needed_to_enter", None)
                if getter:
                    for roleid in getter:
                        if not ctx.guild.get_role(roleid):
                            getter.remove(roleid)

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = humanize_list(self.__author__)
        fmtlink = lambda x, y: f"[{x}]({y})"
        docnote = f"Please consider reading the {fmtlink('docs', self.docs)} if you haven't already.\n\n"
        return f"{context}\n\n{docnote}Author: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    def cog_unload(self):
        with contextlib.suppress(Exception):
            self.bot.remove_dev_env_value("raffle")

    async def initialize(self) -> None:
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("raffle", lambda x: self)

    async def cog_check(self, ctx: commands.Context):
        return ctx.guild is not None

    async def compose_menu(self, ctx, embed_pages: List[discord.Embed]):
        if len(embed_pages) == 1:
            control = {"\N{CROSS MARK}": close_menu}
        else:
            control = DEFAULT_CONTROLS
        return await menu(ctx, embed_pages, control)

    async def raffle_safe_member_scanner(self, ctx: commands.Context, content: str) -> None:
        """We need this to check if the values are formatted properly."""
        try:
            # This can raise BadArgument, that's fine
            content.format(winner=RaffleSafeMember(discord.Member), raffle=r"{raffle}")
        except KeyError as e:
            raise BadArgument(f"{e} was an unexpected argument in your new end message")

    @commands.group()
    async def raffle(self, ctx: Context):
        """Manage raffles for your server."""

    @raffle.command()
    async def version(self, ctx: Context):
        """Get the version of your Raffle cog."""
        await ctx.send(inline(self.__version__))

    @raffle.group()
    async def create(self, ctx: Context):
        """Create a raffle."""
        pass

    @create.command(name="complex")
    async def _complex(self, ctx: Context):
        """Create a raffle with complex conditions."""
        await ctx.trigger_typing()
        check = lambda x: x.author == ctx.author and x.channel == ctx.channel
        message = await ctx.send(
            "You're about to create a new raffle.\n"
            "Please consider reading the docs about the various "
            "conditional blocks if you haven't already.\n\n"
            + self.docs
        )


        try:
            content = await self.bot.wait_for("message", timeout=500, check=check)
        except asyncio.TimeoutError:
            with contextlib.suppress(discord.NotFound):
                await message.delete()


        content = content.content
        valid = self.validator(self.cleanup_code(content))

        if not valid:
            return await ctx.send("Please provide valid YAML.")

        try:
            parser = RaffleManager(valid)
            parser.parser(ctx)
        except (RaffleError, BadArgument) as e:
            exc = "An exception occured whilst parsing your data."
            return await ctx.send(exc + self.format_traceback(e))


        async with self.config.guild(ctx.guild).raffles() as raffle:

            rafflename = valid.get("name").lower()

            if rafflename in [x.lower() for x in raffle.keys()]:
                return await ctx.send("A raffle with this name already exists.")

            data = {
                "entries": [],
                "owner": ctx.author.id,
            }

            conditions = {
                "end_message": valid.get("end_message", None),
                "account_age": valid.get("account_age", None),
                "join_age": valid.get("join_age", None),
                "roles_needed_to_enter": valid.get("roles_needed_to_enter", None),
                "prevented_users": valid.get("prevented_users", None),
                "allowed_users": valid.get("allowed_users", None),
                "description": valid.get("description", None),
                "maximum_entries": valid.get("maximum_entries", None)
            }

            for k, v in conditions.items():
                if v:
                    data[k] = v

            raffle[rafflename] = data
            await ctx.send("Raffle created.")

        await self.replenish_cache(ctx)

    @create.command()
    async def simple(self, ctx, raffle_name: str, *, description: Optional[str] = None):
        """Create a simple arguments with just a name and description."""
        raffle_name = raffle_name.lower()
        async with self.config.guild(ctx.guild).raffles() as raffle:

            if raffle_name in [x.lower() for x in raffle.keys()]:
                return await ctx.send("A raffle with this name already exists.")

            data = {
                "entries": [],
                "owner": ctx.author.id,
            }

            if description:
                data["description"] = description

            raffle[raffle_name] = data
            await ctx.send(f"Raffle created. You can always add complex conditions with `{ctx.clean_prefix}raffle edit` if you wish.")

    @raffle.command()
    async def join(self, ctx: Context, raffle: str):
        """Join a raffle."""
        r = await self.config.guild(ctx.guild).raffles()
        raffle_data = r.get(raffle, None)

        if not raffle_data:
            return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))


        raffle_entities = lambda x: raffle_data.get(x, None)


        if ctx.author.id in raffle_entities("entries"):
            return await ctx.send("You are already in this raffle.")


        if raffle_entities("prevented_users") and ctx.author.id in raffle_entities("prevented_users"):
            return await ctx.send("You are not allowed to join this particular raffle.")


        if raffle_entities("allowed_users") and ctx.author.id not in raffle_entities("allowed_users"):
            return await ctx.send("You are not allowed to join this particular raffle")


        if ctx.author.id == raffle_entities("owner"):
            return await ctx.send("You cannot join your own raffle.")


        if raffle_entities("maximum_entries") and len(raffle_entities("entries")) > raffle_entities("maximum_entries"):
            return await ctx.send("Sorry, the maximum number of users have entered this raffle.")


        if raffle_entities("roles_needed_to_enter"):
            for r in raffle_entities("roles_needed_to_enter"):
                if not r in [x.id for x in ctx.author.roles]:
                    return await ctx.send("You are missing a required role: {}".format(ctx.guild.get_role(r).mention))


        if raffle_entities("account_age") and raffle_entities("account_age") > (now - ctx.author.created_at).days:
                return await ctx.send("Your account must be at least {} days old to join.".format(raffle_entities("account_age")))


        async with self.config.guild(ctx.guild).raffles() as r:
            raffle_entities = lambda x: r[raffle].get(x, None)
            raffle_entities("entries").append(ctx.author.id)


        await ctx.send(f"{ctx.author.mention} you have been added to the raffle.")
        await self.replenish_cache(ctx)

    @raffle.command()
    async def leave(self, ctx: Context, raffle: str):
        """Leave a raffle."""
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))

            raffle_entries = raffle_data.get("entries")

            if not ctx.author.id in raffle_entries:
                return await ctx.send("You are not entered into this raffle.")

            raffle_entries.remove(ctx.author.id)
            await ctx.send(f"{ctx.author.mention} you have been removed from the raffle.")

        await self.replenish_cache(ctx)

    @raffle.command()
    async def mention(self, ctx: Context, raffle: str):
        """Mention all the users entered into a raffle."""
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))

            raffle_entities = lambda x: raffle_data.get(x)

            if not ctx.author.id == raffle_entities("owner"):
                return await ctx.send("You are not the owner of this raffle.")

            if not raffle_entities("entries"):
                return await ctx.send("There are no entries yet for this raffle.")

            for page in pagify(humanize_list([self.bot.get_user(u).mention for u in raffle_entities("entries")])):
                await ctx.send(page)

        await self.replenish_cache(ctx)

    @raffle.command()
    async def end(self, ctx: Context, raffle: str):
        """End a raffle."""
        msg = await ctx.send(f"Ending the `{raffle}` raffle...")
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))

            raffle_owner = raffle_data.get("owner")
            
            if not ctx.author.id == raffle_owner:
                return await ctx.send("You are not the owner of this raffle.")

            r.pop(raffle)

        await asyncio.sleep(1)
        with contextlib.suppress(discord.NotFound):
            await msg.edit(content="Raffle ended.")

        await self.replenish_cache(ctx)
    
    @raffle.command()
    async def kick(self, ctx: Context, raffle: str, member: discord.Member):
        """Kick a user from your raffle."""
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))

            raffle_entities = lambda x: raffle_data.get(x)

            if not ctx.author.id == raffle_entities("owner"):
                return await ctx.send("You are not the owner of this raffle.")

            if member.id not in raffle_entities("entries"):
                return await ctx.send("This user has not entered this raffle.")

            raffle_entities("entries").remove(member.id)
            await ctx.send("User removed from the raffle.")

        await self.replenish_cache(ctx)
        
    @raffle.command(name="list")
    async def _list(self, ctx: Context):
        """List the currently ongoing raffles."""
        r = await self.config.guild(ctx.guild).raffles()

        if not r:
            return await ctx.send("There are no ongoing raffles.")

        lines = []
        for k, v in sorted(r.items()):
            description = v.get("description", None)
            if not description:
                description=""
            lines.append("**{}** {}".format(k, RaffleManager.shorten_description(description)))

        embeds = []
        data = list(pagify("\n".join(lines), page_length=1024))

        for index, page in enumerate(data, 1):
            embed = discord.Embed(
                title="Current raffles",
                description=page,
                color=await ctx.embed_colour()
            )
            embed.set_footer(text="Page {}/{}".format(index, len(data)))
            embeds.append(embed)

        await self.compose_menu(ctx, embeds)
        await self.replenish_cache(ctx)

    @raffle.command()
    @commands.guildowner()
    async def teardown(self, ctx: Context):
        """End ALL ongoing raffles."""
        raffles = await self.config.guild(ctx.guild).raffles()

        if not raffles:
            await ctx.send("There are no ongoing raffles in this guild.")
            return

        message = "Are you sure you want to tear down all ongoing raffles in this guild?"
        can_react = ctx.channel.permissions_for(ctx.me).add_reactions
        if not can_react:
            message += " (yes/no)"
        message = await ctx.send(message)
        if can_react:
            start_adding_reactions(message, ReactionPredicate.YES_OR_NO_EMOJIS)
            predicate = ReactionPredicate.yes_or_no(message, ctx.author)
            event_type = "reaction_add"
        else:
            predicate = MessagePredicate.yes_or_no(ctx)
            event_type = "message"
        
        try:
            await self.bot.wait_for(event_type, check=predicate, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond.")
            return

        with contextlib.suppress(discord.NotFound):
            await message.delete()

        if predicate.result:
            async with self.config.guild(ctx.guild).raffles() as r:
                r.clear()
            await ctx.send("Raffles cleared.")
        
        else:
            await ctx.send("No changes have been made.")

        await self.replenish_cache(ctx)

    @raffle.command()
    async def raw(self, ctx: Context, raffle: str):
        """View the raw dict for a raffle."""
        r = await self.config.guild(ctx.guild).raffles()

        raffle_data = r.get(raffle, None)
        if not raffle_data:
            return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))

        for page in pagify(str({raffle: raffle_data})):
            await ctx.send(box(page, lang="json"))

        await self.replenish_cache(ctx)

    @raffle.command()
    async def members(self, ctx: Context, raffle: str):
        """Get all the members of a raffle."""
        r = await self.config.guild(ctx.guild).raffles()

        raffle_data = r.get(raffle, None)
        if not raffle_data:
            return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))

        entries = raffle_data.get("entries")

        if not entries:
            return await ctx.send("There are no entries yet for this raffle.")

        embed_pages = []

        if len(entries) == 1:
            embed = discord.Embed(
                description=f"Looks like its only {self.bot.get_user(entries[0]).display_name} in here!",
                color=await ctx.embed_colour()
            )
            embed_pages.append(embed)
        else:
            for page in pagify(humanize_list([self.bot.get_user(u).display_name for u in entries])):
                embed = discord.Embed(
                    description=page,
                    color=await ctx.embed_colour()
                )
                embed_pages.append(embed)

        await self.compose_menu(ctx, embed_pages)
        await self.replenish_cache(ctx)
                
    @raffle.command()
    async def draw(self, ctx: Context, raffle: str):
        """Draw a raffle and select a winner."""
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))

            raffle_entities = lambda x: raffle_data.get(x, None)

            if not raffle_entities("entries"):
                return await ctx.send("There are no participants yet for this raffle.")
            winner = random.choice(raffle_entities("entries"))

            if raffle_entities("end_message"):
                message = raffle_entities("end_message")
            else:
                message = "Congratulations {winner.mention}, you have won the {raffle} raffle!"

            message = message.format(winner=RaffleSafeMember(member=self.bot.get_user(winner)), raffle=raffle)

            # Let's add a bit of suspense, shall we? :P
            await ctx.send("Picking a winner from the pool...")
            await ctx.trigger_typing()
            await asyncio.sleep(2)

            await ctx.send(message)

            r.pop(raffle)

        await self.replenish_cache(ctx)

    @raffle.command()
    async def info(self, ctx: Context, raffle: str):
        """Get information about a certain raffle."""
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))

            raffle_entities = lambda x: raffle_data.get(x, None)

            properties = {
                "name": raffle,
                "description": raffle_data.get("description", None),
                "rolesreq": raffle_data.get("roles_needed_to_enter", None),
                "agereq": raffle_data.get("account_age", None),
                "joinreq": raffle_data.get("join_age", None),
                "prevented_users": raffle_data.get("prevented_users", None),
                "allowed_users": raffle_data.get("allowed_users", None),
                "owner": raffle_data.get("owner", None),
                "maximum_entries": raffle_data.get("maximum_entries", None),
                "entries": raffle_data.get("entries", None),
            }

            embed = discord.Embed(
                title="Raffle information | {}".format(properties["name"]),
                description=properties["description"] or italics("No description was provided."),
                color=await ctx.embed_colour(),
                timestamp=datetime.datetime.now(),
            )

            embed.add_field(
                name="Owner",
                value=self.bot.get_user(properties["owner"]).mention,
                inline=True
            )

            embed.add_field(
                name="Entries",
                value=len(properties["entries"]),
                inline=True
            )

            if properties["maximum_entries"]:
                embed.add_field(
                    name="Max Entries",
                    value=humanize_number(properties["maximum_entries"]),
                    inline=True
                )

            if any([properties["joinreq"], properties["agereq"]]):

                age_requirements = []

                if properties["joinreq"]:
                    text = "Guild: {}".format( 
                        properties["joinreq"]
                    )
                    age_requirements.append(text)

                if properties["agereq"]:
                    text = "Discord: {}\n".format(
                        properties["agereq"]
                    )
                    age_requirements.append(text)
                
                embed.add_field(
                    name="Age Requirements",
                    value=box("# Days since you've joined:\n" + "\n".join(age_requirements), lang="yaml"),
                    inline=False
                )

            if properties["rolesreq"]:
                roles = []
                for role in properties["rolesreq"]:
                    if not ctx.guild.get_role(role):
                        continue
                    roles.append(ctx.guild.get_role(role).name)

                embed.add_field(
                    name="Roles Required",
                    value=box("\n".join(f"+ @{v.lstrip('@')}" for v in roles), lang="diff"),
                    inline=False
                )

            if properties["allowed_users"]:
                users = []
                for user in properties["allowed_users"]:
                    if not ctx.guild.get_member(user):
                        continue
                    if ctx.author == ctx.guild.get_member(user):
                        users.append((">>> ", str(ctx.guild.get_member(user))))
                    else:
                        users.append(("#", str(ctx.guild.get_member(user))))

                embed.add_field(
                    name="Allowed Users",
                    value=box("\n".join(f"{v[0]}{c} {v[1]}" for c, v in enumerate(users, 1)), lang="md"),
                    inline=False
                )
            
            if properties["prevented_users"]:
                users = []
                for user in properties["prevented_users"]:
                    if not ctx.guild.get_member(user):
                        continue
                    if ctx.author == ctx.guild.get_member(user):
                        users.append((">>> ", str(ctx.guild.get_member(user))))
                    else:
                        users.append(("#", str(ctx.guild.get_member(user))))

                embed.add_field(
                    name="Prevented Users",
                    value=box("\n".join(f"{v[0]}{c} {v[1]}" for c, v in enumerate(users, 1)), lang="md"),
                    inline=False
                )

            embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
            await ctx.send(embed=embed)
        await self.replenish_cache(ctx)

    @raffle.group()
    async def edit(self, ctx):
        """Edit the settings for a raffle."""
        pass

    @edit.command()
    async def accage(self, ctx, raffle: str, new_account_age: Union[int, bool]):
        """Edit the account age requirement for a raffle.
        
        Use `0` or `false` to disable this condition.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))

            if isinstance(new_account_age, bool):
                if not new_account_age:
                    with contextlib.suppress(KeyError):
                        del raffle_data["account_age"]
                    return await ctx.send("Account age requirement removed from this raffle.")
                else:
                    return await ctx.send("Please provide a number, or \"false\" to disable this condition.")

            try:
                RaffleManager.parse_accage(new_account_age)
            except BadArgument as e:
                return await ctx.send(self.format_traceback(e))

            raffle_data["account_age"] = new_account_age
            await ctx.send("Account age requirement updated for this raffle.")

        await self.replenish_cache(ctx)

    @edit.command()
    async def joinage(self, ctx, raffle: str, new_join_age: Union[int, bool]):
        """Edit the join age requirement for a raffle.
        
        Use `0` or `false` to disable this condition.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))

            if not new_join_age:
                with contextlib.suppress(KeyError):
                    del raffle_data["join_age"]
                return await ctx.send("Join age requirement removed from this raffle.")

            elif new_join_age is True:
                return await ctx.send("Please provide a number, or \"false\" to disable this condition.")

            else:
                try:
                    RaffleManager.parse_joinage(ctx, new_join_age)
                except BadArgument as e:
                    return await ctx.send(self.format_traceback(e))

                raffle_data["join_age"] = new_join_age
                await ctx.send("Join age requirement updated for this raffle.")

        await self.replenish_cache(ctx)

    @edit.command()
    async def description(self, ctx, raffle: str, *, description: Union[bool, str]):
        """Edit the description for a raffle.
        
        Use `0` or `false` to remove this feature.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))

            if not description:
                with contextlib.suppress(KeyError):
                    del raffle_data["description"]
                return await ctx.send("Description removed from this raffle.")

            elif description is True:
                return await ctx.send("Please provide a number, or \"false\" to disable the description.")

            else:
                raffle_data["description"] = description
                await ctx.send("Description updated for this raffle.")

        await self.replenish_cache(ctx)

    @edit.command()
    async def maxentries(self, ctx, raffle: str, maximum_entries: Union[int, bool]):
        """Edit the max entries requirement for a raffle.
        
        Use `0` or `false` to disable this condition.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))

            if not maximum_entries:
                with contextlib.suppress(KeyError):
                    del raffle_data["maximum_entries"]
                return await ctx.send("Maximum entries condition removed from this raffle.")

            elif maximum_entries is True:
                return await ctx.send("Please provide a number, or \"false\" to disable this condition.")

            else:
                raffle_data["maximum_entries"] = maximum_entries
                await ctx.send("Max entries requirement updated for this raffle.")

        await self.replenish_cache(ctx)

    @edit.command()
    async def endmessage(self, ctx, raffle: str, *, end_message: Union[bool, str]):
        """Edit the end message of a raffle.
        
        Use `0` or `false` to disable this condition.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))

            if not end_message:
                with contextlib.suppress(KeyError):
                    del raffle_data["end_message"]
                return await ctx.send("End message feature removed from this raffle. It will now use the default.")

            elif end_message is True:
                return await ctx.send("Please provide a number, or \"false\" to disable this condition.")

            else:
                try:
                    await self.raffle_safe_member_scanner(ctx, end_message)
                except BadArgument as e:
                    return await ctx.send(self.format_traceback(e))
                raffle_data["end_message"] = end_message
                await ctx.send("End message updated for this raffle.")

        await self.replenish_cache(ctx)

    @edit.group()
    async def prevented(self, ctx):
        """Manage prevented users in a raffle."""
        pass

    @prevented.command(name="add")
    async def prevented_add(self, ctx, raffle: str, member: discord.Member):
        """Add a member to the prevented list of a raffle."""
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))

            prevented = raffle_data.get("prevented_users", [])

            if member.id in prevented:
                return await ctx.send("This user is already prevented in this raffle.")

            prevented.append(member.id)
            await ctx.send("{} added to the prevented list for this raffle.".format(member.name))

        await self.replenish_cache(ctx)

    @prevented.command(name="remove", aliases=["del"])
    async def prevented_remove(self, ctx, raffle: str, member: discord.Member):
        """Remove a member from the prevented list of a raffle."""
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))

            prevented = raffle_data.get("prevented_users", [])

            if member.id not in prevented:
                return await ctx.send("This user was not already prevented in this raffle.")

            prevented.remove(member.id)
            await ctx.send("{} remove from the prevented list for this raffle.".format(member.name))

        await self.replenish_cache(ctx)

    @prevented.command(name="clear")
    async def prevented_clear(self, ctx, raffle: str):
        """Clear the prevented list for a raffle.."""
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))

            prevented = raffle_data.get("prevented_users", None)

            if prevented is None:
                return await ctx.send("There are no prevented users.")

        message = "Are you sure you want to clear the prevented users list for this raffle?"
        can_react = ctx.channel.permissions_for(ctx.me).add_reactions
        if not can_react:
            message += " (yes/no)"
        message = await ctx.send(message)
        if can_react:
            start_adding_reactions(message, ReactionPredicate.YES_OR_NO_EMOJIS)
            predicate = ReactionPredicate.yes_or_no(message, ctx.author)
            event_type = "reaction_add"
        else:
            predicate = MessagePredicate.yes_or_no(ctx)
            event_type = "message"
        
        try:
            await self.bot.wait_for(event_type, check=predicate, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond.")
            return

        if predicate.result:
            with contextlib.suppress(KeyError):
                # Still wanna remove empty list here
                del raffle_data["prevented_users"]    
            try:
                await message.edit(content="Prevented users list cleared for this raffle.")
            except discord.NotFound:
                await ctx.send("Prevented users list cleared for this raffle.")
        
        else:
            await ctx.send("No changes have been made.")    

    @edit.group()
    async def allowed(self, ctx):
        """Manage the allowed users list in a raffle."""
        pass

    @allowed.command(name="add")
    async def allowed_add(self, ctx, raffle: str, member: discord.Member):
        """Add a member to the allowed list of a raffle."""
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))

            allowed = raffle_data.get("allowed_users", [])

            if member.id in allowed:
                return await ctx.send("This user is already allowed in this raffle.")

            allowed.append(member.id)
            await ctx.send("{} added to the allowed list for this raffle.".format(member.name))

        await self.replenish_cache(ctx)

    @allowed.command(name="remove", aliases=["del"])
    async def allowed_remove(self, ctx, raffle: str, member: discord.Member):
        """Remove a member from the allowed list of a raffle."""
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))

            allowed = raffle_data.get("allowed_users", [])

            if member.id not in allowed:
                return await ctx.send("This user was not already allowed in this raffle.")

            allowed.remove(member.id)
            await ctx.send("{} remove from the allowed list for this raffle.".format(member.name))

        await self.replenish_cache(ctx)

    @allowed.command(name="clear")
    async def allowed_clear(self, ctx, raffle: str):
        """Clear the allowed list for a raffle.."""
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))

            allowed = raffle_data.get("allowed_users", None)

            if allowed is None:
                return await ctx.send("There are no allowed users.")

        message = "Are you sure you want to clear the allowed list for this raffle?"
        can_react = ctx.channel.permissions_for(ctx.me).add_reactions
        if not can_react:
            message += " (yes/no)"
        message = await ctx.send(message)
        if can_react:
            start_adding_reactions(message, ReactionPredicate.YES_OR_NO_EMOJIS)
            predicate = ReactionPredicate.yes_or_no(message, ctx.author)
            event_type = "reaction_add"
        else:
            predicate = MessagePredicate.yes_or_no(ctx)
            event_type = "message"
        
        try:
            await self.bot.wait_for(event_type, check=predicate, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond.")
            return

        if predicate.result:
            with contextlib.suppress(KeyError):
                # Still wanna remove empty list here
                del raffle_data["allowed_users"]    
            try:
                await message.edit(content="Allowed list cleared for this raffle.")
            except discord.NotFound:
                await ctx.send("Allowed list cleared for this raffle.")
        
        else:
            await ctx.send("No changes have been made.")    

        await self.replenish_cache(ctx)

    @edit.group()
    async def rolesreq(self, ctx):
        """Manage role requirements in a raffle."""
        pass

    @rolesreq.command(name="add")
    async def rolesreq_add(self, ctx, raffle: str, role: discord.Role):
        """Add a role to the role requirements list of a raffle."""
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))

            roles = raffle_data["roles_needed_to_enter"]

            if role.id in roles:
                return await ctx.send("This role is already a requirement in this raffle.")

            roles.append(role.id)
            await ctx.send("{} added to the role requirement list for this raffle.".format(role.name))

        await self.replenish_cache(ctx)

    @rolesreq.command(name="remove", aliases=["del"])
    async def rolereq_remove(self, ctx, raffle: str, role: discord.Role):
        """Remove a role from the role requirements list of a raffle."""
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))

            roles = raffle_data["roles_needed_to_enter"]

            if role.id not in roles:
                return await ctx.send("This role is not already a requirement in this raffle.")

            roles.remove(role.id)
            await ctx.send("{} remove from the role requirement list for this raffle.".format(role.name))

        await self.replenish_cache(ctx)

    @rolesreq.command(name="clear")
    async def rolereq_clear(self, ctx, raffle: str):
        """Clear the prevented list for a raffle.."""
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))

            rolesreq = raffle_data.get("roles_needed_to_enter", None)

            if rolesreq is None:
                return await ctx.send("There are no required roles.")

        message = "Are you sure you want to clear the role requirement list for this raffle?"
        can_react = ctx.channel.permissions_for(ctx.me).add_reactions
        if not can_react:
            message += " (yes/no)"
        message = await ctx.send(message)
        if can_react:
            start_adding_reactions(message, ReactionPredicate.YES_OR_NO_EMOJIS)
            predicate = ReactionPredicate.yes_or_no(message, ctx.author)
            event_type = "reaction_add"
        else:
            predicate = MessagePredicate.yes_or_no(ctx)
            event_type = "message"
        
        try:
            await self.bot.wait_for(event_type, check=predicate, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond.")
            return

        if predicate.result:
            with contextlib.suppress(KeyError):
                # Still wanna remove empty list here
                del raffle_data["roles_needed_to_enter"]    
            try:
                await message.edit(content="Role requirement list cleared for this raffle.")
            except discord.NotFound:
                await ctx.send("Role requirement list cleared for this raffle.")
        
        else:
            await ctx.send("No changes have been made.")    

        await self.replenish_cache(ctx)

    @raffle.command()
    async def conditions(self, ctx):
        """Get information about how conditions work."""
        message = "\n".join(f"{e.name}: {e.value[0].__name__}\n\t{e.value[1]}" for e in RaffleComponents)
        await ctx.send(box(message, lang="yaml"))
        await self.replenish_cache(ctx)