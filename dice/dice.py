import random
import discord
from redbot.core import commands

D = "\N{GAME DIE}"
class Dice(commands.Cog):
  """Roll dice with your own amount of sides."""
  
  def __init__(self, bot):
    self.bot = bot
    
  @commands.command()
  async def dice(self, ctx, number_of_sides: int):
    """Roll a dice."""
    nos = number_of_sides
    if nos > 100:
      await ctx.send("You can't roll above 100!")
    else:
      embed = discord.Embed(title=f"{ctx.author.name} rolls a {nos} sided dice.",
                            description=f"You rolled for {random.randint(1, nos)}. {D}",
                            color=0xe15d59)
      await ctx.send(embed=embed)
