import discord
import asyncio
from redbot.core import commands
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.predicates import ReactionPredicate

class FestiveCards(commands.Cog):
  """Send someone a christmas card!"""
  
  def __init__(self, bot):
    self.bot = bot

  @commands.group()
  async def card(self, ctx):
    """Send a christmas card to someone!"""
      
  @card.group()
  async def send(self, ctx):
    """Send a card to someone!"""
  
  @card.group(autohelp=False, invoke_without_command=True)
  async def viewoutput(self, ctx):
    """Send a template version to your DM!"""
    await ctx.send(
      "Which card type would you like to see? Please run one of the following commands.\n"
      "This message will be deleted after **20 seconds**.\n"
      f"\n`❄️`: `{ctx.clean_prefix}card viewoutput christmas`"
      f"\n`🎂`: `{ctx.clean_prefix}card viewoutput birthday`"
      f"\n`🏥`: `{ctx.clean_prefix}card viewoutput getwellsoon`",
    delete_after=20)
    
  @viewoutput.command()
  async def christmas(self):
    author = ctx.author.name
    foot = (f"Send christmas cards using {ctx.clean_prefix}card!")
    e = discord.Embed(title=f":christmas_tree: Christmas Card from {ctx.author} :christmas_tree:",
                      description="Dear `Username`,\n\n`Your message will go here`\n\nFrom {} :gift:".format(author),
                      colour=discord.Colour.red())
    e.set_footer(text=foot)
    try:
      await author.send(embed=e)
    except discord.HTTPException:
      await ctx.send("Your DMs are turned off, or I don't have permissions to DM you.")
    else:
      await ctx.send("I sent a test message to your DMs!")
    

  @card.command()
  async def christmas(self, ctx: commands.Context, user_id: int, *, message: str):
    """Send a christmas card to someone!"""
    destination = self.bot.get_user(user_id)
    author = ctx.author.name
    user = destination
    if destination is None or destination.bot:
        await ctx.send("Invalid ID, user not found, or user is a bot.")
    foot = (f"Send christmas cards using {ctx.clean_prefix}card!")
    e = discord.Embed(title=f":christmas_tree: Christmas Card from {ctx.author} :christmas_tree:", 
                      description= "Dear {},\n\n{}\n\nFrom {} :gift:".format(user.name, message, author), 
                      colour=discord.Colour.red())
    e.set_footer(text=foot)
    try:
      await destination.send(embed=e)
    except discord.HTTPException:
      await ctx.send(f"Sorry, I couldn't send a card to **{user.name}.**")
    else:
      await ctx.send(f"Christmas card delivered to **{user.name}!** :gift:")
