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
from redbot.core.utils.chat_formatting import box, warning, error, bold


class Staff(commands.Cog):
    """
    Cog for alerting Staff.
    """

    __author__ = ["Kreusada", ]
    __version__ = "1.5.0"

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

    @staffset.command()
    @commands.admin_or_permissions(manage_guild=True)
    async def settings(self, ctx: commands.Context):
        """Show the current settings with Staff."""
        role = await self.config.guild(ctx.guild).role()
        channel = await self.config.guild(ctx.guild).channel()
        if not role:
            role = "None set."
        else:
            role = ctx.guild.get_role(role).mention
        if not channel:
            channel = "None set."
        else:
            channel = self.bot.get_channel(channel).mention
        
        await ctx.send(f"{bold('Role:')} {role}\n{bold('Channel:')} {channel}")


    @commands.command()
    @commands.cooldown(1, 600, commands.BucketType.guild)
    async def staff(self, ctx: commands.Context, reason: str = None):
        """
        Alert for the staff.
        """
        
        channel = await self.config.guild(ctx.guild).channel()
        role = await self.config.guild(ctx.guild).role()

        if not channel:
            return await ctx.send(
                error("The staff have not yet setup a staff channel.")
            )

        channel = self.bot.get_channel(channel)
        role = ctx.guild.get_role(role)

        now = datetime.now()
        date = now.strftime("%d/%m/%y")

        message_list = []
        backslash = '\n'

        async for message in ctx.channel.history(limit=6):
            author, msg = message.author, message.content.replace('`','')
            if len(msg) > 30:
                msg = msg[:30].strip(' ') + '...'
            elif not len(msg):
                msg = "[Embed, Attachment or File]"
            message_list.append(f"{str(author.display_name)}: {msg.replace(backslash, ' ')}")

        context = box('\n'.join(message for message in message_list), lang='yaml')
        reason = reason if reason else "No reason was provided."

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
            return await ctx.send("I do not have permissions to send embeds in the staff's channel.")