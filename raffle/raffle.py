import asyncio
import contextlib
import datetime
import pathlib
import random

import discord
import yaml

from redbot.core import commands, Config
from redbot.core.commands import BadArgument, Context
from redbot.core.utils import chat_formatting as cf

from yaml.parser import (
    ParserError as YAMLParserError,
    ScannerError as YAMLScannerError,
    MarkedYAMLError as YAMLMarkedError
)

with open(pathlib.Path(__file__).parent / "assets" / "raffle.yaml") as f:
    asset = cf.box("".join(f.readlines()), lang="yaml")

with open(pathlib.Path(__file__).parent / "assets" / "conditions.yaml") as f:
    conditions = cf.box("".join(f.readlines()), lang="yaml")

now = datetime.datetime.now()
discord_creation_date = datetime.datetime(2015, 5, 13)

account_age_checker = lambda x: x < (now - discord_creation_date).days
join_age_checker = lambda ctx, x: x < (now - ctx.guild.created_at).days


class RaffleError(Exception):
    """Base exception for all raffle exceptions."""
    pass


class RequiredKeyError(RaffleError):
    """Raised when a raffle key is required."""

    def __init__(self, **kwargs):
        self.key = kwargs.get("key")

    def __str__(self):
        return f"The \"{self.key}\" key is required"


class UnknownRoleError(RaffleError):
    """Raised when an invalid role is provided to the parser."""

    def __init__(self, **kwargs):
        self.role = kwargs.get("role")

    def __str__(self):
        return f"\"{self.role}\" was not a valid role"

class UnknownUserError(RaffleError):
    """Raised when an invalid role is provided to the parser."""

    def __init__(self, **kwargs):
        self.user = kwargs.get("user")

    def __str__(self):
        return f"\"{self.user}\" was not a valid user"

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
        self.roles_needed_to_enter = (
            data.get("roles_needed_to_enter", None) 
            or data.get("role_needed_to_enter", None)
        )
        self.prevented_users = (
            data.get("prevented_users", None)
            or data.get("prevented_user", None)
        )

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
        if self.description:
            if not isinstance(self.description, str):
                raise BadArgument("Description must be str, not {}".format(type(self.description).__name__))
        if self.roles_needed_to_enter:
            if not isinstance(self.roles_needed_to_enter, (int, list)):
                raise BadArgument("Roles must be int or list of ints, not {}".format(type(self.roles_needed_to_enter).__name__))
            if isinstance(self.roles_needed_to_enter, list):
                for r in self.roles_needed_to_enter:
                    if not ctx.guild.get_role(r):
                        raise UnknownRoleError(role=r)
            else:
                if not ctx.guild.get_role(self.roles_needed_to_enter):
                    raise UnknownRoleError(role=self.roles_needed_to_enter)
        if self.prevented_users:
            if not isinstance(self.prevented_users, (int, list)):
                raise BadArgument("Prevented users must be int or list of ints, not {}".format(type(self.prevented_users).__name__))
            if isinstance(self.prevented_users, list):
                for u in self.prevented_users:
                    if not ctx.bot.get_user(u):
                        raise UnknownUserError(user=u)
            else:
                if not ctx.bot.get_user(self.prevented_users):
                    raise UnknownUserError(user=self.prevented_users)

