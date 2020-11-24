import discord
import random
import asyncio
from random import randint
from discord.utils import get
from redbot.core import commands, checks, bank, Config
from redbot.core.utils.predicates import MessagePredicate
from .rtbresources import Embed, RESU, UNSUCRESP, SUCRESP

class RobTheBank(commands.Cog):
  """Rob the bank, gain or get fined!"""
  defaults = {
    "Fine": 400,
    "Deposti": 400,
  }

  def __init__(self, bot):
    self.bot = bot
    self.config = Config.get_conf(
      self, identifier=5865146514315491, force_registration=True
    )
    self.config.register_guild(**self.defaults)

  async def red_delete_data_for_user(self, **kwargs):
      """Nothing to delete."""
      return
   
  @commands.command()
#  @commands.cooldown(1, 300, commands.BucketType.user)
  async def rob(self, ctx):
    """Attempt to rob the bank. Attempt."""
    resu = random.randint[1,2,3,4,5,6]
    status = f"{ctx.author.name} attempted to rob the bank..."
    if resu > 4:
      title = status
      description = random.choice(UNSUCRESP)
      await bank.withdraw_credits(ctx.author, settings["Fine"])
    else:
      title = status
      description = random.choice(SUCRESP)
      await bank.deposit_credits(ctx.author, settings["Deposti"])
    data = Embed.create(self, ctx, title=title, description=description)
    await ctx.send(embed=data)
    
  @commands.group()
  async def robset(self, ctx):
    """Configurations for robbing the bank."""
    
  @robset.command()
  async def deposit(self, ctx, amount: int):
    """Set the amount you can steal from the bank."""
    if amount < 0:
      return await ctx.send("You wouldn't be robbing a bank if you didn't get any money!\n"
                            "Please enter a number equal to or greater than `1`.")
    await self.config.guild(ctx.guild).Deposti.set(amount)
    currency = await bank.get_currency_name(ctx.guild)
    await ctx.send(f"Deposits will now distribute **{amount} {currency}.**")

  @robset.command()
  async def fine(self, ctx, amount: int):
    """Set the amount users could be fined for."""
    if amount < 0:
      return await ctx.send("That's not how fines work :joy:\nPlease enter a number equal to or greater than `1`.")
    await self.config.guild(ctx.guild).Fine.set(amount)
    currency = await bank.get_currency_name(ctx.guild)
    await ctx.send(f"Fines will now withdraw **{amount} {currency}.**")
    
      
      
