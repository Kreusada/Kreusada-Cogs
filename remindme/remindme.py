  
import discord
import asyncio
from redbot.core import commands
from redbot.core.utils.chat_formatting import box

CLOCK = "\N{ALARM CLOCK}"

class RemindMe(commands.Cog):
  """Remind yourself for later!"""
  
  def __init__(self, bot):
    self.bot = bot
    return
  
  @commands.command()
  async def remindme(self, ctx, seconds: int, *, message: str):
    """Remind yourself for later!"""
    reminder = f"{box(message, lang='cmd')}"
    await ctx.send(f"Okay {ctx.author.name}, I will remind you about this in **{seconds} seconds**!")
    await asyncio.sleep(seconds)
    embed = discord.Embed(title=f"{CLOCK} Reminder!", description=f"{ctx.author.name}, you asked me [here]({ctx.message.jump_url}) to remind you about: {reminder}", color=0xff5151)
    embed.set_footer(text=f"{CLOCK} You asked me this {seconds} seconds ago.")
    try: await ctx.author.send(embed=embed)
    except discord.Forbidden: await ctx.send(content=f"I don't have permissions to send DMs to you, so I'll send here instead, {ctx.author.mention}.", embed=embed)
