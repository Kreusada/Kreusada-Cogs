import asyncio
import datetime
import io
import logging

import discord
from redbot.core import Config, commands, modlog
from redbot.core.utils.chat_formatting import box
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.predicates import ReactionPredicate

from typing import Union

log = logging.getLogger("red.kreusada.dehoister")

IDENTIFIER = 435089473534

HOIST = tuple("!\"#$%&'()*+,-./:;<=>?@")
DELTA = "δ"

HOISTING_STANDARDS = (
    "\n\nDehoister will take actions on users if their name starts with one of the following:\n"
    + ", ".join(f"`{X}`" for X in HOIST)
)

AUTO_DEHOIST_EXPLAIN = (
    "To get started, use `{p}hoist set toggle true`, which will enable this feature. "
    "Then, you can customize the nickname via `{p}hoist set nickname`.\n\n"
    "When new users join the guild, their nickname will automatically be changed "
    "to this configured nickname, if they have a hoisted character at the start of their name. "
    "If your bot doesn't have permissions, **this process will be cancelled**, so make sure that "
    "your bot has access to nickname changing."
)

SCAN_AND_CLEAN_EXPLAIN = (
    "If users were able to bypass the auto dehoister, due to the bot being down, or it was toggled "
    "off, there are still tools you can use to protect your guild against hoisted names. "
    "`{p}hoist scan` will return a full list of users who have hoisted nicknames or usernames. "
    "`{p}hoist clean` will change everyones nickname to the configured nickname if they "
    "have a hoisted username/nickname. "
)


