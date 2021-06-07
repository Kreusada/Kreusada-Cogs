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

from typing import List, Optional, Union

from yaml.parser import MarkedYAMLError
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

from .exceptions import (
    RequiredKeyError, 
    RaffleError
)

from .enums import RaffleComponents
from .parser import RaffleManager
from .safety import RaffleSafeMember
from .checks import now
from .formatting import tick, cross

from .helpers import (
    format_traceback,
    cleanup_code,
    validator,
    raffle_safe_member_scanner
)


with open(pathlib.Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


class Raffle(commands.Cog):
    """Create raffles for your server."""

    __author__ = ["Kreusada"]
    __version__ = "1.0.2"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 583475034985340, force_registration=True)
        self.config.register_guild(raffles={})
        self.docs = "https://kreusadacogs.readthedocs.io/en/latest/cog_raffle.html"


    async def replenish_cache(self, ctx: Context) -> None:
        async with self.config.guild(ctx.guild).raffles() as r:

            updates = {}

            for k, v in list(r.items()):

                getter = v.get("owner")
                if not self.bot.get_user(getter):
                    del r[k]
                    updates["owner"] = True

                getter = v.get("entries")
                for userid in getter:
                    if not self.bot.get_user(userid):
                        getter.remove(userid)
                        updates["entries"] = True

                getter = v.get("prevented_users", None)
                if getter:
                    for userid in getter:
                        if not ctx.guild.get_member(userid):
                            getter.remove(userid)
                            updates["prevented_users"] = True

                getter = v.get("allowed_users", None)
                if getter:
                    for userid in getter:
                        if not ctx.guild.get_member(userid):
                            getter.remove(userid)
                            updates["allowed_users"] = True

                getter = v.get("roles_needed_to_enter", None)
                if getter:
                    for roleid in getter:
                        if not ctx.guild.get_role(roleid):
                            getter.remove(roleid)
                            updates["roles_needed_to_enter"] = True

            return any([updates[x] for x in list(updates.keys())])


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


    @commands.group()
    async def raffle(self, ctx: Context):
        """Manage raffles for your server."""


    @raffle.command()
    async def version(self, ctx: Context):
        """Get the version of your Raffle cog."""
        await ctx.send(inline(self.__version__))

    @raffle.command()
    async def docs(self, ctx: Context):
        """Get a link to the docs."""
        message = "**Docs:** {0.docs}".format(self)
        await ctx.send(message)

    @raffle.group()
    async def create(self, ctx: Context):
        """Create a raffle."""
        pass


    @create.command(name="complex")
    async def _complex(self, ctx: Context):
        """Create a raffle with complex conditions."""
        await ctx.trigger_typing()
        check = lambda x: x.author == ctx.author and x.channel == ctx.channel
        message = (
            "You're about to create a new raffle.\n"
            "Please consider reading the docs about the various "
            "conditional blocks if you haven't already.\n\n"
            + self.docs
        )

        message += "\n\n**Conditions Blocks:**" + box("\n".join(f"+ {e.name}" for e in RaffleComponents), lang="diff") 
        await ctx.send(message)  


        try:
            content = await self.bot.wait_for("message", timeout=500, check=check)
        except asyncio.TimeoutError:
            with contextlib.suppress(discord.NotFound):
                await message.delete()


        content = content.content
        valid = validator(cleanup_code(content))

        if not valid:
            return await ctx.send(
                cross("Please provide valid YAML. You can validate your raffle YAML using `{}raffle parse`.").format(ctx.clean_prefix)
            )

        try:
            parser = RaffleManager(valid)
            parser.parser(ctx)
        except (RaffleError, BadArgument) as e:
            exc = cross("An exception occured whilst parsing your data.")
            return await ctx.send(exc + format_traceback(e))


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
                "maximum_entries": valid.get("maximum_entries", None),
                "on_end_action": valid.get("on_end_action", None),
            }

            for k, v in conditions.items():
                if v:
                    data[k] = v

            raffle[rafflename] = data
            await ctx.send(tick("Raffle created with the name `{}`.".format(rafflename)))

        await self.replenish_cache(ctx)


    @create.command()
    async def simple(self, ctx, raffle_name: str, *, description: Optional[str] = None):
        """Create a simple arguments with just a name and description.
        
        **Arguments:**
            - `<name>` - The name for the raffle.
            - `[description]` - The description for the raffle.
        """
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
    async def asyaml(self, ctx: Context, raffle: str):
        """Get a raffle in its YAML format.

        **Arguments:**
            - `<raffle>` - The name of the raffle to get the YAML for.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))

        quotes = lambda x: f'"{x}"'
        relevant_data = [("name", quotes(raffle))]
        for k, v in raffle_data.items():
            if k in ("owner", "entries"):
                # These are not user defined keys
                continue
            if isinstance(v, str):
                v = quotes(v)
            relevant_data.append((k, v))

        message = "**YAML Format for the `{}` raffle**\n".format(raffle)
        await ctx.send(message + box("\n".join(f"{x[0]}: {x[1]}" for x in relevant_data), lang="yaml"))

        await self.replenish_cache(ctx)

    @raffle.command()
    async def template(self, ctx: Context):
        """Get a template of a raffle."""
        with open(pathlib.Path(__file__).parent / "template.yaml") as f:
            docs = "**For more information:** {}\n".format(self.docs)
            await ctx.send(docs + box("".join(f.readlines()), lang="yaml"))

    @raffle.command()
    async def parse(self, ctx: Context):
        """Parse a complex raffle without actually creating it."""
        await ctx.trigger_typing()
        check = lambda x: x.author == ctx.author and x.channel == ctx.channel
        message = (
            "Paste your YAML here. It will be validated, and if there is "
            "an exception, it will be returned to you."

        )

        await ctx.send(message)  

        try:
            content = await self.bot.wait_for("message", timeout=500, check=check)
        except asyncio.TimeoutError:
            with contextlib.suppress(discord.NotFound):
                await message.delete()


        content = content.content
        valid = validator(cleanup_code(content))

        if not valid:
            return await ctx.send("This YAML is invalid.")

        try:
            parser = RaffleManager(valid)
            parser.parser(ctx)
        except (RaffleError, BadArgument) as e:
            exc = "An exception occured whilst parsing your data."
            return await ctx.send(cross(exc) + format_traceback(e))
        
        await ctx.send(tick("This YAML is good to go! No errors were found."))

        await self.replenish_cache(ctx)

    @raffle.command()
    async def join(self, ctx: Context, raffle: str):
        """Join a raffle.
        
        **Arguments:**
            - `<raffle>` - The name of the raffle to join.
        """
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
        """Leave a raffle.
        
        **Arguments:**
            - `<raffle>` - The name of the raffle to leave.
        """
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
        """Mention all the users entered into a raffle.
        
        **Arguments:**
            - `<raffle>` - The name of the raffle to mention all the members in.
        """
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
        """End a raffle.
        
        **Arguments:**
            - `<raffle>` - The name of the raffle to end.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))

            msg = await ctx.send(f"Ending the `{raffle}` raffle...")
            raffle_owner = raffle_data.get("owner")
            
            if not ctx.author.id == raffle_owner:
                return await ctx.send("You are not the owner of this raffle.")

            r.pop(raffle)

        await asyncio.sleep(1)
        with contextlib.suppress(discord.NotFound):
            await msg.edit(content="Raffle ended.")

        await self.replenish_cache(ctx)
    

    @raffle.command()
    @commands.guildowner()
    async def refresh(self, ctx: Context):
        """Refresh all of the raffle caches."""
        cleaner = await self.replenish_cache(ctx)
        if cleaner:
            return await ctx.send("Raffles updated.")
        else:
            return await ctx.send("Everything was already up to date.")


    @raffle.command()
    async def kick(self, ctx: Context, raffle: str, member: discord.Member):
        """Kick a member from your raffle.
        
        **Arguments:**
            - `<raffle>` - The name of the raffle.
            - `<member>` - The member to kick from the raffle.
        """
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
        """View the raw dictionary for a raffle.
        
        **Arguments:**
            - `<raffle>` - The name of the raffle.
        """
        r = await self.config.guild(ctx.guild).raffles()

        raffle_data = r.get(raffle, None)
        if not raffle_data:
            return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))

        for page in pagify(str({raffle: raffle_data})):
            await ctx.send(box(page, lang="json"))

        await self.replenish_cache(ctx)


    @raffle.command()
    async def members(self, ctx: Context, raffle: str):
        """Get all the members of a raffle.
        
        **Arguments:**
            - `<raffle>` - The name of the raffle to get the members from.
        """
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
        """Draw a raffle and select a winner.
        
        **Arguments:**
            - `<raffle>` - The name of the raffle to draw a winner from.
        """
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

            on_end_action = raffle_entities("on_end_action") or "keep_winner"
            message = message.format(winner=RaffleSafeMember(member=self.bot.get_user(winner)), raffle=raffle)

            # Let's add a bit of suspense, shall we? :P
            await ctx.send("Picking a winner from the pool...")
            await ctx.trigger_typing()
            await asyncio.sleep(2)

            await ctx.send(message)

            if on_end_action == "keep_winner":
                return
            if on_end_action == "remove_winner": 
                raffle_entities("entries").remove(winner)
                return
            else:
                # end
                r.pop(raffle)

        await self.replenish_cache(ctx)


    @raffle.command()
    async def info(self, ctx: Context, raffle: str):
        """Get information about a certain raffle.
        
        **Arguments:**
            - `<raffle>` - The name of the raffle to get information for.
        """
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
                "end_message": raffle_data.get("end_message", None),
                "on_end_action": raffle_data.get("on_end_action", None)
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

            embed.add_field(
                name="End Action",
                value=inline(properties["on_end_action"] or "keep_winner"),
                inline=False
            )

            if properties["maximum_entries"]:
                embed.add_field(
                    name="Maximum Entries",
                    value=humanize_number(properties["maximum_entries"]),
                    inline=False
                )

            winner_text = box(properties["end_message"] or r"Congratulations {winner.mention}, you have won the {raffle} raffle!")
            embed.add_field(
                name="Winner text",
                value=winner_text,
                inline=False
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

                if roles:

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

                if users:
                    
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

                if users:

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
        
        **Arguments:**
            - `<raffle>` - The name of the raffle.
            - `<new_account_age>` - The new account age requirement.
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
                return await ctx.send(format_traceback(e))

            raffle_data["account_age"] = new_account_age
            await ctx.send("Account age requirement updated for this raffle.")

        await self.replenish_cache(ctx)


    @edit.command()
    async def joinage(self, ctx, raffle: str, new_join_age: Union[int, bool]):
        """Edit the join age requirement for a raffle.
        
        Use `0` or `false` to disable this condition.
        
        **Arguments:**
            - `<raffle>` - The name of the raffle.
            - `<new_join_age>` - The new join age requirement.
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
                    return await ctx.send(format_traceback(e))

                raffle_data["join_age"] = new_join_age
                await ctx.send("Join age requirement updated for this raffle.")

        await self.replenish_cache(ctx)


    @edit.command()
    async def description(self, ctx, raffle: str, *, description: Union[bool, str]):
        """Edit the description for a raffle.
        
        Use `0` or `false` to remove this feature.
        
        **Arguments:**
            - `<raffle>` - The name of the raffle.
            - `<description>` - The new description.
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
    async def endaction(self, ctx, raffle: str, *, on_end_action: Union[bool, str]):
        """Edit the on_end_action for a raffle.
        
        Use `0` or `false` to remove this feature.
        
        **Arguments:**
            - `<raffle>` - The name of the raffle.
            - `<on_end_action>` - The new action. Must be one of `end`, `remove_winner`, or `keep_winner`.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))

            if not on_end_action:
                with contextlib.suppress(KeyError):
                    del raffle_data["on_end_action"]
                return await ctx.send("On end action set to the default: `keep_winner`.")

            elif on_end_action is True:
                return await ctx.send("Please provide a number, or \"false\" to disable the description.")

            else:
                if not on_end_action in ("end", "remove_winner", "keep_winner"):
                    return await ctx.send("Please provide one of `end`, `remove_winner`, or `keep_winner`.")
                raffle_data["on_end_action"] = on_end_action
                await ctx.send("On end action updated for this raffle.")

        await self.replenish_cache(ctx)


    @edit.command()
    async def maxentries(self, ctx, raffle: str, maximum_entries: Union[int, bool]):
        """Edit the max entries requirement for a raffle.
        
        Use `0` or `false` to disable this condition.
        
        **Arguments:**
            - `<raffle>` - The name of the raffle.
            - `<maximum_entries>` - The new maximum number of entries.
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
        
        **Arguments:**
            - `<raffle>` - The name of the raffle.
            - `<end_message>` - The new ending message.
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
                    raffle_safe_member_scanner(ctx, end_message)
                except BadArgument as e:
                    return await ctx.send(format_traceback(e))
                raffle_data["end_message"] = end_message
                await ctx.send("End message updated for this raffle.")

        await self.replenish_cache(ctx)

    @edit.command()
    async def fromyaml(self, ctx, raffle: str):
        """Edit a raffle directly from yaml.
        
        **Arguments:**
            - `<raffle>` - The name of the raffle to edit.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))

            if not ctx.author.id == raffle_data["owner"]:
                return await ctx.send("You are not the owner of this raffle.")

        existing_data = {
            "end_message": raffle_data.get("end_message", None),
            "account_age": raffle_data.get("account_age", None),
            "join_age": raffle_data.get("join_age", None),
            "roles_needed_to_enter": raffle_data.get("roles_needed_to_enter", None),
            "prevented_users": raffle_data.get("prevented_users", None),
            "allowed_users": raffle_data.get("allowed_users", None),
            "description": raffle_data.get("description", None),
            "maximum_entries": raffle_data.get("maximum_entries", None),
            "on_end_action": raffle_data.get("on_end_action", None),
        }

        message = (
            "You're about to **edit an existing raffle**.\n\nThe `name` "
            "block cannot be edited through this command, it's preferred "
            "if you create a new raffle with the new name instead.\nYou can end "
            f"this raffle through using `{ctx.clean_prefix}raffle end {raffle}`."
            "\nPlease consider reading the docs about the various "
            "conditional blocks if you haven't already.\n\n"
            + self.docs
        )

        quotes = lambda x: f'"{x}"'
        noedits = lambda x: f"{x} # Cannot be edited"
        relevant_data = [("name", noedits(quotes(raffle)))]
        for k, v in raffle_data.items():
            if k in ("owner", "entries"):
                # These are not user defined keys
                continue
            if isinstance(v, str):
                v = quotes(v)
            relevant_data.append((k, v))

        message += "\n\n**Current settings:**" + box("\n".join(f"{x[0]}: {x[1]}" for x in relevant_data), lang="yaml")
        await ctx.send(message)  

        check = lambda x: x.channel == ctx.channel and x.author == ctx.author

        try:
            content = await self.bot.wait_for("message", timeout=500, check=check)
        except asyncio.TimeoutError:
            with contextlib.suppress(discord.NotFound):
                await message.delete()


        content = content.content
        valid = validator(cleanup_code(content))

        if not valid:
            return await ctx.send(
                "Please provide valid YAML. You can validate your raffle YAML using `{}raffle parse`.".format(ctx.clean_prefix)
            )

        try:
            parser = RaffleManager(valid)
            parser.parser(ctx)
        except RequiredKeyError:
            pass
        except (RaffleError, BadArgument) as e:
            exc = cross("An exception occured whilst parsing your data.")
            return await ctx.send(exc + format_traceback(e))

        data = {
            "owner": raffle_data.get("owner"),
            "entries": raffle_data.get("entries")
        }

        conditions = {
            "end_message": valid.get("end_message", None),
            "account_age": valid.get("account_age", None),
            "join_age": valid.get("join_age", None),
            "roles_needed_to_enter": valid.get("roles_needed_to_enter", None),
            "prevented_users": valid.get("prevented_users", None),
            "allowed_users": valid.get("allowed_users", None),
            "description": valid.get("description", None),
            "maximum_entries": valid.get("maximum_entries", None),
            "on_end_action": valid.get("on_end_action", None),
        }

        for k, v in conditions.items():
            if v:
                data[k] = v

        async with self.config.guild(ctx.guild).raffles() as r:
            r[raffle] = data

        additions = []
        deletions = []

        for k, v in conditions.items():
            if v and not existing_data[k]:
                additions.append(k)
                continue
            if not v and existing_data[k]:
                deletions.append(k)
                continue

        if any([additions, deletions]):
            additions = "\n".join(f"+ {a}" for a in additions)
            deletions = "\n".join(f"- {d}" for d in deletions)

            diffs = box(f"{additions}\n{deletions}", lang="diff")
            update = tick("Raffle edited. The following conditions have been added/removed: {}".format(diffs))
        
        else:
            update = tick("Raffle edited. No conditions were added or removed.")

        await ctx.send(update)

        await self.replenish_cache(ctx)


    @edit.group()
    async def prevented(self, ctx):
        """Manage prevented users in a raffle."""
        pass


    @prevented.command(name="add")
    async def prevented_add(self, ctx, raffle: str, member: discord.Member):
        """Add a member to the prevented list of a raffle.
        
        **Arguments:**
            - `<raffle>` - The name of the raffle.
            - `<member>` - The member to add to the prevented list.
        """
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
        """Remove a member from the prevented list of a raffle.
        
        **Arguments:**
            - `<raffle>` - The name of the raffle.
            - `<member>` - The member to remove from the prevented list.
        """
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
        """Clear the prevented list for a raffle.
        
        **Arguments:**
            - `<raffle>` - The name of the raffle.
        """
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
        """Add a member to the allowed list of a raffle.
        
        **Arguments:**
            - `<raffle>` - The name of the raffle.
            - `<member>` - The member to add to the allowed list.
        """
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
        """Remove a member from the allowed list of a raffle.
        
        **Arguments:**
            - `<raffle>` - The name of the raffle.
            - `<member>` - The member to remove from the allowed list.
        """
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
        """Clear the allowed list for a raffle."""
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
        """Add a role to the role requirements list of a raffle.
        
        **Arguments:**
            - `<raffle>` - The name of the raffle.
            - `<role>` - The role to add to the list of role requirements.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))

            roles = raffle_data.get("roles_needed_to_enter", [])

            if role.id in roles:
                return await ctx.send("This role is already a requirement in this raffle.")

            if not roles:
                raffle_data["roles_needed_to_enter"] = [role.id]
            else:
                roles.append(role.id)
            await ctx.send("{} added to the role requirement list for this raffle.".format(role.name))

        await self.replenish_cache(ctx)


    @rolesreq.command(name="remove", aliases=["del"])
    async def rolereq_remove(self, ctx, raffle: str, role: discord.Role):
        """Remove a role from the role requirements list of a raffle.
        
        **Arguments:**
            - `<raffle>` - The name of the raffle.
            - `<role>` - The role to remove from the list of role requirements.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))

            roles = raffle_data.get("roles_needed_to_enter", [])

            if role.id not in roles:
                return await ctx.send("This role is not already a requirement in this raffle.")

            roles.remove(role.id)
            await ctx.send("{} remove from the role requirement list for this raffle.".format(role.name))

        await self.replenish_cache(ctx)


    @rolesreq.command(name="clear")
    async def rolereq_clear(self, ctx, raffle: str):
        """Clear the role requirement list for a raffle.

        
        **Arguments:**
            - `<raffle>` - The name of the raffle.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send("There is not an ongoing raffle with the name `{}`.".format(raffle))

            rolesreq = raffle_data.get("roles_needed_to_enter", [])

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
    async def conditions(self, ctx: Context):
        """Get information about how conditions work."""
        message = "\n".join(f"{e.name}: {e.value[0].__name__}\n\t{e.value[1]}" for e in RaffleComponents)
        await ctx.send(box(message, lang="yaml"))
        await self.replenish_cache(ctx)
