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

    __version__ = "2.0.3"
    __author__ = "saurichable, Kreusada"

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=564154651321346431, force_registration=True)
        self.config.register_guild(channels=[], whitelist=[], time=0)

    async def red_delete_data_for_user(self, **kwargs):
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

    @galleryset.command(name="add", usage="<channels...>")
    async def galleryset_add(self, ctx: commands.Context, *channels: discord.TextChannel):
        """Add channels to the list of Gallery channels."""
        if not channels:
            await ctx.send_help()
            return

        added_channels = []
        already_in_list = []

        async with self.config.guild(ctx.guild).channels() as channel_list:
            for channel in channels:
                if channel.id not in channel_list:
                    channel_list.append(channel.id)
                    added_channels.append(channel.mention)
                else:
                    already_in_list.append(channel.mention)

        if added_channels:
            await ctx.send(f"{', '.join(added_channels)} added to the Gallery channels list.")
        if already_in_list:
            await ctx.send(f"{', '.join(already_in_list)} already in the Gallery channels list.")

    @galleryset.command(name="remove", usage="<channels...>")
    async def galleryset_remove(self, ctx: commands.Context, *channels: discord.TextChannel):
        """Remove channels from the list of Gallery channels."""
        if not channels:
            await ctx.send_help()
            return

        removed_channels = []
        not_in_list = []

        async with self.config.guild(ctx.guild).channels() as channel_list:
            for channel in channels:
                if channel.id in channel_list:
                    channel_list.remove(channel.id)
                    removed_channels.append(channel.mention)
                else:
                    not_in_list.append(channel.mention)

        if removed_channels:
            await ctx.send(f"{', '.join(removed_channels)} removed from the Gallery channels list.")
        if not_in_list:
            await ctx.send(f"{', '.join(not_in_list)} not in the Gallery channels list.")

    @galleryset.command(name="role")
    async def galleryset_role(self, ctx: commands.Context, *roles: discord.Role):
        """Add or remove whitelisted roles. 
        Running the command twice with the same role removes it from the whitelist."""
        if not roles:
            # Clear the whitelist if no roles are provided
            await self.config.guild(ctx.guild).whitelist.clear()
            await ctx.send("All whitelisted roles have been deleted.")
            return
        
        async with self.config.guild(ctx.guild).whitelist() as whitelisted_roles:
            added_roles = []
            removed_roles = []
            for role in roles:
                if role.id in whitelisted_roles:
                    whitelisted_roles.remove(role.id)
                    removed_roles.append(role.name)
                else:
                    whitelisted_roles.append(role.id)
                    added_roles.append(role.name)

        response = []
        if added_roles:
            response.append(f"Whitelisted roles added: {', '.join(added_roles)}")
        if removed_roles:
            response.append(f"Whitelisted roles removed: {', '.join(removed_roles)}")

        await ctx.send("\n".join(response))

    @galleryset.command(name="time")
    async def galleryset_time(self, ctx: commands.Context, time: commands.positive_int):
        """Set how long (in seconds!!) the bot should wait before deleting non images.
        0 to reset (default time)"""
        await self.config.guild(ctx.guild).time.set(time)
        await ctx.send(f"I will wait {time} seconds before deleting messages that are not images.")

    @galleryset.command(name="settings", aliases=["showsettings", "setting", "show"])
    async def galleryset_settings(self, ctx: commands.Context):
        """See current settings."""
        data = await self.config.guild(ctx.guild).all()
        channels = [ctx.guild.get_channel(c_id).mention for c_id in data["channels"] if ctx.guild.get_channel(c_id)]
        channels = "None" if not channels else humanize_list(channels)
        
        whitelist_roles = [ctx.guild.get_role(role_id).name for role_id in data["whitelist"] if ctx.guild.get_role(role_id)]
        whitelist_roles = "None" if not whitelist_roles else humanize_list(whitelist_roles)

        embed = discord.Embed(colour=await ctx.embed_colour(), timestamp=datetime.datetime.now())
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon)
        embed.title = "**__Gallery Settings:__**"
        embed.set_footer(text="*required to function properly")

        embed.add_field(name="Gallery channels*", value=channels)
        embed.add_field(name="Whitelisted roles", value=whitelist_roles)
        embed.add_field(name="Wait time", value=str(data["time"]))

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not message.guild:
            return

        if message.author.bot:
            return

        if message.channel.id not in await self.config.guild(message.guild).channels():
            return

        if not message.attachments:
            uris = re.findall(
                r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                message.content,
            )
            if len(uris) == 1:
                uri = "".join(uris)
                uri = uri.split("?")[0]
                parts = uri.split(".")
                extension = parts[-1]
                imageTypes = ["jpg", "jpeg", "tiff", "png", "gif", "webp", "bmp"]
                if "tenor.com" in uri or "giphy.com" in uri or "cdn.discordapp.com" in uri:
                    return
                if extension in imageTypes:
                    return

            whitelist_roles = await self.config.guild(message.guild).whitelist()
            time = await self.config.guild(message.guild).time()

            if whitelist_roles:
                user_roles = set(role.id for role in message.author.roles)
                if user_roles.intersection(whitelist_roles):
                    return

            if time != 0:
                await asyncio.sleep(time)

            try:
                await message.delete()
            except discord.Forbidden:
                log.warning("Unable to delete message in Gallery channel %s", message.channel.id)
