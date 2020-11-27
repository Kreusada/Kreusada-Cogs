import discord
import random
from redbot.core import commands, checks, Config, bank
from .mjolnirutils import lifted, failed

class Mjolnir(commands.Cog):
  """Try and lift Thor's hammer!"""
  defaults = {
    "bank": 0,
    "role": None
  }
  
  def __init__(self):
    self.config = Config.get_conf(self, 200730042020, force_registration=True)
    self.config.register_guild(**self.defaults)
    
  async def red_delete_data_for_user(self, **kwargs):
    """Nothing to delete."""
    return
  
  @commands.command(1, 300, commands.BucketType.user)
  async def trylift(self, ctx):
    """Try and lift Thor's hammer!"""
    settings = await self.config.guild(ctx.guild).all()
    currency = await bank.get_currency_name(ctx.guild)
    role = await self.config.guild(ctx.guild).role()
    bank = await self.config.guild(ctx.guild).bank()
    trylift_chance = round(random.uniform(0, 100), 2)
    if trylift_chance < 0.03:
      user = bot.get_user(ctx.author.id)
      embed = Embed.create(self, ctx, title=f"{ctx.author.name} LIFTED THE HAMMER! :hammer::zap:", description=lifted)
      await user.send(f"**{bank} {currency} was added to your bank account in {ctx.guild.name}.")
      await bank.deposit_credits(ctx.author, settings["bank"])
      await member.add_roles(settings["role"])
      await ctx.send(embed=embed)
    else:
      embed = Embed.create(self, ctx, title=f"{ctx.author.name} attempted to lift the hammer. :hammer::zap:", description=random.choice(failed))
      await ctx.send(embed=embed)
      
  @commands.group()
  async def liftset(self, ctx):
    """Mjolnir configuration."""
    
  @liftset.command()
  async def bank(self, ctx):
    """Decides whether users win currency from lifting mjolnir. Defaults to 0."""
    currency = await bank.get_currency_name(ctx.guild)
    if amount <= 0:
      return await ctx.send(f"Those who lift Thor's hammer will not be given any {currency}.")
    await self.config.guild(ctx.guild).bank.set(amount)
    await ctx.send(f"Those who lift Thor's hammer will now be given **{amount} {currency}**.")
    
  @liftset.command()
  async def role(self, ctx, role: discord.Role):
    """Decides whether users win currency from lifting mjolnir."""
    try:
      await self.config.guild(ctx.guild).set_raw("role", value=role.id)
      await ctx.send(f"{role.mention} will now be granted for those who lift Thor's hammer. :hammer:.")
    except discord.Forbidden:
      await ctx.send("Hmm, I couldn't do that. Perhaps check my permissions?")
      

