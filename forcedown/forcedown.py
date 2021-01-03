import discord
from datetime import datetime, timedelta
from redbot.core import bank, commands, checks, Config

default_user = {
  "forcedown": 100,
}

default_guild = {
  "bank": 10000,
  "forcedownguild": 100,
  "quantity": 1
}

# ForceDown was a custom game requested by Pootle on Discord. Thanks Pootle!
  
class ForceDown(commands.Cog):
  """
  ForceDown: Get your number to 0 to win some cash!
  ForceDown is a came which involves lowering your number to 0, to win currency.
  """
  
  def __init__(self, bot):
    self.bot = bot
    self.config = Config.get_conf(self, 348736583543, force_registration=True)
    self.config.register_user(**default_user)
    self.config.register_guild(**default_guild)

  async def red_delete_data_for_user(self, **kwargs):
      """
      Nothing to delete
      """
      return
    
  @commands.command()
  @commands.cooldown(1, 600, commands.BucketType.user)
  async def fd(self, ctx):
    """Forcedown your total to zero!"""
    now = datetime.now()
    strftime = now.strftime("Today at %H:%M %p")
    forcedown = await self.config.user(ctx.author).forcedown()
    quantity = await self.config.guild(ctx.guild).quantity()
    forcedownguild = await self.config.guild(ctx.guild).forcedownguild()
    negative = forcedownguild - quantity
    if forcedown > 0:
      embed = discord.Embed(title=":white_check_mark: Forcedown Successful",
                            description=(
                              f"Previous amount: {forcedown}\n"
                              f"Guild quantity settings: -{quantity}\n"
                              f"New total: **{negative}**"
                            ), color=0xff5151)
      embed.set_footer(text=strftime)
      await self.config.user(ctx.author).forcedown.set(negative)
      await ctx.send(embed=embed)
    else:
      await ctx.send(f"You've reached **0**! Now its time to use `{ctx.clean_prefix}fdclaim`.")
    
  @commands.command()
  async def fdclaim(self, ctx):
    """Claim your prizes and reset your total!"""
    currency = await bank.get_currency_name(ctx.guild)
    forcedown = await self.config.user(ctx.author).forcedown()
    banktot = await self.config.guild(ctx.guild).bank()
    forcedownguild = await self.config.guild(ctx.guild).forcedownguild()
    if forcedown <= 0:
      await self.config.user(ctx.author).forcedown.set(forcedownguild)
      await ctx.send(
        f"Hooray {ctx.author.name}! **{banktot} {currency}** have been added to your bank account.\n"
        f"Your forcedown total has been reset to **{forcedownguild}**."
      )
    else:
      await ctx.send(
        f"Not yet {ctx.author.name}. You still have {forcedown} left to forcedown."
      )
      return
    return
  
  @commands.group()
  async def fdset(self, ctx):
    """Settings for forcedown."""
    
  @fdset.command()
  async def reduction(self, ctx, amount: int):
    """Set the quantity deducted from forcedown."""
    await self.config.guild(ctx.guild).quantity.set(amount)
    await ctx.send(f"Done! Running `{ctx.clean_prefix}fd` will now deduct **{amount}** from their total.")
    
  @fdset.command()
  async def start(self, ctx, amount: int):
    """Set the starting quantity for forcedown."""
    await self.config.guild(ctx.guild).forcedownguild.set(amount)
    await ctx.send(f"Done! Users will now start with a forcedown of **{amount}**.")

  @fdset.command()
  async def bank(self, ctx, amount: int):
    """Set the bank payout for forcedown. Default = 10000"""
    await self.config.guild(ctx.guild).bank.set(amount)
    currency = await bank.get_currency_name(ctx.guild)
    await ctx.send(f"Done! Running `{ctx.clean_prefix}fdclaim` will now deposit **{amount}** {currency}")

  @fdset.command()
  async def settings(self, ctx):
    """See all the settings for forcedown."""
    forcedown = await self.config.user(ctx.author).forcedown()
    bank = await self.config.guild(ctx.guild).bank()
    forcedownguild = await self.config.guild(ctx.guild).forcedownguild()
    quantity = await self.config.guild(ctx.guild).quantity()
    embed = discord.Embed(title=f":gear: Settings for {ctx.guild.name}",
                          description=(
                            f"{ctx.author}'s current amount: **{forcedown}**\n\n"
                            f"Bank deposit: **{bank}**\n"
                            f"Forcedown starting number: **{forcedownguild}**\n"
                            f"Forcedown reduction number: **{quantity}**"
                          ), color=0xff5151)
    await ctx.send(embed=embed)

