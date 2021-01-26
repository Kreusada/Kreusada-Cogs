import discord
import asyncio
from redbot.core import commands
from redbot.core.i18n import Translator, cog_i18n

_ = Translator("SendCards", __file__)

@cog_i18n(_)
class SendCards(commands.Cog):
  """Send someone a card!"""
  
  def __init__(self, bot):
    self.bot = bot

  async def red_delete_data_for_user(self, **kwargs):
      """
      Nothing to delete
      """
      return

  @commands.group()
  async def card(self, ctx):
    """General settings for cards."""
      
  @card.group()
  async def send(self, ctx):
    """Send a card to someone!"""
    
# This cog was made a while back, when I just started learning to code.
# The original concept of getting a users DMs was taken from 
    
  @send.command()
  async def christmas(self, ctx: commands.Context, user_id: int, *, message: str):
    """Send a christmas card to someone!"""
    destination = self.bot.get_user(user_id)
    author = ctx.author.name
    user = destination
    if destination is None or destination.bot:
        await ctx.send("Invalid ID, user not found, or user is a bot.")
    else:
      foot = (f"Send christmas cards using: {ctx.clean_prefix}card send christmas!")
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

  @send.command()
  async def birthday(self, ctx: commands.Context, user_id: int, *, message: str):
    """Send a birthday card to someone!"""
    destination = self.bot.get_user(user_id)
    author = ctx.author.name
    user = destination
    if destination is None or destination.bot:
        await ctx.send("Invalid ID, user not found, or user is a bot.")
    else:
      foot = (f"Send birthday cards using: {ctx.clean_prefix}card send birthday!")
      e = discord.Embed(title=f":tada: Birthday Card from {ctx.author} :tada:", 
                       description= "Dear {},\n\n{}\n\nFrom {} :balloon:".format(user.name, message, author), 
                       colour=discord.Colour.red())
      e.set_footer(text=foot)
    try:
      await destination.send(embed=e)
    except discord.HTTPException:
      await ctx.send(f"Sorry, I couldn't send a card to **{user.name}.**")
    else:
      await ctx.send(f"Birthday card delivered to **{user.name}!** :tada:")

  @send.command(aliases=["gws"])
  async def getwellsoon(self, ctx: commands.Context, user_id: int, *, message: str):
    """Send a get well soon card to someone!"""
    destination = self.bot.get_user(user_id)
    author = ctx.author.name
    user = destination
    if destination is None or destination.bot:
        await ctx.send("Invalid ID, user not found, or user is a bot.")
    else:
      foot = (f"Send get well soon cards using: {ctx.clean_prefix}card send getwellsoon!")
      e = discord.Embed(title=f":thermometer_face: Get Well Soon Card from {ctx.author} :thermometer_face:", 
                       description= "Dear {},\n\n{}\n\nFrom {} :pray:".format(user.name, message, author), 
                        colour=discord.Colour.red())
      e.set_footer(text=foot)
    try:
      await destination.send(embed=e)
    except discord.HTTPException:
      await ctx.send(f"Sorry, I couldn't send a card to **{user.name}.**")
    else:
      await ctx.send(f"Get well soon card delivered to **{user.name}!** I hope they're okay too! :pray:")

  @send.command()
  async def valentine(self, ctx: commands.Context, user_id: int, *, message: str):
    """Send a valentines card to someone!"""
    destination = self.bot.get_user(user_id)
    author = ctx.author.name
    user = destination
    if destination is None or destination.bot:
        await ctx.send("Invalid ID, user not found, or user is a bot.")
    else:
      foot = (f"Send valentine cards using: {ctx.clean_prefix}card send valentine!")
      romance = ":smiling_face_with_3_hearts:"
      e = discord.Embed(title=f"{romance} Valentines Card from {ctx.author} {romance}", 
                       description= "Dear {},\n\n{}\n\nWith love from {} {}".format(user.name, message, author, romance), 
                        colour=discord.Colour.red())
      e.set_footer(text=foot)
    try:
      await destination.send(embed=e)
    except discord.HTTPException:
      await ctx.send(f"Sorry, I couldn't send a card to **{user.name}.**")
    else:
      await ctx.send(f"Valentines card delivered to **{user.name}!** Hey {author}, stop blushing. :wink:")
