import asyncio
import datetime
import typing

import discord
from discord.utils import find, get
from redbot.core import Config, checks, commands
from redbot.core.bot import Red


class Counting(commands.Cog):
    """
    Make a counting channel with goals.
    """

    __version__ = "1.5.0"
    __author__ = "saurichable, Kreusada"

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1564646215646, force_registration=True)

        self.config.register_guild(
            channel=0,
            previous=0,
            goal=0,
            last=0,
            whitelist=None,
            warning=False,
            seconds=0,
            topic=True,
        )

    async def red_delete_data_for_user(self, *, requester, user_id):
        for guild in self.bot.guilds:
            if user_id == await self.config.guild(guild).last():
                await self.config.guild(guild).last.clear()

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nVersion: {self.__version__}\nAuthors: {self.__author__}"

    @checks.admin()
    @checks.bot_has_permissions(manage_channels=True, manage_messages=True)
    @commands.group(autohelp=True, aliases=["counting"])
    @commands.guild_only()
    async def countset(self, ctx: commands.Context):
        """Various Counting settings."""

    @countset.command(name="channel")
    async def countset_channel(
        self, ctx: commands.Context, channel: typing.Optional[discord.TextChannel]
    ):
        """Set the counting channel.

        If channel isn't provided, it will delete the current channel."""
        if not channel:
            await self.config.guild(ctx.guild).channel.set(0)
            return await ctx.send("Channel removed.")
        await self.config.guild(ctx.guild).channel.set(channel.id)
        goal = await self.config.guild(ctx.guild).goal()
        if await self.config.guild(ctx.guild).topic():
            await self._update_topic(channel)
        await ctx.send(f"{channel.name} has been set for counting.")

    @countset.command(name="goal")
    async def countset_goal(self, ctx: commands.Context, goal: int = 0):
        """Set the counting goal.

        If goal isn't provided, it will be deleted."""
        if not goal:
            await self.config.guild(ctx.guild).goal.clear()
            return await ctx.send("Goal removed.")
        await self.config.guild(ctx.guild).goal.set(goal)
        await ctx.send(f"Goal set to {goal}.")

    @countset.command(name="start")
    async def countset_start(self, ctx: commands.Context, number: int):
        """Set the starting number."""
        channel = ctx.guild.get_channel(await self.config.guild(ctx.guild).channel())
        if not channel:
            return await ctx.send(
                f"Set the channel with `{ctx.clean_prefix}countset channel <channel>`, please."
            )
        await self.config.guild(ctx.guild).previous.set(number)
        await self.config.guild(ctx.guild).last.clear()
        goal = await self.config.guild(ctx.guild).goal()
        next_number = number + 1
        if await self.config.guild(ctx.guild).topic():
            await self._update_topic(channel)
        await channel.send(number)
        if c_id != ctx.channel.id:
            await ctx.send(f"Counting start set to {number}.")

    @countset.command(name="reset")
    async def countset_reset(self, ctx: commands.Context, confirmation: bool = False):
        """Reset the counter and start from 0 again!"""
        if not confirmation:
            return await ctx.send(
                "This will reset the ongoing counting. This action **cannot** be undone.\n"
                f"If you're sure, type `{ctx.clean_prefix}countset reset yes`."
            )
        p = await self.config.guild(ctx.guild).previous()
        if p == 0:
            return await ctx.send("The counting hasn't even started.")
        c = ctx.guild.get_channel(await self.config.guild(ctx.guild).channel())
        if not c:
            return await ctx.send(
                f"Set the channel with `{ctx.clean_prefix}countchannel <channel>`, please."
            )
        await self.config.guild(ctx.guild).previous.clear()
        await self.config.guild(ctx.guild).last.clear()
        await c.send("Counting has been reset.")
        goal = await self.config.guild(ctx.guild).goal()
        if await self.config.guild(ctx.guild).topic():
            await self._update_topic(c)
        if c_id != ctx.channel.id:
            await ctx.send("Counting has been reset.")

    @countset.command(name="role")
    async def countset_role(self, ctx: commands.Context, role: typing.Optional[discord.Role]):
        """Add a whitelisted role."""
        if not role:
            await self.config.guild(ctx.guild).whitelist.clear()
            await ctx.send(f"Whitelisted role has been deleted.")
        else:
            await self.config.guild(ctx.guild).whitelist.set(role.id)
            await ctx.send(f"{role.name} has been whitelisted.")

    @countset.command(name="warnmsg")
    async def countset_warnmsg(
        self,
        ctx: commands.Context,
        on_off: typing.Optional[bool],
        seconds: typing.Optional[int],
    ):
        """Toggle a warning message.

        If `on_off` is not provided, the state will be flipped.
        Optionally add how many seconds the bot should wait before deleting the message (0 for not deleting).
        """
        target_state = on_off or not (await self.config.guild(ctx.guild).warning())
        await self.config.guild(ctx.guild).warning.set(target_state)
        if target_state:
            if not seconds or seconds < 0:
                seconds = 0
                await ctx.send("Warning messages are now enabled.")
            else:
                await ctx.send(
                    f"Warning messages are now enabled, will be deleted after {seconds} seconds."
                )
            await self.config.guild(ctx.guild).seconds.set(seconds)
        else:
            await ctx.send("Warning messages are now disabled.")

    @countset.command(name="topic")
    async def countset_topic(self, ctx: commands.Context, on_off: typing.Optional[bool]):
        """Toggle counting channel's topic changing.

        If `on_off` is not provided, the state will be flipped.="""
        target_state = on_off or not (await self.config.guild(ctx.guild).topic())
        await self.config.guild(ctx.guild).topic.set(target_state)
        if target_state:
            await ctx.send("Updating the channel's topic is now enabled.")
        else:
            await ctx.send("Updating the channel's topic is now disabled.")

    @countset.command(name="settings")
    async def countset_settings(self, ctx: commands.Context):
        """See current settings."""
        data = await self.config.guild(ctx.guild).all()
        channel = ctx.guild.get_channel(data["channel"])
        channel = channel.mention if channel else "None"

        goal = "None" if data["goal"] == 0 else str(data["goal"])

        role = ctx.guild.get_role(data["whitelist"])
        role = role.name if role else "None"

        warn = "Disabled" if data["warning"] else f"Enabled ({data['seconds']} s)"

        embed = discord.Embed(colour=await ctx.embed_colour(), timestamp=datetime.datetime.now())
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.title = "**__Counting settings:__**"
        embed.set_footer(text="*required to function properly")

        embed.add_field(name="Channel*:", value=channel)
        embed.add_field(name="Whitelisted role:", value=role)
        embed.add_field(name="Warning message:", value=warn)
        embed.add_field(name="Next number:", value=str(data["previous"] + 1))
        embed.add_field(name="Goal:", value=goal)
        embed.add_field(name="Topic changing:", value=str(data["topic"]))

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild or message.author.id == self.bot.user.id:
            return
        if message.channel.id != await self.config.guild(message.guild).channel():
            return
        last_id = await self.config.guild(message.guild).last()
        previous = await self.config.guild(message.guild).previous()
        seconds = await self.config.guild(message.guild).seconds()
        if message.author.id != last_id:
            try:
                current = int(message.content)
                if current - 1 == previous:
                    await self.config.guild(message.guild).previous.set(current)
                    await self.config.guild(message.guild).last.set(message.author.id)
                    if await self.config.guild(message.guild).topic():
                        return await self._update_topic(message.channel)
                    return
            except (TypeError, ValueError):
                pass
        rid = await self.config.guild(message.guild).whitelist()
        if rid:
            role = message.guild.get_role(int(rid))
            if role and role in message.author.roles:
                return
        if await self.config.guild(message.guild).warning():
            if message.author.id != last_id:
                warn_msg = await message.channel.send(
                    f"The next message in this channel must be {previous + 1}"
                )
            else:
                warn_msg = await message.channel.send(f"You cannot count twice in a row.")
            if seconds != 0:
                await asyncio.sleep(seconds)
                await warn_msg.delete()
        try:
            await message.delete()
        except (discord.Forbidden, discord.NotFound):
            pass

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.guild:
            return
        if message.channel.id != await self.config.guild(message.guild).channel():
            return
        try:
            deleted = int(message.content)
            previous = await self.config.guild(message.guild).previous()
            goal = await self.config.guild(message.guild).goal()
            if deleted == previous:
                s = str(deleted)
                if goal == 0:
                    msgs = await message.channel.history(limit=100).flatten()
                else:
                    msgs = await message.channel.history(limit=goal).flatten()
                msg = find(lambda m: m.content == s, msgs)
                if not msg:
                    p = deleted - 1
                    await self.config.guild(message.guild).previous.set(p)
                    await message.channel.send(deleted)
        except (TypeError, ValueError):
            return

    async def _update_topic(self, channel):
        goal = await self.config.guild(channel.guild).goal()
        prev = await self.config.guild(channel.guild).previous()
        if goal != 0 and prev < goal:
            await channel.edit(
                topic=f"Let's count! | Next message must be {prev + 1}! | Goal is {goal}!"
            )
        elif goal != 0 and prev == goal:
            await channel.send("We've reached the goal! :tada:")
            await channel.edit(topic=f"Goal reached! :tada:")
        else:
            await channel.edit(topic=f"Let's count! | Next message must be {prev + 1}!")
