import discord
import random
import asyncio
from random import randint
from discord.utils import get
from redbot.core import commands, checks, bank, Config
from redbot.core.utils.predicates import MessagePredicate
from .rtbresources import Embed

class RobTheBank(commands.Cog):
  """Rob the bank, gain or get fined!"""
  defaults = {
    "Fine": 400,
    "Deposit": 400,
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
  @commands.cooldown(1, 300, commands.BucketType.user)
  async def rob(self, ctx):
    """Attempt to rob the bank. Attempt."""
    settings = await self.config.guild(ctx.guild).all()
    numbers = [1,2,3,4,5,6]
    numbersrand = random.choice(numbers)
    yestatus = f"<:dollarbag:778687019944771616> {ctx.author.name} successfully robbed the bank."
    nostatus = f"<:dollarbag:778687019944771616> {ctx.author.name} failed, dismally."
    currency = await bank.get_currency_name(ctx.guild)
    deposit = await self.config.guild(ctx.guild).Deposit()
    fine = await self.config.guild(ctx.guild).Fine()
    subt = f"<:success:777167188816560168> {fine} {currency} has been withdrawn from your bank account."
    incr = f"<:success:777167188816560168> {deposit} {currency} has been added into your bank account."
    no = [
      f"Oh I caught you red handed there!\n **You have been fined {fine} {currency}.**\n\n {subt}",
      f"Get some good detective skills before trying to rob my bank!\n **You have been fined {fine} {currency}.**\n\n {subt}",
      f"Oh, its you again... {ctx.author.name} is it?\n **You have been fined {fine} {currency}.**\n\n {subt}"
    ]
    yes = [
      f":loudspeaker: Dispatch, we've lost the suspect.\n **You have earnt yourself {deposit} {currency}!**\n\n {incr}",
      f"Looks like {ctx.author.name} made it out alive, somehow...\n **You have earnt yourself {deposit} {currency}!**\n\n {incr}",
      f"We let you loose on purpose, we really did.\n **You have earnt yourself {deposit} {currency}!**\n\n {incr}"
    ]
    if numbersrand > 4:
      title = nostatus
      description = random.choice(no).format(currency)
      await bank.withdraw_credits(ctx.author, settings["Fine"])
    else:
      title = yestatus
      description = random.choice(yes).format(currency)
      await bank.deposit_credits(ctx.author, settings["Deposit"])
    data = Embed.create(self, ctx, title=title, description=description)
    await ctx.send(embed=data)
    
  @commands.group()
  @checks.mod()
  async def robset(self, ctx):
    """Configurations for robbing the bank."""
    
  @robset.command()
  async def deposit(self, ctx, amount: int):
    """
    Set the amount you can steal from the bank.
    Odds for and against acquiring money are 50/50.
    The default value for deposits are: `400`.
    We don't recommend going much higher than this.
    """
    if amount < 0:
      return await ctx.send("You wouldn't be robbing a bank if you didn't get any money!\n"
                            "Please enter a number equal to or greater than `1`.")
    await self.config.guild(ctx.guild).Deposit.set(amount)
    currency = await bank.get_currency_name(ctx.guild)
    await ctx.send(f"Deposits will now distribute **{amount} {currency}.**")

  @robset.command()
  async def fine(self, ctx, amount: int):
    """
    Set the amount you can get fined for from the bank.
    Odds for and against acquiring money are 50/50.
    The default value for fines are: `400`.
    We don't recommend going much higher than this.
    """
    if amount < 0:
      return await ctx.send("That's not how fines work :joy:\nPlease enter a number equal to or greater than `1`.")
    await self.config.guild(ctx.guild).Fine.set(amount)
    currency = await bank.get_currency_name(ctx.guild)
    await ctx.send(f"Fines will now withdraw **{amount} {currency}.**")
    
  @robset.command()
  async def showsettings(self, ctx):
    """Shows the current settings for RobTheBank."""
    fin = await self.config.guild(ctx.guild).Fine()
    deposi = await self.config.guild(ctx.guild).Deposit()
    if fin == 400 and deposi == 400:
      s = "Standard"
    else:
      s = "Customized"
    embed = Embed.create(self, ctx, title=f"{ctx.guild.name} Settings",
                         description=(
                           f"Deposit: **{deposi}**\n"
                           f"Fine: **{fin}**\n"
                           f"Settings: **{s}**"
                         )
                        )
    await ctx.send(embed=embed)
      
      
