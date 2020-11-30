import discord
from redbot.core import commands, checks
from redbot.cogs.downloader.converters import InstalledCog

class l(commands.Cog):
  """private learning"""
  
  def __init__(self, bot):
    self.bot = bot
  
    @bot.event
    async def on_message(message):
      if message.author == bot.user:
        return
      
      if message.content.startswith("Demaratus"):
        await message.channel.send("Hi")
