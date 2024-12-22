import datetime
import typing

import discord
from redbot.core import Config, commands
from redbot.core.bot import Red
from redbot.core.utils.chat_formatting import humanize_list


class Lock(commands.Cog):
    """
    Lock `@everyone` from sending messages in channels or the entire guild, and only allow Moderators to talk.
    """

    __version__ = "2.0.0"
    __author__ = "saurichable, Kreusada"

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=36546565165464, force_registration=True)

        self.config.register_guild(moderator=None, everyone=True, ignore=[])

    async def red_delete_data_for_user(self, *, requester, user_id):
        # nothing to delete
        return

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nVersion: {self.__version__}\nAuthors : {self.__author__}"

    @commands.group(autohelp=True)
    @commands.guild_only()
    @commands.admin()
    async def lockset(self, ctx: commands.Context):
        """Various Lock settings."""

    @lockset.command(name="role")
    async def lockset_role(self, ctx: commands.Context, role: discord.Role):
        """Set role that can lock channels."""
        await self.config.guild(ctx.guild).moderator.set(role.id)
        await ctx.tick()

    @lockset.command(name="perms")
    async def lockset_perms(self, ctx: commands.Context, everyone: bool):
        """Set if you use roles to access channels."""
        await self.config.guild(ctx.guild).everyone.set(not everyone)
        await ctx.tick()

    @lockset.command(name="ignore")
    async def lockset_ignore(self, ctx: commands.Context, channel: discord.TextChannel):
        """Ignore a channel during server lock."""
        if channel.id not in await self.config.guild(ctx.guild).ignore():
            async with self.config.guild(ctx.guild).ignore() as ignore:
                ignore.append(channel.id)
            return await ctx.send(
                f"{channel.mention} has been added into the ignored channels list."
            )
        await ctx.send(f"{channel.mention} is already in the ignored channels list.")

    @lockset.command(name="unignore")
    async def lockset_unignore(self, ctx: commands.Context, channel: discord.TextChannel):
        """Remove channels from the ignored list."""
        if channel.id not in await self.config.guild(ctx.guild).ignore():
            return await ctx.send(f"{channel.mention} already isn't in the ignored channels list.")
        async with self.config.guild(ctx.guild).ignore() as ignore:
            ignore.remove(channel.id)
        await ctx.send(f"{channel.mention} has been removed from the ignored channels list.")

    @lockset.command(name="settings")
    async def lockset_settings(self, ctx: commands.Context):
        """See current settings."""
        data = await self.config.guild(ctx.guild).all()
        mods = ctx.guild.get_role(data["moderator"])
        mods = "None" if not mods else mods.name

        channels = data["ignore"]
        c_text = list()
        if channels == []:
            c_text = "None"
        else:
            for channel in channels:
                c = ctx.guild.get_channel(channel)
                if c:
                    c_text.append(c.mention)
            c_text = humanize_list(c_text)

        embed = discord.Embed(colour=await ctx.embed_colour(), timestamp=datetime.datetime.now())
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.title = "**__Lock settings:__**"
        embed.set_footer(text="*required to function properly")

        embed.add_field(name="Role that can type after locking*:", value=mods, inline=False)
        embed.add_field(
            name="Using roles to access servers:*:",
            value=str(not data["everyone"]),
            inline=False,
        )
        embed.add_field(name="Ignored channels:", value=c_text, inline=False)

        await ctx.send(embed=embed)

    @commands.mod()
    @commands.bot_has_permissions(manage_channels=True)
    @commands.guild_only()
    @commands.group(invoke_without_command=True)
    async def lock(self, ctx: commands.Context):
        """Lock `@everyone` from sending messages."""
        mods = ctx.guild.get_role(await self.config.guild(ctx.guild).moderator())
        which = await self.config.guild(ctx.guild).everyone()

        if not mods:
            return await ctx.send("Uh oh. Looks like your Admins haven't setup this yet.")
        if which:
            await ctx.channel.set_permissions(
                ctx.guild.default_role, read_messages=True, send_messages=False
            )
        else:
            await ctx.channel.set_permissions(
                ctx.guild.default_role, read_messages=False, send_messages=False
            )
        await ctx.channel.set_permissions(mods, read_messages=True, send_messages=True)
        await ctx.send(":lock: Channel locked. Only Moderators can type.")

    @lock.command(name="server")
    async def lock_server(self, ctx: commands.Context, confirmation: typing.Optional[bool]):
        """Lock `@everyone` from sending messages in the entire server."""
        if not confirmation:
            return await ctx.send(
                "This will overwrite every channel's permissions.\n"
                f"If you're sure, type `{ctx.clean_prefix}lockserver yes` (you can set an alias for this so I don't ask you every time)."
            )
        async with ctx.typing():
            mods = ctx.guild.get_role(await self.config.guild(ctx.guild).moderator())
            which = await self.config.guild(ctx.guild).everyone()
            ignore = await self.config.guild(ctx.guild).ignore()

            if not mods:
                return await ctx.send("Uh oh. Looks like your Admins haven't setup this yet.")
            for channel in ctx.guild.text_channels:
                if channel.id in ignore:
                    continue
                if which:
                    await channel.set_permissions(
                        ctx.guild.default_role, read_messages=True, send_messages=False
                    )
                else:
                    await channel.set_permissions(
                        ctx.guild.default_role, read_messages=False, send_messages=False
                    )
                await channel.set_permissions(mods, read_messages=True, send_messages=True)
        await ctx.send(":lock: Server locked. Only Moderators can type.")

    @commands.mod()
    @commands.bot_has_permissions(manage_channels=True)
    @commands.guild_only()
    @commands.group(invoke_without_command=True)
    async def unlock(self, ctx: commands.Context):
        """Unlock the channel for `@everyone`."""
        mods = ctx.guild.get_role(await self.config.guild(ctx.guild).moderator())
        which = await self.config.guild(ctx.guild).everyone()

        if not mods:
            return await ctx.send("Uh oh. Looks like your Admins haven't setup this yet.")
        if which:
            await ctx.channel.set_permissions(
                ctx.guild.default_role, read_messages=True, send_messages=True
            )
        else:
            await ctx.channel.set_permissions(
                ctx.guild.default_role, read_messages=False, send_messages=True
            )
        await ctx.send(":unlock: Channel unlocked.")

    @unlock.command(name="server")
    async def unlock_server(self, ctx: commands.Context):
        """Unlock the entire server for `@everyone`"""
        async with ctx.typing():
            mods = ctx.guild.get_role(await self.config.guild(ctx.guild).moderator())
            which = await self.config.guild(ctx.guild).everyone()
            ignore = await self.config.guild(ctx.guild).ignore()

            if not mods:
                return await ctx.send("Uh oh. Looks like your Admins haven't setup this yet.")
            for channel in ctx.guild.text_channels:
                if channel.id in ignore:
                    continue
                if which:
                    await channel.set_permissions(
                        ctx.guild.default_role, read_messages=True, send_messages=True
                    )
                else:
                    await channel.set_permissions(
                        ctx.guild.default_role, read_messages=False, send_messages=True
                    )
        await ctx.send(":unlock: Server unlocked.")
