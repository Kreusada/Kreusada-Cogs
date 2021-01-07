import discord
import asyncio
from datetime import datetime, timedelta
from redbot.core import commands, checks, Config, modlog


class Staff(commands.Cog):
    """Cog for alerting Staff."""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(
            self, 200730042020, force_registration=True)
        self.config.register_guild(role=None, channel=None)

    async def red_delete_data_for_user(self, **kwargs):
        """
        Nothing to delete
        """
        return

    @commands.group()
    async def staffset(self, ctx):
        """Staff notifier configuration."""

    @staffset.command()
    @checks.admin_or_permissions(manage_guild=True)
    async def channel(self, ctx, channel: discord.TextChannel = None):
        """Sets the channel for staff to receive notifications."""
        if channel is None:
            await ctx.send("No channel was specified. Channel reset.")
            await self.config.guild(ctx.guild).channel.set(None)
        else:
            await self.config.guild(ctx.guild).channel.set(channel.id)
            embed = discord.Embed(
                title="Successful :white_check_mark:",
                description=f"{channel.mention} will now receive notifications from users to notify the staff."
            )
            await ctx.send(embed=embed)

    @staffset.command()
    @checks.admin_or_permissions(manage_guild=True)
    async def role(self, ctx, role: discord.Role = None):
        """Sets the Staff role."""
        if role is None:
            await ctx.send("No role was specified. Role reset.")
            await self.config.guild(ctx.guild).role.set(None)
        else:
            try:
                await self.config.guild(ctx.guild).role.set(role.id)
                embed = discord.Embed(
                    title="Successful :white_check_mark:",
                    description=f"{role.mention} will now be considered as the Staff role.",
                )
                await ctx.send(embed=embed)
            except discord.Forbidden:
                embed = discord.Embed(
                    title="Oopsies! :x:",
                    description=f"Something went wrong during the setup process."
                )
                await ctx.send(embed=embed)
        
    @commands.command()
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def staff(self, ctx, reason: str = None):
        """Notifies the staff."""
        message = ctx.message
        channel = discord.utils.get(ctx.guild.channels, id=await self.config.guild(ctx.guild).channel())
        role = discord.utils.get(ctx.guild.roles, id=await self.config.guild(ctx.guild).role())
        jumper_f = "[Click here for context]({})".format(ctx.message.jump_url)
        now = datetime.now()
        D = now.strftime("%d/%m/%y")
        embed = discord.Embed(
            title="Staff Attention Pending",
            description="[Click here for context]({})".format(ctx.message.jump_url),
            color=await ctx.embed_colour()
        )
        embed.add_field(name="Member", value=ctx.author.mention, inline=True)
        embed.add_field(name="Channel", value=ctx.channel.mention, inline=True)
        embed.add_field(name="Date", value=D, inline=True)
        if reason is not None:
            embed.add_field(name="Reason", value=reason, inline=False)
        else:
            pass
        embed.set_author(name=f"{ctx.author} | {ctx.author.id}", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{self.bot.user.name} | Staff", icon_url=self.bot.user.avatar_url)
        if channel is not None:
            await message.add_reaction("✅")
            await ctx.send("We have sent a report to the staff team. They will be with you as soon as possible.")
            if role is not None:
                return await channel.send(content=f":warning: {role.mention}", allowed_mentions=discord.AllowedMentions(roles=True), embed=embed, delete_after=43200)
            else:
                await channel.send(allowed_mentions=discord.AllowedMentions(roles=True), embed=embed, delete_after=43200)
            return
        else:
            await message.add_reaction("❌")
            return await ctx.send("The staff team have not yet configured a channel.")
