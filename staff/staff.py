"""
MIT License

Copyright (c) 2021 kreusada

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import discord

from datetime import datetime

from redbot.core import commands, Config

class Staff(commands.Cog):
    """
    Cog for alerting Staff.
    """

    __author__ = ["Kreusada", ]
    __version__ = "1.4.0"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 200730042020, force_registration=True)
        self.config.register_guild(role=None, channel=None)

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad."""
        context = super().format_help_for_context(ctx)
        authors = ", ".join(a for a in self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """
        Nothing to delete
        """
        return

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

    @commands.command()
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def staff(self, ctx: commands.Context, reason: str = None):
        """Notifies the staff."""
        message = ctx.message
        channel = discord.utils.get(
            ctx.guild.channels, id=await self.config.guild(ctx.guild).channel()
        )
        role = discord.utils.get(
            ctx.guild.roles, id=await self.config.guild(ctx.guild).role()
        )
        D = datetime.now().strftime("%d/%m/%y")
        if await ctx.embed_requested():
            embed = discord.Embed(
                title="Staff Attention Pending",
                description="[Click here for context]({})".format(message.jump_url),
                color=await ctx.embed_colour(),
            )
            embed.add_field(name="Member", value=ctx.author.mention, inline=True)
            embed.add_field(name="Channel", value=ctx.channel.mention, inline=True)
            embed.add_field(name="Date", value=D, inline=True)
            if reason:
                embed.add_field(name="Reason", value=reason, inline=False)
            embed.set_author(
                name=f"{ctx.author} | {ctx.author.id}", icon_url=ctx.author.avatar_url
            )
            embed.set_footer(
                text=f"{self.bot.user.name} | Staff", icon_url=self.bot.user.avatar_url
            )
            if channel:
                await ctx.tick()
                await ctx.send(
                    "We have sent a report to the staff team. They will be with you as soon as possible."
                )
                if role:
                    try:
                        return await channel.send(
                            content=f":warning: {role.mention}",
                            allowed_mentions=discord.AllowedMentions(roles=True),
                            embed=embed,
                            delete_after=43200,
                        )
                    except discord.Forbidden:
                        await ctx.send(
                            "I don't have permission to post in the staff's channel."
                        )
                else:
                    try:
                        return await channel.send(
                            allowed_mentions=discord.AllowedMentions(roles=True),
                            embed=embed,
                            delete_after=43200,
                        )
                    except discord.Forbidden:
                        await ctx.send(
                            "I don't have permission to post in the staff's channel."
                        )
            else:
                await message.add_reaction("❌")
                return await ctx.send(
                    "The staff team have not yet configured a channel."
                )
        else:
            text = (
                f"Staff Attention Pending | Conspicuous Activity :warning:\n"
                f"**User:** {ctx.author.name} ({ctx.author.id})\n**Date:** {D}\n**Channel:** {ctx.channel.mention}\n"
            )

            if reason:
                text = text + f"\n**Reason:** {reason}"
            try:
                if channel:
                    await ctx.tick()
                    await channel.send(text)
                    await ctx.send(
                        "We have sent a report to the staff team. They will be with you as soon as possible."
                    )
                else:
                    await message.add_reaction("❌")
                    return await ctx.send(
                        "The staff team have not yet configured a channel."
                    )
            except discord.Forbidden:
                await ctx.send(
                    "I don't have permission to post in the staff's channel."
                )
