import asyncio
import contextlib
import datetime

import discord
from redbot.core import VersionInfo, commands, version_info
from redbot.core.utils.predicates import MessagePredicate

from .log import log
from .mixins import MixinMeta

RED_3_2_0 = version_info >= VersionInfo.from_str("3.2.0")
default_wave = "\N{WAVING HAND SIGN}\N{EMOJI MODIFIER FITZPATRICK TYPE-3}"


class Utilities(MixinMeta):
    async def startup(self):
        if RED_3_2_0:
            await self.bot.wait_until_red_ready()
        else:
            await self.bot.wait_until_ready()
        conf = await self.config.all()
        maybe_channel = conf.get("restart_channel", None)
        await self.config.restart_channel.clear()
        # Using the walrus operator we can check if the channel is originally None
        # Or that we cannot find that channel
        if maybe_channel is None or (ch := self.bot.get_channel(maybe_channel)) is None:
            return
        author = await self.config.restarted_author()
        try:
            await ch.send(conf["restarted_message"].replace(r"{author}", author))
        except discord.Forbidden as e:
            log.info("Unable to send a confirmation message to the restart channel")
            log.debug(
                f"Unable to send a message to channel: {ch.guild} ({ch.guild.id})", exc_info=e
            )

    async def _announce_start(self, *, reconnect: bool = False):
        if not reconnect:
            if self.red_ready():
                return  # So, the bot has already been initialized and that means that we don't have to do anything here
            if RED_3_2_0:
                await self.bot.wait_until_red_ready()
            else:
                await self.bot.wait_until_ready()
            self._already_connected = True
        conf = await self.config.all()
        maybe_channel = conf.get("announcement_channel", None)
        if any([maybe_channel is None, (ch := self.bot.get_channel(maybe_channel)) is None]):
            return
        online = (
            ("I have reconnected.", "has reconnected")
            if reconnect
            else ("I'm back online.", "is online")
        )
        kwargs = {
            "content": (
                f"**{self.bot.user.name} {online[1]}**\n\n{online[0]}"
                f"\n\n<t:{round(datetime.datetime.now().timestamp())}:R>"
            )
        }
        if ch.permissions_for(ch.guild.me).embed_links:  # Wish I could use ctx.embed_requested
            embed = discord.Embed(
                title=f"{self.bot.user.name} {online[1]}.",
                description=online[0],
                colour=await self.bot.get_embed_colour(ch),
                timestamp=datetime.datetime.utcnow(),  # This is fine
            )
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            kwargs = {"embed": embed}
        try:
            await ch.send(**kwargs)
        except discord.Forbidden as e:
            log.error("I could not send a message to the announcement channel.", exc_info=e)

    async def _send_announcement(self, *, shutdown: bool = True):
        channel = await self.config.announcement_channel()
        if not channel or not (channel := self.bot.get_channel(channel)):
            return
        shutting_down = "shutting down" if shutdown else "restarting"
        channel: discord.TextChannel
        kwargs = {"content": f"I am now {shutting_down}. {default_wave}"}
        if channel.permissions_for(channel.guild.me):
            embed = discord.Embed(
                title=f"{channel.guild.me.name} is offline.",
                colour=await self.bot.get_embed_colour(channel),
                description=f"I am now {shutting_down}. {default_wave}",
                timestamp=datetime.datetime.utcnow(),
            )
            embed.set_author(name=channel.guild.me.name, icon_url=self.bot.user.avatar_url)
            kwargs = {"embed": embed}
        try:
            await channel.send(**kwargs)
        except discord.Forbidden as e:
            log.error(
                f"I could not send the announcement channel to {channel.name} ({channel.id})",
                exc_info=e,
            )

    async def confirmation(self, ctx: commands.Context, _type: str):
        await ctx.send(f"Are you sure you want to {_type} {ctx.me.name}? (yes/no)")
        with contextlib.suppress(asyncio.TimeoutError):
            pred = MessagePredicate.yes_or_no(ctx, user=ctx.author)
            await ctx.bot.wait_for("message", check=pred, timeout=60)
            return pred.result
        return False

    @commands.Cog.listener()
    async def on_connect(self):
        if (
            self._first_connect or not await self.config.reconnect()
        ):  # This is the way Red checks this
            return  # The announcement will be sent by the _announcement_start
        await self._announce_start(reconnect=True)
