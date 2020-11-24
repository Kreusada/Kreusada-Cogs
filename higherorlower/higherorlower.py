import discord
import random
import asyncio
from random import randint
from discord.utils import get
from redbot.core import commands, checks, bank, Config
from redbot.core.utils.predicates import MessagePredicate

class HigherOrLower(commands.Cog):
  """Play higher or lower, win extra cash."""
  
  def __init__(self, bot):
    self.bot = bot
    self.config = Config.get_conf(
      self, identifier=5865146514315491, force_registration=True
    )
    
#  @commands.command()
#  async def holset(self, ctx):
#    """Configuration for Higher or Lower"""
#    currency = await bank.get_currency_name(ctx.guild)
#    pred = MessagePredicate.yes_or_no(ctx)
#    await ctx.send("Do you want the winner to get a role?\n Please type `yes` or `no`.")
#    try:
#      await self.bot.wait_for("message", timeout=30, check=pred)
#    except asyncio.TimeoutError:
#      return await ctx.send("You took too long there.")
#    if pred.result:
#      await ctx.send("What role should it be?")
#      role = MessagePredicate.valid_role(ctx)
#      try:
#        await self.bot.wait_for("message", timeout=30, check=role)
#      except asyncio.TimeoutError:
#        return await ctx.send("You took too long there.")
#      required = role.result
#      await self.config.guild(ctx.guild).required.set(str(required))
#      await ctx.send(
#        f"How much {currency} do you want winners to receive?"
#      )
#      predi = MessagePredicate.valid_int(ctx)
#      try:
#          await self.bot.wait_for("message", timeout=30, check=predi)
#      except asyncio.TimeoutError:
#        return await ctx.send("You took too long there.")
#      amount = predi.result
#      await self.config.guild(ctx.guild).amount.set(amount)
#      await ctx.send("Your currency payout has been set.")
#      
  @commands.command(aliases = ["hol"])
  async def higherorlower(self, ctx):
#    currency = await bank.get_currency_name(ctx.guild)
#    name_required = await self.config.guild(ctx.guild).required()
#    required = get(ctx.guild.roles, name=name_required)
#    amount = await self.config.guild(ctx.guild).amount()
    CardQuantity = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    numchoice = random.choice(CardQuantity)
    if numchoice == 1:
      await ctx.send(f"Starting with {}! Higher or lower?").format(numchoice)
    elif numchoice == 2:
      await ctx.send(f"Starting with {}! Higher or lower?").format(numchoice)
    elif numchoice == 3:
      await ctx.send(f"Starting with {}! Higher or lower?").format(numchoice)
    elif numchoice == 4:
      await ctx.send(f"Starting with {}! Higher or lower?").format(numchoice)
    elif numchoice == 5:
      await ctx.send(f"Starting with {}! Higher or lower?").format(numchoice)
    elif numchoice == 6:
      await ctx.send(f"Starting with {}! Higher or lower?").format(numchoice)
    elif numchoice == 7:
      await ctx.send(f"Starting with {}! Higher or lower?").format(numchoice)
    elif numchoice == 8:
      await ctx.send(f"Starting with {}! Higher or lower?").format(numchoice)
    elif numchoice == 9:
      await ctx.send(f"Starting with {}! Higher or lower?").format(numchoice)
    elif numchoice == 10:
      await ctx.send(f"Starting with {}! Higher or lower?").format(numchoice)
    elif numchoice == 11:
      await ctx.send(f"Starting with {}! Higher or lower?").format(numchoice)
    elif numchoice == 12:
      await ctx.send(f"Starting with {}! Higher or lower?").format(numchoice)
    elif numchoice == 13:
      await ctx.send(f"Starting with {}! Higher or lower?").format(numchoice)
    elif numchoice == 14:
      await ctx.send(f"Starting with {}! Higher or lower?").format(numchoice)
    else:
      await ctx.send("test")
    pass

          
