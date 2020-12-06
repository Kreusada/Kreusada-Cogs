import discord
from datetime import datetime, timedelta
from redbot.core import commands, Config, checks


class ModMail(commands.Cog):
    """This cog allows you to see any dms your bot receives"""

    default_global = {
        "channel": None,
        "role": None
    }

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(
            self, 12386760762, force_registration=True)
        self.config.register_global(**self.default_global)
        
    @commands.group()
    @checks.admin_or_permissions(manage_guild=True)
    async def modmailset(self, ctx):
        """Configure your modmail."""
        return
    
    @modmailset.command()
    async def channel(self, ctx, channel: discord.TextChannel):
        """Sets the channel to receive notifications."""
        await self.config.guild(ctx.guild).set_raw("channel", value=channel.id)
        embed = discord.Embed(
            self, ctx, title="Successful",
            description=f"{channel.mention} will now receive notifications from users who use the modmail."
        )
        await ctx.send(embed=embed)
        
    @modmailset.command()
    async def role(self, ctx, role: discord.Role):
        """Sets an optional role to be pinged for modmail."""
        try:
            await self.config.guild(ctx.guild).set_raw("role", value=role.id)
            embed = discord.Embed(
                self, ctx, title="Successful",
                description=f"`{role.mention}` will now be mentioned for modmail alerts.",
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = Embed.create(
                self, ctx, title="Oopsies!",
                description=f"Something went wrong during the setup process."
            )
            await ctx.send(embed=embed)
            return
        return
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if not isinstance(message.channel, discord.DMChannel):
            return
        if message.author.bot:
            return
        app = await self.bot.application_info()
        if message.author.id == app.owner.id:
            return
        channel = self.bot.get_channel(await self.config.get_raw("channel"))
        role = self.bot.get_role(await self.config.get_raw("role"))
        if not message.content[0] in await self.bot.get_prefix(message) and channel is not None:
            embed = discord.Embed(self, message, title="Mod Mail 📬", description=message.content)
            await channel.send(embed=embed)
        
