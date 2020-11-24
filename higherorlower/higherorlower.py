import discord
import random
import asyncio
from random import randint
from discord.utils import get
from .resources import SCQ, CLASSES, Embed
from redbot.core import commands, checks, bank, Config
from redbot.core.utils.predicates import MessagePredicate

class HigherOrLower(commands.Cog):
  """Play higher or lower, win extra cash."""
  
  def __init__(self, bot):
    self.bot = bot
    self.config = Config.get_conf(
      self, identifier=5865146514315491, force_registration=True
    )
    
  @commands.command(aliases = ["hol"])
  async def higherorlower(self, ctx):
    """Play higher or lower, win currency."""
    await ctx.send(f"Session started for **{ctx.author.name}**.")
    currency = await bank.get_currency_name(ctx.guild)
    speccardQuan = SCQ
    cardClass = random.choice(CLASSES)
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
    data = Embed.create(self, ctx, title=f"{cardQuan} of {cardClass} is your first card.",
                        description="Higher or lower? Type `h` or `l`.")
    session = await ctx.send(embed=data)
    
  @commands.Cog.listener()
  async def on_message(self, message):
    if message.content.startswith('h'):
      channel = message.channel
      await bot.wait_for(session)
      await channel.send("Test")
          
