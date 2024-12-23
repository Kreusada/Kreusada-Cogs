import asyncio
import datetime
import logging
import re
import typing

import discord
from redbot.core import Config, commands
from redbot.core.bot import Red
from redbot.core.utils.chat_formatting import humanize_list

log = logging.getLogger("red.kreusada-cogs.gallery")


class Gallery(commands.Cog):
    """
    Set channels as galleries, deleting all messages that don't contain any attachments.
    """

    __version__ = "2.0.1"
    __author__ = "saurichable, Kreusada"

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=564154651321346431, force_registration=True)

        self.config.register_guild(channels=[], whitelist=None, time=0)

    async def red_delete_data_for_user(self, **kwargs):
        # nothing to delete
        return

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nVersion: {self.__version__}\nAuthors: {self.__author__}"

    @commands.group()
    @commands.guild_only()
    @commands.admin()
    @commands.bot_has_permissions(manage_messages=True)
    async def galleryset(self, ctx: commands.Context):
        """Various Gallery settings."""

    @galleryset.command(name="add")
    async def galleryset_add(self, ctx: commands.Context, channel: discord.TextChannel):
        """Add a channel to the list of Gallery channels."""
        if channel.id not in await self.config.guild(ctx.guild).channels():
            async with self.config.guild(ctx.guild).channels() as channels:
                channels.append(channel.id)
            await ctx.send(f"{channel.mention} has been added into the Gallery channels list.")
        else:
            await ctx.send(f"{channel.mention} is already in the Gallery channels list.")

    @galleryset.command(name="remove")
    async def galleryset_remove(self, ctx: commands.Context, channel: discord.TextChannel):
        """Remove a channel from the list of Gallery channels."""
        if channel.id in await self.config.guild(ctx.guild).channels():
            async with self.config.guild(ctx.guild).channels() as channels:
                channels.remove(channel.id)
            await ctx.send(f"{channel.mention} has been removed from the Gallery channels list.")
        else:
            await ctx.send(f"{channel.mention} isn't in the Gallery channels list.")

    @galleryset.command(name="role")
    async def galleryset_role(self, ctx: commands.Context, role: typing.Optional[discord.Role]):
        """Add or remove a whitelisted role."""
        if not role:
            await self.config.guild(ctx.guild).whitelist.clear()
            await ctx.send("Whitelisted role has been deleted.")
        else:
            await self.config.guild(ctx.guild).whitelist.set(role.id)
            await ctx.send(f"{role.name} has been whitelisted.")

    @galleryset.command(name="time")
    async def galleryset_time(self, ctx: commands.Context, time: commands.positive_int):
        """Set how long (in seconds!!) the bot should wait before deleting non images.

        0 to reset (default time)"""
        await self.config.guild(ctx.guild).time.set(time)
        await ctx.send(f"I will wait {time} seconds before deleting messages that are not images.")

    @galleryset.command(name="settings")
    async def galleryset_settings(self, ctx: commands.Context):
        """See current settings."""
        data = await self.config.guild(ctx.guild).all()

        channels = []
        for c_id in data["channels"]:
            c = ctx.guild.get_channel(c_id)
            if c:
                channels.append(c.mention)
        channels = "None" if channels == [] else humanize_list(channels)

        role = ctx.guild.get_role(data["whitelist"])
        role = "None" if not role else role.name

        embed = discord.Embed(colour=await ctx.embed_colour(), timestamp=datetime.datetime.now())
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
        embed.title = "**__Unique Name settings:__**"
        embed.set_footer(text="*required to function properly")

        embed.add_field(name="Gallery channels:", value=channels)
        embed.add_field(name="Whitelisted role:", value=role)
        embed.add_field(name="Wait time:", value=str(data["time"]))

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not message.guild:
            return
        if message.channel.id not in await self.config.guild(message.guild).channels():
            return
        if not message.attachments:
            uris = re.findall(
                "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                message.content,
            )
            if len(uris) == 1:
                uri = "".join(uris)
                uri = uri.split("?")[0]
                parts = uri.split(".")
                extension = parts[-1]
                imageTypes = ["jpg", "jpeg", "tiff", "png", "gif", "bmp"]
                if extension in imageTypes:
                    return
            rid = await self.config.guild(message.guild).whitelist()
            time = await self.config.guild(message.guild).time()
            if rid:
                role = message.guild.get_role(int(rid))
                if role and role in message.author.roles:
                    return
            if time != 0:
                await asyncio.sleep(time)
            try:
                await message.delete()
            except discord.Forbidden:
                log.warning("Unable to delete message in Gallery channel %s", message.channel.id)
