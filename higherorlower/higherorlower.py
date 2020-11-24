import discord
import random
import asyncio
from random import randint
from discord.utils import get
from .resources import SCQ, Embed
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
  @commands.command(aliases = ["hol"])
  async def higherorlower(self, ctx):
    """Play higher or lower, win currency."""
    data = Embed.create(self, ctx, title=f"Session started for **{ctx.author.name}**.")
    sessionstart = await ctx.send(embed=data)
    currency = await bank.get_currency_name(ctx.guild)
    speccardQuan = SCQ
    cardQuan = random.randint(1, 14)
    if cardQuan == 11:
      cardQuan = speccardQuan[0]
    elif cardQuan == 12:
      cardQuan = speccardQuan[1]
    elif cardQuan == 13:
      cardQuan = speccardQuan[2]
    elif cardQuan == 14:
      cardQuan = speccardQuan[3]
    elif cardQuan < 11:
      cardQuan = cardQuan
    else:
      print("Something went wrong.")
    await ctx.message.edit(sessionstart=f"{cardQuan}")

          
