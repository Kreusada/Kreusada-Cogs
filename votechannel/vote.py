import discord

from redbot.core import commands, Config
from redbot.core.utils.chat_formatting import bold


DEFAULT_UP = "\N{UPWARDS BLACK ARROW}\N{VARIATION SELECTOR-16}"
DEFAULT_DOWN = "\N{DOWNWARDS BLACK ARROW}\N{VARIATION SELECTOR-16}"


class VoteChannel(commands.Cog):
    """
    Designate a channel(s) to have vote reactions on each post.
    """

    __version__ = "1.1.0"
    __author__ = ["Kreusada"]

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
        """Thanks Sinbad."""
        return f"{super().format_help_for_context(ctx)}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """
        Nothing to delete
        """
        return

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
        x = False if toggled else True
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
        except discord.Forbidden:
            if message.author.bot:  # This is super important, as I discovered. The bot can react to it's own messages,
                pass                # And will spam this exception as a result.
            else:                   # Exceptions with bots will fall silently.
                return await message.channel.send(
                    "I am missing permissions to add reactions to the messages here."
                )
        except discord.HTTPException:
            if message.author.bot:  # This is super important, as I discovered. The bot can react to it's own messages,
                pass                 # And will spam this exception as a result.
            else:                    # Exceptions with bots will fall silently.
                return await message.channel.send(
                    "You did not enter a valid emoji in the setup."
                )
