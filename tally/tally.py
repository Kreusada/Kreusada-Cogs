# This cog was built by Kreusada#0518 for user keene91#8160 over at Discord.
import discord
from redbot.core import commands, checks, Config

default_guild = {
  "COUNT": 0,
  "CHANNEL": None,
}
default_user = {
  "CONTRIBUTIONS": 0,
}

class Tally(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.config = Config.get_conf(self, 324098245, force_registration=True)
    self.config.register_guild(**default_guild)
    self.config.register_user(**default_user)
    
  @commands.group()
  @checks.admin_or_permissions(administrator=True)
  async def tallyset(self, ctx):
    """Configure settings for your server's tally."""
    
  @commands.command()
  async def tally(self, ctx, amount: float = 1):
    """Add a point to the guild's tally."""
    guildtally = await self.config.guild(ctx.guild).COUNT()
    usertally = await self.config.user(ctx.author).CONTRIBUTIONS()
    chan = await self.config.guild(ctx.guild).CHANNEL()
    channel = discord.utils.get(ctx.guild.channels, id=chan)
    guildtally += amount
    usertally += amount
    await self.config.guild(ctx.guild).COUNT.set(guildtally)
    await self.config.user(ctx.author).CONTRIBUTIONS.set(usertally)
    if not channel:
      await ctx.send(f"** +{amount} from {ctx.author.name}.**\n**{ctx.guild.name}** is now at **{guildtally}**.")
    else:
      await channel.send(f"** +{amount} from {ctx.author.name}.**\n**{ctx.guild.name}** is now at **{guildtally}**.")
      await ctx.send(f"Seeing as this is not the correct channel, I posted my response to {channel.mention}.")

  @tallyset.command()
  async def forceset(self, ctx, amount: float):
    """FORCE set custom points. Admins can only access this command."""
    sett = await self.config.guild(ctx.guild).COUNT.set(amount)
    await ctx.message.add_reaction("✅")
    await ctx.send(f"New total: **{sett}**.")
    
  @tallyset.command()
  async def reset(self, ctx):
    """Reset the guild's tally."""
    await self.config.guild(ctx.guild).COUNT.set(0)
    await ctx.message.add_reaction("✅")
    return
  
  @tallyset.command()
  async def channel(self, ctx, channel: discord.TextChannel = None):
    """Set the channel for tallies."""
    chan = await self.config.guild(ctx.guild).CHANNEL()
    await ctx.send(f"I will now only send tallies to {channel.mention}.")
    
  @commands.command()
  async def tallyboard(self, ctx):
    """Review the servers current tallyboard."""
    guildtally = await self.config.guild(ctx.guild).COUNT()
    usertally = await self.config.user(ctx.author).CONTRIBUTIONS()
    embed = discord.Embed(title=f"{ctx.guild.name}'s Tallyboard",
                          description=f"Total tally: **{guildtally}**\nLifetime contributions from you: **{usertally}**",
                          color=0xeb8a86)
    await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(Tally(bot))
