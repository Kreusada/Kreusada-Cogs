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

  @classmethod
  def higher_or_lower(
      cls,
      ctx: Optional[commands.Context] = None,
      channel: Optional[discord.TextChannel] = None,
      user: Optional[discord.abc.User] = None,
      same_context = cls.same_context(ctx, channel, user)

  def predicate(self: MessagePredicate, m: discord.Message) -> bool:
    if not same_context(m):
      return False
    content = m.content.lower()
    if content in ("higher", "high", "h"):
      self.result = True
   elif content in ("lower", "high", "l"):
      self.result = False
   else:
      return False
    return True

    return cls(predicate)
    
  @commands.command(aliases = ["hol"])
  async def higherorlower(self, ctx):
    """Play higher or lower, win currency."""
    await ctx.send(f"Session started for **{ctx.author.name}**.")
    speccardQuan = SCQ
    cardClass = random.choice(CLASSES)
    cardQuan = random.randint(1, 14)
    roundone = cardQuan
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
    pred = MessagePredicate.higher_or_lower(ctx)
    currency = await bank.get_currency_name(ctx.guild)
    data = Embed.create(self, ctx, title=f"{roundone} of {cardClass} is your first card.",
                        description="Higher or lower? Type `higher` or `lower`.")
    await ctx.send(embed=data)
    try:
      await self.bot.wait_for("message", timeout=30, check=pred)
    except asyncio.TimeoutError:
      return await ctx.send(f"You took too long to decide. You need to start a new game using {ctx.clean_prefix}higherorlower.")
    roundtwo = random.randint(1,14)
    if pred.result:
      if roundone > roundtwo:
        await ctx.send("Testing")
      else:
        await ctx.send("Testing2")
    
          
