from typing import Literal, Optional

import discord
from redbot.core import Config, commands
from redbot.core.bot import Red

ENABLE_CONFIRMATION_MESSAGE = (
    "Successfully *enabled* deletion of {type} messages in {channel.mention}. "
)
ENABLE_CONFIRMATION_WITH_PERMS = "Messages sent by {type}s will be deleted with a delay of {delay} seconds. Ensure that I retain sufficient permissions to delete messages."
ENABLE_CONFIRMATION_WITHOUT_PERMS = "However, I do not currently have sufficient permissions to delete messages in {channel.mention}."

DISABLE_CONFIRMATION_MESSAGE = "Successfully *disabled* deletion of {type} messages in {channel.mention}. Messages sent by {type}s will no longer be deleted."


class MessageDeleter(commands.Cog):
    """Delete messages from users and bots, inclusively or exclusively, in text channels."""

    __version__ = "1.0.0"
    __author__ = "Kreusada"

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, 719988449867989142, force_registration=True)
        self.config.register_guild(channels={})

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    async def enable_for(
        self, *, type: Literal["bots", "humans"], channel: discord.TextChannel, delay: int
    ):
        cid = str(channel.id)
        async with self.config.guild(channel.guild).channels() as channels:
            if cid not in channels:
                channels[cid] = {"bots": False, "humans": False}
            channels[cid][type] = delay
        if not channel.permissions_for(channel.guild.me).manage_messages:
            return False
        return True

    async def enable_for(
        self, *, type: Literal["bots", "humans"], channel: discord.TextChannel, delay: int
    ):
        cid = str(channel.id)
        channels = await self.config.guild(channel.guild).channels()
        if cid not in channels:
            channels[cid] = {"bots": False, "humans": False}
        channels[cid][type] = delay
        await self.config.guild(channel.guild).channels.set(channels)
        if not channel.permissions_for(channel.guild.me).manage_messages:
            return False
        return True

    async def disable_for(self, *, type: Literal["bots", "humans"], channel: discord.TextChannel):
        cid = str(channel.id)
        channels = await self.config.guild(channel.guild).channels()
        if cid in channels:
            channels[cid][type] = False
        if all(mode is False for mode in channels[cid].values()):  # config cleanup
            del channels[cid]
        await self.config.guild(channel.guild).channels.set(channels)

    @staticmethod
    def get_confirmation_message(can_delete_messages: bool):
        message = ENABLE_CONFIRMATION_MESSAGE
        if not can_delete_messages:
            message += ENABLE_CONFIRMATION_WITHOUT_PERMS
        else:
            message += ENABLE_CONFIRMATION_WITH_PERMS
        return message

    @commands.group()
    @commands.guild_only()
    @commands.mod_or_permissions(manage_messages=True)
    async def msgdeleter(self, ctx: commands.Context):
        """Commands to configure MessageDeleter."""

    @msgdeleter.command(name="settings")
    async def msgdeleter_settings(self, ctx: commands.Context):
        """Shows the current settings for MessageDeleter in this guild."""
        channels = await self.config.guild(ctx.guild).channels()
        message = "## Settings for MessageDeleter in this guild\n"
        has_settings = False
        for cid, settings in channels.items():
            has_settings = True
            line = f"- {ctx.guild.get_channel(int(cid)).mention} -"
            bot_settings = settings["bots"]
            if bot_settings is not False:
                if bot_settings == 0:
                    line += " Messages sent by bots are **instantly** deleted."
                else:
                    line += f" Messages sent by bots are deleted after **{bot_settings}** seconds."
            human_settings = settings["humans"]
            if human_settings is not False:
                if human_settings == 0:
                    line += " Messages sent by humans are **instantly** deleted."
                else:
                    line += (
                        f" Messages sent by humans are deleted after **{human_settings}** seconds."
                    )
            message += line + "\n"
        await ctx.send(message if has_settings else "No settings to show.")

    @msgdeleter.command(name="reset")
    async def msgdeleter_reset(self, ctx: commands.Context):
        """Reset MessageDeleter in this guild."""
        await self.config.guild(ctx.guild).channels.clear()
        await ctx.send("MessageDeleter successfully reset.")

    @msgdeleter.group(name="bots", aliases=["bot"])
    async def msgdeleter_bots(self, ctx: commands.Context):
        """Enable or disable deletion of bot messages."""

    @msgdeleter_bots.command(name="enable")
    async def msgdeleter_bots_enable(
        self,
        ctx: commands.Context,
        channel: discord.TextChannel,
        delay: Optional[commands.Range[int, None, 10]] = 0,
    ):
        """Enable deletion of bot messages in a text channel."""
        can_delete_messages = await self.enable_for(type="bots", channel=channel, delay=delay)
        await ctx.send(
            self.get_confirmation_message(can_delete_messages).format(
                type="bot",
                channel=channel,
                delay=str(delay),
            )
        )

    @msgdeleter_bots.command(name="disable")
    async def msgdeleter_bots_disable(self, ctx: commands.Context, channel: discord.TextChannel):
        """Disable deletion of bot messages in a text channel."""
        await self.disable_for(type="bots", channel=channel)
        await ctx.send(DISABLE_CONFIRMATION_MESSAGE.format(type="bot", channel=channel))

    @msgdeleter.group(name="humans", aliases=["human", "users", "user", "members", "member"])
    async def msgdeleter_humans(self, ctx: commands.Context):
        """Enable or disable deletion of human messages."""

    @msgdeleter_humans.command(name="enable")
    async def msgdeleter_humans_enable(
        self,
        ctx: commands.Context,
        channel: discord.TextChannel,
        delay: Optional[commands.Range[int, None, 10]] = 0,
    ):
        """Enable deletion of human messages in a text channel."""
        can_delete_messages = await self.enable_for(type="humans", channel=channel, delay=delay)
        await ctx.send(
            self.get_confirmation_message(can_delete_messages).format(
                type="human",
                channel=channel,
                delay=str(delay),
            )
        )

    @msgdeleter_humans.command(name="disable")
    async def msgdeleter_humans_disable(self, ctx: commands.Context, channel: discord.TextChannel):
        """Disable deletion of human messages in a text channel."""
        await self.disable_for(type="humans", channel=channel)
        await ctx.send(DISABLE_CONFIRMATION_MESSAGE.format(type="human", channel=channel))

    @commands.Cog.listener("on_message")
    async def message_deleter_listener(self, message: discord.Message):
        if message.guild is None:
            return
        if not message.channel.permissions_for(message.guild.me).manage_messages:
            return
        if await self.bot.cog_disabled_in_guild(self, message.guild):
            return
        if not await self.bot.ignored_channel_or_guild(message):
            return
        if not await self.bot.allowed_by_whitelist_blacklist(message.author):
            return

        config = await self.config.guild(message.guild).channels()
        if (mcid := str(message.channel.id)) not in config:
            return
        setting = config[mcid]["bots" if message.author.bot else "humans"]
        if setting is False:
            return
        await message.delete(delay=setting)
