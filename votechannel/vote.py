import contextlib

import discord
from redbot.core import Config, commands
from redbot.core.utils.chat_formatting import box

DEFAULT_UP = "\N{UPWARDS BLACK ARROW}\N{VARIATION SELECTOR-16}"
DEFAULT_DOWN = "\N{DOWNWARDS BLACK ARROW}\N{VARIATION SELECTOR-16}"

_default_settings = {
    'up': DEFAULT_UP,
    'down': DEFAULT_DOWN,
    'toggled': False,
}

class VoteChannel(commands.Cog):
    """
    Designate channels to have vote reactions on each post.
    """

    __author__ = ["Kreusada"]
    __version__ = "2.0.0"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 45345435, force_registration=True)
        self.config.register_channel(**_default_settings)
        self.cache = {}
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(RuntimeError, ValueError):
                self.bot.add_dev_env_value(self.__class__.__name__.lower(), lambda _: self)

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """
        Nothing to delete
        """
        return

    def cog_unload(self):
        with contextlib.suppress(KeyError):
            self.bot.remove_dev_env_value(self.__class__.__name__.lower())

    async def initialize(self):
        self.cache = await self.config.all_channels()

    @commands.group()
    async def votechannel(self, ctx: commands.Context):
        """Commands with VoteChannel."""

    @votechannel.command(name="add")
    @commands.mod_or_permissions(administrator=True)
    async def votechannel_add(self, ctx: commands.Context, channel: discord.TextChannel):
        """Add a channel."""
        toggle = await self.config.channel(channel).toggled()
        if toggle:
            await ctx.send("This channel is already being used as a vote channel.")
        else:
            if not channel.permissions_for(ctx.me).add_reactions:
                await ctx.send("I need to be able to add reactions in that channel.")
                return
            await self.config.channel(channel).toggled.set(True)
            self.cache[channel.id] = _default_settings
            self.cache[channel.id]["toggled"] = True
            await ctx.send(f"{channel.mention} is now a vote channel.")

    @votechannel.command(name="remove", aliases=["del", "delete"])
    @commands.mod_or_permissions(administrator=True)
    async def votechannel_remove(self, ctx: commands.Context, channel: discord.TextChannel):
        """Remove a channel."""
        toggle = await self.config.channel(channel).toggled()
        if not toggle:
            await ctx.send("This channel is not already being used as a vote channel.")
        else:
            await self.config.channel(channel).toggled.set(False)
            del self.cache[channel.id]
            await ctx.send(f"{channel.mention} is no longer a vote channel.")

    @votechannel.command(name="list", aliases=["show"])
    @commands.mod_or_permissions(administrator=True)
    async def votechannel_list(self, ctx: commands.Context):
        """List the vote channels."""
        channels = []
        for channel in ctx.guild.text_channels:
            with contextlib.suppress(KeyError):
                if self.cache[channel.id]["toggled"]:
                    channels.append(channel.name)
        if not channels:
            await ctx.send("There are no vote channels.")
            return
        channels = box("\n".join(f"+ {c}" for c in channels), lang="diff")
        await ctx.send(f"**Current vote channels:**\n{channels}")

    @votechannel.command(name="upemoji")
    @commands.mod_or_permissions(administrator=True)
    async def votechannel_upemoji(self, ctx: commands.Context, channel: discord.TextChannel, emoji: str):
        """Change the up emoji for a channel."""
        try:
            await ctx.message.add_reaction(emoji)
        except discord.HTTPException:
            message = "Invalid emoji."
        else:
            toggle = await self.config.channel(channel).toggled()
            if not toggle:
                message = "This channel is not yet a vote channel."
            elif emoji == self.cache[channel.id]["down"]:
                message = "The emoji cannot be the same as the down emoji."
            else:
                message = f"Set the up emoji for {channel.mention} to \"{emoji}\"."
                await self.config.channel(channel).up.set(emoji)
                self.cache[channel.id]["up"] = emoji
        finally:
            await ctx.send(message)

    @votechannel.command(name="downemoji")
    @commands.mod_or_permissions(administrator=True)
    async def votechannel_downemoji(self, ctx: commands.Context, channel: discord.TextChannel, emoji: str):
        """Change the down emoji for a channel."""
        try:
            await ctx.message.add_reaction(emoji)
        except discord.HTTPException:
            message = "Invalid emoji."
        else:
            toggle = await self.config.channel(channel).toggled()
            if not toggle:
                message = "This channel is not yet a vote channel."
            elif emoji == self.cache[channel.id]["up"]:
                message = "The emoji cannot be the same as the up emoji."
            else:
                message = f"Set the down emoji for {channel.mention} to \"{emoji}\"."
                await self.config.channel(channel).down.set(emoji)
                self.cache[channel.id]["down"] = emoji
        finally:
            await ctx.send(message)

    @commands.Cog.listener()
    async def on_message_without_command(self, message: discord.Message):
        if message.guild is None:
            return

        if message.author.bot:
            return

        channel_perms = message.channel.permissions_for(message.guild)
        if not channel_perms.add_reactions:
            return

        if await self.bot.cog_disabled_in_guild(self, message.guild):
            return

        if not await self.bot.ignored_channel_or_guild(message):
            return

        if not await self.bot.allowed_by_whitelist_blacklist(message.author):
            return
        
        if not message.guild:
            return

        settings = self.cache[message.channel.id]

        if not self.cache[message.channel.id]["toggled"]:
            return

        for emoji in ('up', 'down'):
            await message.add_reaction(settings[emoji])
