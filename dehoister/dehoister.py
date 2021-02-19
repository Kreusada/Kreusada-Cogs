import io
import discord
import logging
import asyncio

from redbot.core import commands, Config
from redbot.core.utils.chat_formatting import box
from redbot.core.utils.predicates import ReactionPredicate
from redbot.core.utils.menus import start_adding_reactions

log = logging.getLogger("red.kreusada.dehoister")

IDENTIFIER = 435089473534

HOIST = "!\"#$%&'()*+,-./:;<=>?@0123456789"

AUTO_DEHOIST_EXPLAIN = (
    "To get started, use `{p}hoist set toggle true`, which will enable this feature. "
    "Then, you can customize the nickname via `{p}hoist set nickname`.\n\n"
    "When new users join the guild, their nickname will automatically be changed "
    "to this configured nickname, if they have a hoisted character at the start of their name. "
    "If your bot doesn't have permissions, **this process will be cancelled**, so make sure that "
    "your bot has access to nickname changing."
)

SCAN_AND_CLEAN_EXPLAIN = (
    "If users were able to bypass the auto dehoister, due to the bot being down, or it was toggled
    "off, there are still tools you can use to protect your guild against hoisted names."
    "`{p}hoist scan` will return a full list of users who have hoisted nicknames or usernames."
    "`{p}hoist clean` will change everyones nickname to the configured nickname if they
    "have a hoisted username/nickname."
)


class Dehoister(commands.Cog):
    """
    Dehoist usernames that start with hoisting characters.
    """

    __author__ = "Kreusada"
    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, IDENTIFIER, force_registration=True)
        self.config.register_guild(nickname="Ze Dehoisted", toggled=False)

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad."""
        return f"{super().format_help_for_context(ctx)}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    async def clean_hoist_pred(self, ctx):
        hoisted_count = self.get_hoisted_count(ctx)
        if not hoisted_count:
            return await ctx.send("There are no hoisted members.")
        if not ctx.channel.permissions_for(ctx.me).add_reactions:
            return await ctx.send("I cannot add reactions.")
        msg = await ctx.send(
            f"Are you sure you would like to dehoist {hoisted_count} hoisted users? "
            f"This may take a few moments. Their nickname's will be changed to {nickname}, "
            f"you can cancel now and change this nickname via `{ctx.clean_prefix}hoist set nickname "
            "if you wish."
        )
        pred = ReactionPredicate.yes_or_no(msg, ctx.author)
        start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)
        try:
            await self.bot.wait_for("reaction_add", check=pred, timeout=30)
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send(f"You took too long to respond.")
        if pred.result:
            if ctx.channel.permissions_for(ctx.me).manage_nicknames:
                async with ctx.typing():
                    for m in ctx.guild.members:
                        if m.display_name.startswith(tuple(HOIST)):
                            try:
                                await m.edit(
                                    nick=await self.config.guild(ctx.guild).nickname()
                                )
                            except discord.Forbidden:
                                exception = True
                                await ctx.send(
                                    f"I could not change {ctx.guild.owner.name}'s nickname because I cannot edit owner nicknames."
                                )
                await ctx.send(
                    f"{hoisted_count - 1 if exception else 0} users have been dehoisted."
                )
            else:
                return await ctx.send("I do not have permissions.")
        else:
            await ctx.send("No changes have been made.")

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
        if await self.config.guild(guild).toggled() is False:
            return
        if member.bot:
            return
        if not guild:
            return
        if member.name.startswith(tuple(HOIST)):
            try:
                return await member.edit(nick=await self.config.guild(guild).nickname())
            except discord.Forbidden as f:
                log.error(f)

    @commands.group()
    @commands.mod_or_permissions(manage_nicknames=True)
    async def hoist(self, ctx):
        """Commands for Dehoister."""

    @commands.command()
    async def dehoist(self, ctx: commands.Context, member: discord.Member):
        """Manually dehoist a particular user."""
        try:
            await member.edit(nick=await self.config.guild(ctx.guild).nickname())
            await ctx.send(f"`{member.name}` has successfully been dehoisted.")
        except discord.Forbidden:
            await ctx.send("I am not authorized to edit nicknames.")

    @hoist.command()
    async def scan(self, ctx):
        """Scan for hoisted members."""
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
    async def clean(self, ctx):
        """Dehoist all members in the guild."""
        await self.clean_hoist_pred(ctx)

    @commands.admin_or_permissions(administrator=True)
    @hoist.group(name="set")
    async def _set(self, ctx: commands.Context):
        """Settings for Dehoister."""

    @_set.group()
    async def explain(self, ctx: commands.Context):
        """Explain how Dehoister works."""

    @explain.command()
    async def auto(self, ctx):
        """Explains how auto-dehoist works."""
        if await ctx.embed_requested():
            embed = discord.Embed(
                description=AUTO_DEHOIST_EXPLAIN.format(p=ctx.clean_prefix),
                color=await ctx.embed_colour(),
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(AUTO_DEHOIST_EXPLAIN.format(p=ctx.clean_prefix))

    @explain.command()
    async def scanclean(self, ctx):
        """Explains how scanning and cleaning works."""
        if await ctx.embed_requested():
            embed = discord.Embed(
                description=SCAN_AND_CLEAN_EXPLAIN.format(p=ctx.clean_prefix),
                color=await ctx.embed_colour(),
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(SCAN_AND_CLEAN_EXPLAIN.format(p=ctx.clean_prefix))

    @_set.command()
    async def toggle(self, ctx: commands.Context, true_or_false: bool):
        """Toggle the Dehoister."""
        await self.config.guild(ctx.guild).toggled.set(true_or_false)
        await ctx.send(
            "Dehoister has been enabled."
        ) if true_or_false is True else await ctx.send("Dehoister has been disabled.")

    @_set.command()
    async def nickname(self, ctx: commands.Context, *, nickname: str):
        """Set the nickname for dehoisted members."""
        if len(nickname) < 32:
            await self.config.guild(ctx.guild).nickname.set(nickname)
            await ctx.send(
                f"Dehoisted members will now have their nickname set to `{nickname}`."
            )
        else:
            await ctx.send(
                f"Discord has a limit of 32 characters for nicknames. Your chosen nickname, {nickname}, could not be set."
            )