class Dehoister(commands.Cog):
    """
    Dehoist usernames that start with hoisting characters.
    """

    __author__ = ["Kreusada", ]
    __version__ = "1.5.1"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, IDENTIFIER, force_registration=True)
        self.config.register_guild(
            nickname=f"{DELTA} Dehoisted", toggled=False, ignored_users=[]
        )

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad."""
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    async def ex(self, ctx, _type):
        _type += HOISTING_STANDARDS
        if not await ctx.embed_requested():
            return await ctx.send(_type.format(p=ctx.clean_prefix))

        embed = discord.Embed(
            description=_type.format(p=ctx.clean_prefix), color=await ctx.embed_colour()
        )
        return await ctx.send(embed=embed)

    async def create_case(self, ctx, user, moderator):
        try:
            await modlog.register_casetype(
                name="Dehoisted",
                default_setting=True,
                image="\N{ANGER SYMBOL}",
                case_str="Dehoisted",
            )
        except RuntimeError:
            # If this casetype already exists
            pass
        await modlog.create_case(
            bot=self.bot,
            guild=ctx.guild,
            created_at=datetime.datetime.utcnow(),
            action_type="Dehoisted",
            user=user,
            moderator=moderator,
            reason="This user had a hoisted display name.",
        )

    async def get_hoisted_count(self, ctx):
        ignored_users = await self.config.guild(ctx.guild).ignored_users()
        return sum(
            bool(m.display_name.startswith(HOIST) and not m.bot and m.id not in ignored_users)
            for m in ctx.guild.members
        )

    async def get_hoisted_list(self, ctx):
        ignored_users = await self.config.guild(ctx.guild).ignored_users()
        B = "\n"  # F-string cannot include backslash
        return "\n\n".join(
            # Pre-formatting for output
            f"{m}:{f'{B}- {m.nick}' if m.nick else ''}{B}-- {m.id}"
            for m in ctx.guild.members
            if m.display_name.startswith(HOIST)
            and not m.bot and m.id not in ignored_users
        )

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):

        guild = member.guild
        ctx = self.bot.get_context(member)
        toggle = await self.config.guild(guild).toggled()

        if any([not toggle, member.bot, not guild]):
            return

        if member.name.startswith(HOIST):
            if ctx.channel.permissions_for(self.bot).manage_nicknames:
                await member.edit(nick=await self.config.guild(guild).nickname())
                await self.create_case(ctx, member, self.bot)
            else:
                log.error(f"Invalid permissions to edit a members name. [{member.id}]")


    @commands.group()
    @commands.mod_or_permissions(manage_nicknames=True)
    async def hoist(self, ctx: commands.Context):
        """Commands for Dehoister."""

    @hoist.command()
    async def dehoist(self, ctx: commands.Context, member: discord.Member):
        """
        Manually dehoist a particular user.

        **Example Usage**
        `[p]dehoist spongebob`
        `[p]dehoist 1234567890`

        Users who are dehoisted will have their nicknames changed to the set nickname.
        You can set the nickname by using `[p]hoist set nickname`.
        """
        if not ctx.channel.permissions_for(ctx.me).manage_nicknames:
            return await ctx.send("I do not have permission to edit nicknames.")

        if member.nick == await self.config.guild(ctx.guild).nickname():
            return await ctx.send(f"{member.name} is already dehoisted.")

        try:
            await member.edit(nick=await self.config.guild(ctx.guild).nickname())
            await ctx.send(f"`{member.name}` has successfully been dehoisted.")
            await self.create_case(ctx, member, ctx.author)
        except discord.Forbidden:
            await ctx.send(f"I could not dehoist {member.name}.")

    @hoist.command()
    async def scan(self, ctx: commands.Context):
        """
        Scan for hoisted members.

        This command will return a count and list of members.
        It will follow this format:
        ---------------------------------
        X users found:
        user#0001:
        - Their nickname (if applicable)
        -- Their user ID.
        ---------------------------------

        If there are more than 10 hoisted users, this list
        will instead be sent as a Discord file, named `hoisted.txt`.
        """
        await ctx.trigger_typing()
        count = await self.get_hoisted_count(ctx)
        join = f"{count} users found:\n\n{await self.get_hoisted_list(ctx)}"
        if count > 9:
            await ctx.send(
                "There were 10 or more hoisted users, so to be corteous to others, I've uploaded the list as a file.",
                file=discord.File(io.BytesIO(join.encode()), filename="hoisted.txt"),
            )

        else:
            if not count:
                await ctx.send("No hoisted users were found.")
            else:
                msg = box(join, lang="yaml")
                if await ctx.embed_requested():
                    embed = discord.Embed(
                        title=f"Hoisted users in {ctx.guild.name}",
                        description=msg,
                        color=await ctx.embed_colour(),
                    )
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(msg)

    @hoist.command()
    async def clean(self, ctx: commands.Context):
        """
        Dehoist all members in the guild.

        NOTE: If the server owner is hoisted, [botname] cannot change their nickname.
        """
        hoisted_count = await self.get_hoisted_count(ctx)
        
        guild_config = await self.config.guild(ctx.guild).all()
        nickname = guild_config["nickname"]
        ignored_users = guild_config["ignored_users"]

        if not hoisted_count:
            return await ctx.send("There are no hoisted members.")

        if not ctx.channel.permissions_for(ctx.me).add_reactions:
            return await ctx.send("I cannot add reactions.")

        if not ctx.channel.permissions_for(ctx.me).manage_nicknames:
            return await ctx.send("I do not have permission to edit nicknames.")

        msg = await ctx.send(
            f"Are you sure you would like to dehoist {hoisted_count} hoisted users? "
            f"This may take a few moments.\nTheir nickname's will be changed to `{nickname}`, "
            f"you can cancel now and change this nickname via `{ctx.clean_prefix}hoist set nickname` "
            "if you wish."
        )

        pred = ReactionPredicate.yes_or_no(msg, ctx.author)
        start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)

        try:
            await self.bot.wait_for("reaction_add", check=pred, timeout=30)
        except asyncio.TimeoutError:
            await msg.delete()
            return await ctx.send(f"You took too long to respond.")

        if pred.result:
            await ctx.trigger_typing()
            exceptions = 0
            for m in ctx.guild.members:
                if m.display_name.startswith(HOIST) and not m.bot and m.id not in ignored_users:
                    try:
                        await m.edit(
                            nick=await self.config.guild(ctx.guild).nickname()
                        )
                    except discord.Forbidden: 
                        # This exception will only occur if an attempt is made to dehoist server owner
                        exceptions += 1  
                        await ctx.send(
                            f"I could not change {ctx.guild.owner.name}'s nickname because I cannot edit owner nicknames."
                        )
            await ctx.send(f"{hoisted_count - exceptions} users have been dehoisted.")
        else:
            await ctx.send("No changes have been made.")

    @hoist.group(name="set")
    async def _set(self, ctx: commands.Context):
        """Settings for Dehoister."""

    @hoist.group()
    async def ignore(self, ctx: commands.Context):
        """Add and remove certain users from being ignored by the auto-dehoister."""

    @ignore.command(name="add", require_var_positional=True)
    async def ignore_add(self, ctx: commands.Context, *users: Union[discord.Member, int]):
        """Add users to the ignore list.

        If on the ignore list, the dehoister will not dehoist them if 
        they have a hoisted nickname/username.
        """
        async with self.config.guild(ctx.guild).ignored_users() as ignored_users:
            for uid in users:
                if isinstance(uid, discord.Member):
                    uid = uid.id
                ignored_users.append(uid)
        await ctx.tick()

    @ignore.command(name="remove", aliases=["del"], require_var_positional=True)
    async def ignore_remove(self, ctx: commands.Context, *users: int):
        """Remove users from the ignore list.
        
        Once removed, they will be dehoisted by the dehoister if 
        they have a hoisted nickname/username.
        """
        async with self.config.guild(ctx.guild).ignored_users() as ignored_users:
            for uid in users:
                try:
                    ignored_users.remove(uid)
                except ValueError:
                    pass
        await ctx.tick()

    @ignore.command(name="list")
    async def ignore_list(self, ctx: commands.Context):
        """List the users ignored by the auto-dehoister."""
        ignored = await self.config.guild(ctx.guild).ignored_users()
        if not ignored:
            return await ctx.send("There are no users on the ignore list")
        filtered = [f"{uid} ({await self._get_user_name(uid)})" for uid in ignored]
        ignored = "\n".join(filtered)
        await ctx.send(box(ignored))

    async def _get_user_name(self, uid: int):
        return await self.bot.get_or_fetch_user(uid) or "Unknown or Deleted User"

    @_set.command()
    async def toggle(self, ctx: commands.Context):
        """
        Toggle the auto-dehoister.

        When this cog is installed for the first time,
        it is automatically set **off**. Use this command to turn
        it on. You can always turn it off again at a later date.
        """
        toggled = await self.config.guild(ctx.guild).toggled()
        await self.config.guild(ctx.guild).toggled.set(not toggled)
        await ctx.send(
            "Dehoister has been enabled."
        ) if not toggled else await ctx.send("Dehoister has been disabled.")

    @_set.command()
    async def nickname(self, ctx: commands.Context, *, nickname: str):
        """
        Set the nickname for dehoisted members.

        This nickname will be referred to everytime this cog takes
        action on members with hoisted display names, so make sure you
        find a suitable display name!

        If none is set, the default nickname is `δ Dehoisted`.
        """
        if len(nickname) > 31:
            return await ctx.send(
                f"Discord has a limit of 32 characters for nicknames. Your chosen nickname could not be set."
            )
        await self.config.guild(ctx.guild).nickname.set(nickname)
        await ctx.send(
            f"Dehoisted members will now have their nickname set to `{nickname}`."
        )

    @hoist.group()
    async def explain(self, ctx: commands.Context):
        """Explain how Dehoister works."""

    @explain.command()
    async def auto(self, ctx: commands.Context):
        """Explains how auto-dehoist works."""
        await self.ex(ctx, AUTO_DEHOIST_EXPLAIN)

    @explain.command()
    async def scanclean(self, ctx: commands.Context):
        """Explains how scanning and cleaning works."""
        await self.ex(ctx, SCAN_AND_CLEAN_EXPLAIN)
