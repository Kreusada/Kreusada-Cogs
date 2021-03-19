import asyncio
import discord

from redbot.core import commands, Config
from redbot.core.utils.chat_formatting import box
from redbot.core.utils.predicates import MessagePredicate

class ServerBlock(commands.Cog):
    """
    Blocklist guilds from being able to add [botname].
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 34237423098423094, force_registration=True)
        self.config.register_global(blacklist=[])

    @commands.group(aliases=["serverblacklist", "serverblocklist"])
    async def sbl(self, ctx):
        """
        Guild blocklist management.
        """

    @sbl.command(usage="<guild_id>")
    async def add(self, ctx, guild: int):
        """Add a guild to the guild blocklist."""
        b = await self.config.blacklist()
        if guild in b:
            return await ctx.send("This guild is already blocklisted.")
        b.append(guild)
        await self.config.blacklist.set(b)
        msg = "Guild added to blocklist."
        if not guild in [g.id for g in self.bot.guilds]:
            await ctx.send(msg)
        else:
            msg += (
                f" {ctx.me.name} is currently in this guild. Would you like it to leave? (yes/no)"
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
                await ctx.send(f"Okay, {ctx.me.name} will remain in the guild.")

    @sbl.command(usage="<guild_id>")
    async def remove(self, ctx, guild: int):
        """Remove a guild from the guild blocklist."""
        b = await self.config.blacklist()
        if guild in b:
            b.remove(guild)
            await self.config.blacklist.set(b)
        else:
            return await ctx.send("This guild is not on the blocklist.")
        await ctx.send("Guild removed from blocklist.")

    @sbl.command(name="list")
    async def _list(self, ctx):
        """Lists guilds on the blocklist."""
        b = await self.config.blacklist()
        title = "Blocklisted guild"
        if not b:
            return await ctx.send("There are no blocklisted guilds.")
        if len(b) == 1:
            return await ctx.send(box(title + ': ' + str(b[0]), lang='yaml'))
        await ctx.send(box(f'{title}s:' + '\n\n' + "\n".join(f"\t{x}" for x in b), lang='yaml'))

    @sbl.command()
    async def clear(self, ctx):
        """Clears the guild blocklist."""
        blacklist = await self.config.blacklist()
        s = 's' if len(blacklist) > 1 else ''
        are = 'are' if len(blacklist) > 1 else 'is'
        if not blacklist:
            return await ctx.send("There are no servers on the server blocklist.")
        await ctx.send(f"There {are} currently {len(blacklist)} server{s} on the blocklist. Are you sure? (yes/no)")
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
            return await guild.leave()