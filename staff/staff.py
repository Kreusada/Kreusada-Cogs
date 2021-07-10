import contextlib
from datetime import datetime

import discord
from redbot.core import Config, commands
from redbot.core.utils.chat_formatting import bold, box, error, warning


class Staff(commands.Cog):
    """
    This cog will allow you to alert staff using a command, which will be sent
    to the specified staff channel. Provides additional details such as the last messages
    in the channel, the date, author, and more.
    """

    __author__ = ["Kreusada"]
    __version__ = "1.5.3"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 200730042020, force_registration=True)
        self.config.register_guild(role=None, channel=None)

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
            self.bot.remove_dev_env_value("staff")

    async def initialize(self) -> None:
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("staff", lambda x: self)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        staff_channel = await self.config.guild(channel.guild).channel()
        if channel.id == staff_channel:
            await self.config.guild(channel.guild).channel.clear()

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        staff_role = await self.config.guild(role.guild).role()
        if role.id == staff_role:
            await self.config.guild(role.guild).role.clear()

    @commands.group()
    async def staffset(self, ctx: commands.Context):
        """Staff notifier configuration."""

    @staffset.command()
    @commands.admin_or_permissions(manage_guild=True)
    async def channel(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """Sets the channel for staff to receive notifications."""
        if channel is None:
            await ctx.send("No channel was specified. Channel reset.")
            await self.config.guild(ctx.guild).channel.clear()
        else:
            await self.config.guild(ctx.guild).channel.set(channel.id)
            await ctx.send(
                f"{channel.mention} will now receive notifications from users to notify the staff."
            )

    @staffset.command()
    @commands.admin_or_permissions(manage_guild=True)
    async def role(self, ctx: commands.Context, role: discord.Role = None):
        """Sets the Staff role."""
        if role is None:
            await ctx.send("No role was specified. Role reset.")
            await self.config.guild(ctx.guild).role.clear()
        else:
            await self.config.guild(ctx.guild).role.set(role.id)
            await ctx.send(f"{role.mention} will now be considered as the Staff role.")

    @staffset.command()
    @commands.admin_or_permissions(manage_guild=True)
    async def settings(self, ctx: commands.Context):
        """Show the current settings with Staff."""
        role = await self.config.guild(ctx.guild).role()
        channel = await self.config.guild(ctx.guild).channel()
        role = ctx.guild.get_role(role)
        channel = self.bot.get_channel(channel)
        role = "None set." if not role else role.mention
        channel = "None set." if not channel else channel.mention
        await ctx.send(f"{bold('Role:')} {role}\n{bold('Channel:')} {channel}")

    @commands.command()
    @commands.cooldown(1, 600, commands.BucketType.guild)
    async def staff(self, ctx: commands.Context, *, reason: str = None):
        """
        Alert for the staff.
        """

        channel = await self.config.guild(ctx.guild).channel()
        role = await self.config.guild(ctx.guild).role()

        if not channel:
            return await ctx.send(error("The staff have not yet setup a staff channel."))

        channel = self.bot.get_channel(channel)
        role = ctx.guild.get_role(role)

        now = datetime.now()
        date = now.strftime("%d/%m/%y")

        message_list = []
        backslash = "\n"

        async for message in ctx.channel.history(limit=6):
            author, msg = message.author, message.content.replace("`", "")
            if len(msg) > 90:
                msg = msg[:90].strip(" ") + "..."
            elif not len(msg):
                msg = "[Embed, Attachment or File]"
            message_list.append(f"{str(author.display_name)}: {msg.replace(backslash, ' ')}")

        context = box("\n".join(message_list), lang="yaml")
        reason = reason or "No reason was provided."

        embed = discord.Embed(
            title=warning("Staff Attention Pending | Conspicuous Activity"),
            description="[Click here for context]({})".format(ctx.message.jump_url),
            color=await ctx.embed_colour(),
        )

        embed.add_field(name="Member", value=ctx.author.mention, inline=True)
        embed.add_field(name="Channel", value=ctx.channel.mention, inline=True)
        embed.add_field(name="Date", value=date, inline=True)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Context", value=context, inline=False)

        if await ctx.embed_requested():
            try:
                await channel.send(
                    allowed_mentions=discord.AllowedMentions(roles=True),
                    content=role.mention if role else None,
                    embed=embed,
                )
                await ctx.send("I have alerted the authorities, please remain calm.")
            except discord.Forbidden:
                return await ctx.send("I do not have permissions to alert the staff.")
        else:
            return await ctx.send(
                "I do not have permissions to send embeds in the staff's channel."
            )