class Raffle(commands.Cog):
    """Create raffles for your server."""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 583475034985340, force_registration=True)
        self.config.register_guild(raffles={})

    @staticmethod
    def format_traceback(exc) -> str:
        boxit = lambda x, y: cf.box(f"{x}: {y}", lang="yaml")
        return boxit(exc.__class__.__name__, exc)

    @staticmethod
    def cleanup_code(content) -> str:
        # From redbot.core.dev_commands, thanks will :P
        if content.startswith("```") and content.endswith("```"):
            return "\n".join(content.split("\n")[1:-1])
        return content.strip("` \n")

    @staticmethod
    def validator(data) -> dict:
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
                getter = v[0].get("entries")
                for userid in getter:
                    if not self.bot.get_user(userid):
                        getter.remove(userid)
                getter = v[0].get("prevented_users")
                for userid in getter:
                    if not self.bot.get_user(userid):
                        getter.remove(userid)
                getter = v[0].get("roles_needed_to_enter")
                for roleid in getter:
                    if not ctx.guild.get_role(roleid):
                        getter.remove(roleid)

    @commands.group()
    async def raffle(self, ctx: Context):
        """Manage raffles for your server."""

    @raffle.command()
    async def create(self, ctx: Context):
        """Create a raffle."""
        await self.replenish_cache(ctx)
        check = lambda x: x.author == ctx.author and x.channel == ctx.channel
        await ctx.send(
            "Now you need to create your raffle using YAML.\n"
            "The `name` field is required, whilst you can also add an " 
            "optional description and various conditions. See below for"
            " an example:" + asset
        )
        try:
            content = await self.bot.wait_for("message", timeout=250, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("You took too long to respond.")
        content = content.content
        valid = self.validator(self.cleanup_code(content))
        if not valid:
            return await ctx.send("Please provide valid YAML.")
        try:
            parser = RaffleManager(valid)
            parser.parser(ctx)
        except Exception as e:
            return await ctx.send(self.format_traceback(e))
        async with self.config.guild(ctx.guild).raffles() as raffle:
            rafflename = valid.get("name").lower()
            if rafflename in [x.lower() for x in raffle.keys()]:
                return await ctx.send("A raffle with this name already exists.")
            data = {
                "account_age": valid.get("account_age", None),
                "join_age": valid.get("join_age", None),
                "roles_needed_to_enter": valid.get("roles_needed_to_enter" or "role_needed_to_enter", []),
                "prevented_users": valid.get("prevented_users" or "prevented_user", []),
                "entries": [],
                "maximum_entries": valid.get("maximum_entries", None),
                "owner": ctx.author.id,
                "description": valid.get("description", None)
            }
            raffle[rafflename] = [data]
            await ctx.send(
                "Raffle created with the name \"{0}\". Type `{1}raffle join {0}` to join the raffle.".format(
                    rafflename,
                    ctx.clean_prefix
                )
            )

    @raffle.command()
    async def join(self, ctx: Context, raffle: str):
        """Join a raffle."""
        await self.replenish_cache(ctx)
        async with self.config.guild(ctx.guild).raffles() as r:
            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))
            raffle_entities = lambda x: raffle_data[0].get(x, None)
            if ctx.author.id in raffle_entities("entries"):
                return await ctx.send("You are already in this raffle.")
            if ctx.author.id in raffle_entities("prevented_users"):
                return await ctx.send("You are not allowed to join this particular raffle.")
            if ctx.author.id == raffle_entities("owner"):
                return await ctx.send("You cannot join your own raffle.")
            if raffle_entities("maximum_entries") == 0:
                return await ctx.send("Sorry, the maximum number of users have entered this raffle.")
            for r in raffle_entities("roles_needed_to_enter"):
                if not r in [x.id for x in ctx.author.roles]:
                    return await ctx.send("You are missing a required role: {}".format(ctx.guild.get_role(r).mention))
            if raffle_entities("account_age"):
                if raffle_entities("account_age") > (now - ctx.author.created_at).days:
                    return await ctx.send("Your account must be at least {} days old to join.".format(raffle_entities("account_age")))
            raffle_entities("entries").append(ctx.author.id)
            if raffle_entities("maximum_entries") is not None:
                raffle_data[0]["maximum_entries"] -= 1
            await ctx.send(f"{ctx.author.mention} you have been added to the raffle!")

    @raffle.command()
    async def leave(self, ctx: Context, raffle: str):
        """Leave a raffle."""
        await self.replenish_cache(ctx)
        async with self.config.guild(ctx.guild).raffles() as r:
            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))
            raffle_entries = raffle_data[0].get("entries")
            if not ctx.author.id in raffle_entries:
                return await ctx.send("You are not entered into this raffle.")
            raffle_entries.remove(ctx.author.id)
            await ctx.send(f"{ctx.author.mention} you have been removed from the raffle.")

    @raffle.command()
    async def mention(self, ctx: Context, raffle: str):
        """Mention all the users entered into a raffle."""
        await self.replenish_cache(ctx)
        async with self.config.guild(ctx.guild).raffles() as r:
            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))
            raffle_entities = lambda x: raffle_data[0].get(x)
            if not ctx.author.id == raffle_entities("owner"):
                return await ctx.send("You are not the owner of this raffle.")
            if not raffle_entities("entries"):
                return await ctx.send("There are no entries yet for this raffle.")
            for page in cf.pagify(cf.humanize_list([self.bot.get_user(u).mention for u in raffle_entities("entries")])):
                await ctx.send(page)

    @raffle.command()
    async def end(self, ctx: Context, raffle: str):
        """End a raffle."""
        await self.replenish_cache(ctx)
        async with self.config.guild(ctx.guild).raffles() as r:
            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))
            raffle_entities = lambda x: raffle_data[0].get(x)
            if not ctx.author.id == raffle_entities("owner"):
                return await ctx.send("You are not the owner of this raffle.")
            r.pop(raffle)
            await ctx.send("Raffle ended.")
    
    @raffle.command()
    async def kick(self, ctx: Context, raffle: str, member: discord.Member):
        """Kick a user from your raffle."""
        await self.replenish_cache(ctx)
        async with self.config.guild(ctx.guild).raffles() as r:
            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))
            raffle_entities = lambda x: raffle_data[0].get(x)
            if not ctx.author.id == raffle_entities("owner"):
                return await ctx.send("You are not the owner of this raffle.")
            if member.id not in raffle_entities("entries"):
                return await ctx.send("This user has not entered this raffle.")
            raffle_entities("entries").remove(member.id)
            await ctx.send("User removed from the raffle.")
        
    @raffle.command(name="list")
    async def _list(self, ctx: Context):
        """List the currently ongoing raffles."""
        await self.replenish_cache(ctx)
        async with self.config.guild(ctx.guild).raffles() as r:
            if not r:
                return await ctx.send("There are no ongoing raffles.")
            await ctx.send("\n".join(f"`{r}`" for r in list(r.keys())))

    @raffle.command()
    async def teardown(self, ctx: Context):
        """End ALL ongoing raffles."""
        await self.replenish_cache(ctx)
        async with self.config.guild(ctx.guild).raffles() as r:
            r.clear()
            await ctx.send("Raffles cleared.")

    @raffle.command()
    async def raw(self, ctx: Context, raffle: str):
        """View the raw dict for a raffle."""
        await self.replenish_cache(ctx)
        async with self.config.guild(ctx.guild).raffles() as r:
            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))
            data = {raffle: raffle_data}
            for page in cf.pagify(str(data)):
                await ctx.send(cf.box(page, lang="json"))

    @raffle.command()
    async def members(self, ctx: Context, raffle: str):
        """Get all the members of a raffle."""
        await self.replenish_cache(ctx)
        async with self.config.guild(ctx.guild).raffles() as r:
            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))
            raffle_entities = lambda x: raffle_data[0].get(x)
            if not raffle_entities("entries"):
                return await ctx.send("There are no entries yet for this raffle.")
            for page in cf.pagify(cf.humanize_list([self.bot.get_user(u).display_name for u in raffle_entities("entries")])):
                await ctx.send(page)
                
    @raffle.command()
    async def draw(self, ctx: Context, raffle: str):
        """Draw a raffle and select a winner."""
        await self.replenish_cache(ctx)
        async with self.config.guild(ctx.guild).raffles() as r:
            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))
            raffle_entities = lambda x: raffle_data[0].get(x)
            if not raffle_entities("entries"):
                return await ctx.send("There are no participants yet for this raffle.")
            winner = random.choice(raffle_entities("entries"))

            # Let's add a bit of suspense, shall we? :P
            await ctx.send("Picking a winner from the pool...")
            await ctx.trigger_typing()
            await asyncio.sleep(2)

            await ctx.send(
                "Congratulations {}, you have won the {} raffle! {}".format(
                    self.bot.get_user(winner).mention,
                    raffle,
                    ":tada:"
                )
            )
            r.pop(raffle)

    @raffle.command()
    async def info(self, ctx: Context, raffle: str):
        """Get information about a certain raffle."""
        await self.replenish_cache(ctx)
        async with self.config.guild(ctx.guild).raffles() as r:
            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))
            raffle_entities = lambda x: raffle_data[0].get(x, None)
            name = raffle
            description = raffle_entities("description")
            rolesreq = raffle_entities("roles_needed_to_enter")
            agereq = raffle_entities("account_age")
            joinreq = raffle_entities("join_age")
            prevented_users = raffle_entities("prevented_users")
            owner = raffle_entities("owner")
            maximum_entries = raffle_entities("maximum_entries")
            entries = len(raffle_entities("entries"))
            message = ""
            if maximum_entries == 0:
                message += "This raffle is no longer accepting entries.\n"
            message += (
                f"\nRaffle name: {name}\n"
                f"Description: {description or 'No description was provided.'}\n"
                f"Owner: {self.bot.get_user(owner).name} ({owner})\n"
                f"Entries: {entries}"
            )
            if not any([rolesreq, agereq, prevented_users]):
                message += "\nConditions: None"
            else:
                if rolesreq:
                    message += "\nRoles Required: " + ", ".join(ctx.guild.get_role(r).name for r in rolesreq)
                if agereq:
                    message += "\nAccount age requirement in days: {}".format(agereq)
                if joinreq:
                    message += "\nGuild join age requirement in days: {}".format(joinreq)
                if prevented_users:
                    message += "\nPrevented Users: " + ", ".join(self.bot.get_user(u).name for u in prevented_users)
            await ctx.send(cf.box(message, lang="yaml"))

    @raffle.group()
    async def edit(self, ctx):
        """Edit the settings for a raffle."""
        pass

    @edit.command()
    async def accage(self, ctx, raffle: str, new_account_age: int):
        """Edit the account age requirement for a raffle."""
        await self.replenish_cache(ctx)
        async with self.config.guild(ctx.guild).raffles() as r:
            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))
            try:
                RaffleManager.parse_accage(new_account_age)
            except BadArgument as e:
                return await ctx.send(self.format_traceback(e))
            raffle_data[0]["account_age"] = new_account_age
            await ctx.send("Account age requirement updated for this raffle.")

    @edit.command()
    async def joinage(self, ctx, raffle: str, new_join_age: int):
        """Edit the join age requirement for a raffle."""
        await self.replenish_cache(ctx)
        async with self.config.guild(ctx.guild).raffles() as r:
            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))
            try:
                RaffleManager.parse_joinage(ctx, new_join_age)
            except BadArgument as e:
                return await ctx.send(self.format_traceback(e))
            raffle_data[0]["join_age"] = new_join_age
            await ctx.send("Join age requirement updated for this raffle.")

    @edit.command()
    async def description(self, ctx, raffle: str, *, description: str):
        """Edit the description of a raffle."""
        await self.replenish_cache(ctx)
        async with self.config.guild(ctx.guild).raffles() as r:
            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))
            raffle_data[0]["description"] = description
            await ctx.send("Description updated for this raffle.")

    @edit.group()
    async def prevented(self, ctx):
        """Manage prevented users in a raffle."""
        pass

    @prevented.command(name="add")
    async def prevented_add(self, ctx, raffle: str, member: discord.Member):
        """Add a member to the prevented list of a raffle."""
        await self.replenish_cache(ctx)
        async with self.config.guild(ctx.guild).raffles() as r:
            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))
            prevented = raffle_data[0]["prevented_users"]
            if member.id in prevented:
                return await ctx.send("This user is already prevented in this raffle.")
            prevented.append(member.id)
            await ctx.send("{} added to the prevented list for this raffle.".format(member.name))

    @prevented.command(name="remove", aliases=["del"])
    async def prevented_remove(self, ctx, raffle: str, member: discord.Member):
        """Add a member to the prevented list of a raffle."""
        await self.replenish_cache(ctx)
        async with self.config.guild(ctx.guild).raffles() as r:
            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))
            prevented = raffle_data[0]["prevented_users"]
            if member.id not in prevented:
                return await ctx.send("This user was not already prevented in this raffle.")
            prevented.remove(member.id)
            await ctx.send("{} remove from the prevented list for this raffle.".format(member.name))

    @edit.group()
    async def rolesreq(self, ctx):
        """Manage role requirements in a raffle."""
        pass

    @rolesreq.command(name="add")
    async def rolesreq_add(self, ctx, raffle: str, role: discord.Role):
        """Add a role to the role requirements list of a raffle."""
        await self.replenish_cache(ctx)
        async with self.config.guild(ctx.guild).raffles() as r:
            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))
            roles = raffle_data[0]["roles_needed_to_enter"]
            if role.id in roles:
                return await ctx.send("This role is already a requirement in this raffle.")
            roles.append(role.id)
            await ctx.send("{} added to the role requirement list for this raffle.".format(role.name))

    @rolesreq.command(name="remove", aliases=["del"])
    async def rolereq_remove(self, ctx, raffle: str, role: discord.Role):
        """Remove a role from the role requirements list of a raffle."""
        await self.replenish_cache(ctx)
        async with self.config.guild(ctx.guild).raffles() as r:
            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))
            roles = raffle_data[0]["roles_needed_to_enter"]
            if role.id not in roles:
                return await ctx.send("This role is not already a requirement in this raffle.")
            roles.remove(role.id)
            await ctx.send("{} remove from the role requirement list for this raffle.".format(role.name))

    @raffle.command()
    async def conditions(self, ctx):
        """Get information about how conditions work."""
        await self.replenish_cache(ctx)
        await ctx.send(conditions)