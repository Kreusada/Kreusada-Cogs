import discord
import asyncio
from redbot.core import commands
from redbot.core.utils.chat_formatting import box

CLOCK = "\N{ALARM CLOCK}"

class Reminder(commands.Cog):
  """Remind yourself for later!"""
  
  def __init__(self, bot):
    self.bot = bot
    
  @commands.group()
  async def remind(self, ctx):
    """Remind a Discord user."""
    pass

  @remind.command()
  async def me(self, ctx, hours: float, *, message: str):
    """Remind yourself for later!"""
    if hours < 1:
      hours *= 60
      timeframe = "minutes"
    else:
      hours = hours
      timeframe = "hours"
    reminder = f"{box(message, lang='cmd')}"
    await ctx.send(f"Okay {ctx.author.name}, I will remind you this in **{int(hours)} {timeframe}**!")
    time = hours * 3600
    await asyncio.sleep(time)
    embed = discord.Embed(title=f"{CLOCK} Reminder!", description=f"{ctx.author.name}, you asked me [here]({ctx.message.jump_url}) to remind you about: {reminder}", color=0xff5151)
    embed.set_footer(text=f"⏰ You asked me this {int(hours)} {timeframe} ago.")
    try: 
      await ctx.author.send(embed=embed)
    except discord.Forbidden: 
      await ctx.send(content=f"I don't have permissions to send DMs to you, so I'll send here instead, {ctx.author.mention}.", embed=embed)

  @remind.command()
  async def user(self, ctx, user_id: int, hours: float, *, message: str):
    """Remind a Discord user."""
    if hours < 1:
      hours *= 60
      timeframe = "minutes"
    else:
      hours = hours
      timeframe = "hours"
    reminder = f"{box(message, lang='cmd')}"
    user = self.bot.get_user(user_id)
    await ctx.send(f"Okay {ctx.author.name}, I will remind {user.name} about this in **{int(hours)} {timeframe}**!")
    time = hours * 3600
    await asyncio.sleep(time)
    embed = discord.Embed(title=f"{CLOCK} Reminder!", description=f"{ctx.author.name}, wanted to remind you [here]({ctx.message.jump_url}) about: {reminder}", color=0xff5151)
    embed.set_footer(text=f"{CLOCK} {ctx.author} requested this {int(hours)} {timeframe} ago.")
    try: 
      await user.send(embed=embed)
    except discord.Forbidden: 
      return await author.send(f"{user.name} does not have their DMs enabled, so I cannot send them this reminder: {reminder}\n I'm sorry!")
