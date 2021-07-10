import contextlib

import discord
from redbot.core import Config, commands
from redbot.core.utils.chat_formatting import bold

DEFAULT_UP = "\N{UPWARDS BLACK ARROW}\N{VARIATION SELECTOR-16}"
DEFAULT_DOWN = "\N{DOWNWARDS BLACK ARROW}\N{VARIATION SELECTOR-16}"


class VoteChannel(commands.Cog):
    """
    Designate a channel(s) to have vote reactions on each post.
    """

    __author__ = ["Kreusada"]
    __version__ = "1.1.1"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 45345435, force_registration=True)
        self.config.register_guild(
            up=DEFAULT_UP,
            down=DEFAULT_DOWN,
            channels=[],
            toggled=True,
        )

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
        with contextlib.suppress(Exception):
            self.bot.remove_dev_env_value("votechannel")

    async def initialize(self) -> None:
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("votechannel", lambda x: self)

    @commands.group()
    async def vote(self, ctx):
        """Commands with VoteChannel."""

    @vote.group()
    async def channel(self, ctx):
        """Set channels where votes can take place."""

    @commands.mod_or_permissions(administrator=True)
    @channel.command()
    async def add(self, ctx, channel: discord.TextChannel):
        """Add a channel."""
        channels = await self.config.guild(ctx.guild).channels()
        channels.append(channel.id)
        await self.config.guild(ctx.guild).channels.set(channels)
        await ctx.send(f"{channel.mention} is now a voting channel.")

    @commands.mod_or_permissions(administrator=True)
    @channel.command(aliases=["del", "delete"])
    async def remove(self, ctx, channel: discord.TextChannel):
        """Remove a channel."""
        channels = await self.config.guild(ctx.guild).channels()
        if channel.id in channels:
            channels.remove(channel.id)
            await self.config.guild(ctx.guild).channels.set(channels)
            await ctx.send(f"{channel.mention} has been removed.")
        else:
            await ctx.send(f"{channel.mention} was not a voting channel.")

    @channel.command(name="list")
    async def _list(self, ctx):
        """List the current voting channels."""
        channels = await self.config.guild(ctx.guild).channels()
        if channels:
            await ctx.send(
                bold("Current channels with VoteChannel:\n")
                + ", ".join(self.bot.get_channel(c).mention for c in channels)
            )
        else:
            await ctx.send(bold("No channels are being used for VoteChannel yet."))

    @commands.mod_or_permissions(administrator=True)
    @vote.command()
    async def toggle(self, ctx):
        """Toggle VoteChannel."""
        toggled = await self.config.guild(ctx.guild).toggled()
        x = not toggled
        verb = "disabled" if toggled else "enabled"
        await self.config.guild(ctx.guild).toggled.set(x)
        await ctx.send(f"VoteChannel has been {verb}.")

    @vote.group()
    async def emoji(self, ctx):
        """Set the emojis for VoteChannel."""

    @commands.mod_or_permissions(administrator=True)
    @emoji.command()
    async def up(self, ctx, emoji: str = None):
        """
        Set the up emoji.

        If an invalid emoji is given, your vote channel will error.
        If left blank, defaults to the default up emoji.
        """
        if not emoji:
            await self.config.guild(ctx.guild).up.set(DEFAULT_UP)
            await ctx.send(f"Up reaction has been reset to `{DEFAULT_UP}`.")
        else:
            await self.config.guild(ctx.guild).up.set(emoji)
            await ctx.tick()

    @commands.mod_or_permissions(administrator=True)
    @emoji.command()
    async def down(self, ctx, emoji: str = None):
        """
        Set the down emoji.

        If an invalid emoji is given, your vote channel will error.
        If left blank, defaults to the default down emoji.
        """
        if not emoji:
            await self.config.guild(ctx.guild).down.set(DEFAULT_DOWN)
            await ctx.send(f"Down reaction has been reset to `{DEFAULT_DOWN}`.")
        else:
            await self.config.guild(ctx.guild).down.set(emoji)
            await ctx.tick()

    @emoji.command()
    async def presets(self, ctx):
        """View the current emojis for VoteChannel."""
        UP = await self.config.guild(ctx.guild).up()
        DOWN = await self.config.guild(ctx.guild).down()
        await ctx.send(f"{bold('Up Emoji: ')}{UP}\n{bold('Down Emoji: ')}{DOWN}")

    @commands.Cog.listener()
    async def on_message_without_command(self, message):
        ### We will allow bots to receive reactions here
        if not message.guild:
            return
        if not await self.config.guild(message.guild).toggled():
            return
        if message.channel.id not in await self.config.guild(message.guild).channels():
            return

        UP = await self.config.guild(message.guild).up()
        DOWN = await self.config.guild(message.guild).down()

        try:
            await message.add_reaction(UP)
            await message.add_reaction(DOWN)
        #### Seeing as we've allowed bot's to react to themselves,
        #### we now need to disable the exceptions on themselves to nullify any spam.
        except discord.Forbidden:
            if not message.author.bot:
                msg = (
                    f"{message.author.mention} Looks like I cannot add reactions to your message. "
                )
                if not message.channel.permissions_for(message.guild.me).add_reactions:
                    msg += "I do not have permissions to add reactions here."
                else:
                    msg += "You most likely have blocked me."
                return await message.channel.send(msg, delete_after=5)
        except discord.HTTPException:
            if not message.author.bot:
                return await message.channel.send(
                    "You did not enter a valid emoji in the setup.", delete_after=5
                )
