import asyncio
import contextlib
import logging

import discord
from redbot.core import Config, commands
from redbot.core.utils.chat_formatting import box
from redbot.core.utils.predicates import MessagePredicate

log = logging.getLogger("red.kreusada.serverblock")


class ServerBlock(commands.Cog):
    """
    Blocklist servers from being able to add [botname].
    """

    __author__ = ["Kreusada"]
    __version__ = "0.3.1"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 34237423098423094, force_registration=True)
        self.config.register_global(blacklist=[])

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    def cog_unload(self):
        with contextlib.suppress(Exception):
            self.bot.remove_dev_env_value("serverblock")

    async def initialize(self) -> None:
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("serverblock", lambda x: self)

    @commands.is_owner()
    @commands.group(aliases=["serverblacklist", "serverblocklist"])
    async def sbl(self, ctx):
        """
        Server blocklist management.
        """

    @sbl.command(usage="<server_id>")
    async def add(self, ctx, guild: int):
        """Add a server to the server blocklist."""
        b = await self.config.blacklist()
        if guild in b:
            return await ctx.send("This server is already blocklisted.")
        b.append(guild)
        await self.config.blacklist.set(b)
        msg = "Server added to blocklist."
        if not guild in [g.id for g in self.bot.guilds]:
            await ctx.send(msg)
        else:
            msg += (
                f" {ctx.me.name} is currently in this server. Would you like it to leave? (yes/no)"
            )
            await ctx.send(msg)
            get_guild = self.bot.get_guild(guild)
            try:
                pred = MessagePredicate.yes_or_no(ctx, user=ctx.author)
                msg = await ctx.bot.wait_for("message", check=pred, timeout=60)
            except asyncio.TimeoutError:
                await ctx.send("You took too long to respond, I assumed yes.")
                return await get_guild.leave()

            if pred.result:
                await ctx.send("Done.")
                return await get_guild.leave()
            else:
                await ctx.send(f"Okay, {ctx.me.name} will remain in the server.")

    @sbl.command(usage="<server_id>")
    async def remove(self, ctx, guild: int):
        """Remove a server from the server blocklist."""
        b = await self.config.blacklist()
        if guild in b:
            b.remove(guild)
            await self.config.blacklist.set(b)
        else:
            return await ctx.send("This server is not on the blocklist.")
        await ctx.send("Server removed from blocklist.")

    @sbl.command(name="list")
    async def _list(self, ctx):
        """Lists servers on the blocklist."""
        b = await self.config.blacklist()
        title = "Blocklisted server"
        if not b:
            return await ctx.send("There are no blocklisted servers.")
        if len(b) == 1:
            return await ctx.send(box(title + ": " + str(b[0]), lang="yaml"))
        await ctx.send(box(f"{title}s:" + "\n\n" + "\n".join(f"\t{x}" for x in b), lang="yaml"))

    @sbl.command()
    async def clear(self, ctx):
        """Clears the server blocklist."""
        blacklist = await self.config.blacklist()
        s = "s" if len(blacklist) > 1 else ""
        are = "are" if len(blacklist) > 1 else "is"
        if not blacklist:
            return await ctx.send("There are no servers on the server blocklist.")
        await ctx.send(
            f"There {are} currently {len(blacklist)} server{s} on the blocklist. Are you sure? (yes/no)"
        )
        try:
            pred = MessagePredicate.yes_or_no(ctx, user=ctx.author)
            msg = await ctx.bot.wait_for("message", check=pred, timeout=60)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond - try again, please.")

        if pred.result:
            await self.config.blacklist.clear()
            await ctx.send("Done.")
        else:
            await ctx.send("Okay, no changes.")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        config = await self.config.blacklist()
        if guild.id in config:
            with contextlib.suppress(discord.Forbidden):
                await guild.owner.send(
                    f"Your server is on my blocklist. You cannot invite me to {guild.name}."
                )
            log.info(
                "{0.name} has left a server that was on the server blocklist: {1.name} ({1.id})".format(
                    self.bot.user, guild
                )
            )
            return await guild.leave()
