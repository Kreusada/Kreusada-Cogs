"""
MIT License

Copyright (c) 2021 kreusada

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import io
import discord
import logging
import asyncio
import datetime

from redbot.core import commands, Config, modlog
from redbot.core.utils.chat_formatting import box
from redbot.core.utils.predicates import ReactionPredicate
from redbot.core.utils.menus import start_adding_reactions

log = logging.getLogger("red.kreusada.dehoister")

IDENTIFIER = 435089473534

HOIST = "!\"#$%&'()*+,-./:;<=>?@"
DELTA = "δ"

HOISTING_STANDARDS = (
    "\n\nDehoister will take actions on users if their name starts with one of the following:\n"
    + ", ".join(f"`{X}`" for X in tuple(HOIST))
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

MODLOG_EXPLAIN = (
    "You can record events to the modlog by enabling the toggle via `{p}hoist set modlog`. "
    "If a user joins the guild with a hoisted name, or if you manually use `{p}hoist dehoist`, "
    "the events will be recorded to your modlog channel, you will need to load the modlog cog "
    "for this to work by using `{p}load modlog`.\n\n"
    "Events from `{p}hoist clean` will not be recorded, due to potential spam."
)


class Dehoister(commands.Cog):
    """
    Dehoist usernames that start with hoisting characters.
    """

    __author__ = ["Kreusada", ]
    __version__ = "1.5.0"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, IDENTIFIER, force_registration=True)
        self.config.register_guild(
            nickname=f"{DELTA} Dehoisted", toggled=False
        )

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad."""
        context = super().format_help_for_context(ctx)
        authors = ", ".join(a for a in self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    async def ex(self, ctx, _type):
        _type += HOISTING_STANDARDS
        if await ctx.embed_requested():
            embed = discord.Embed(
                description=_type.format(p=ctx.clean_prefix), color=await ctx.embed_colour()
            )
            return await ctx.send(embed=embed)
        else:
            return await ctx.send(_type.format(p=ctx.clean_prefix))

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

    @staticmethod
    def get_hoisted_count(ctx):
        count = 0
        for m in ctx.guild.members:
            if m.display_name.startswith(tuple(HOIST)):
                count += 1
        return count

    @staticmethod
    def get_hoisted_list(ctx):
        B = "\n"  # F-string cannot include backslash
        return "\n\n".join(
            f"{m}:{f'{B}- {m.nick}' if m.nick else ''}{B}-- {m.id}"
            for m in ctx.guild.members
            if m.display_name.startswith(tuple(HOIST))
        )

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = member.guild
        ctx = self.bot.get_context(member)
        toggle = await self.config.guild(guild).toggled()
        if not toggle:
            return
        if member.bot:
            return
        if not guild:
            return
        if member.name.startswith(tuple(HOIST)):
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
        if member.nick == await self.config.guild(ctx.guild).nickname():
            return await ctx.send(f"{member.name} is already dehoisted.")
        if ctx.channel.permissions_for(ctx.me).manage_nicknames:
            await member.edit(nick=await self.config.guild(ctx.guild).nickname())
            await ctx.send(f"`{member.name}` has successfully been dehoisted.")
            await self.create_case(ctx, member, ctx.author)
        else:
            await ctx.send("I am not authorized to edit nicknames.")

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
        count = self.get_hoisted_count(ctx)
        join = self.get_hoisted_list(ctx)
        if count > 9:
            await ctx.send(
                "There were 10 or more hoisted users, so to be corteous to others, I've uploaded the list as a file.",
                file=discord.File(io.BytesIO(join.encode()), filename="hoisted.txt"),
            )
        else:
            if not count:
                await ctx.send("No hoisted users were found.")
            else:
                msg = box(f"{count} users found:\n\n{join}", lang="yaml")
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
        nickname = await self.config.guild(ctx.guild).nickname()
        hoisted_count = self.get_hoisted_count(ctx)
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
        exceptions = 0
        if pred.result:
            await ctx.trigger_typing()
            for m in ctx.guild.members:
                if m.display_name.startswith(tuple(HOIST)):
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

    @_set.command()
    async def toggle(self, ctx: commands.Context):
        """
        Toggle the auto-dehoister.

        When this cog is installed for the first time,
        it is automatically set **off**. Use this command to turn
        it on. You can always turn it off again at a later date.
        """
        toggled = await self.config.guild(ctx.guild).toggled()
        await self.config.guild(ctx.guild).toggled.set(False if toggled else True)
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

        If none is set, the default nickname is `Ze Dehoisted`.
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

    @explain.command(name="modlog")
    async def _modlog(self, ctx: commands.Context):
        """Explains how the modlog works."""
        await self.ex(ctx, MODLOG_EXPLAIN)
