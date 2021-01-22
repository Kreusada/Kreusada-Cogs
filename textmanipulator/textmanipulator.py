import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import box

from redbot.core import commands
from redbot.core.i18n import Translator, cog_i18n

_ = Translator("TextManipulator", __file__)

@cog_i18n(_)
class TextManipulator(commands.Cog):
  """Manipulate characters and text."""
  
  def __init__(self, bot):
    self.bot = bot

  async def red_delete_data_for_user(self, **kwargs):
      """
      Nothing to delete
      """
      return
    
  @commands.group()
  async def convert(self, ctx):
    """Convert text into different types."""
    
  @convert.command()
  async def upper(self, ctx, *, characters: str):
    """Convert all characters to uppercase."""
    await ctx.send(characters.upper())

  @convert.command()
  async def lower(self, ctx, *, characters: str):
    """Convert all characters to lowercase."""
    await ctx.send(characters.lower())

  @convert.command()
  async def title(self, ctx, *, characters: str):
    """Convert all characters to titlecase."""
    await ctx.send(characters.title())

  @convert.command()
  async def snake(self, ctx, *, characters: str):
    """Convert all spaces to underscores."""
    await ctx.send(characters.replace(' ', '_'))

  @convert.command()
  async def alt(self, ctx, *, characters: str):
    """Convert all characters to alternating case."""
    characters = list(characters)
    characters[0::2] = map(str.upper, characters[0::2])
    characters[1::2] = map(str.lower, characters[1::2])
    inputer = ''
    await ctx.send(f"{inputer.join(characters)}")
    
  @commands.command()
  async def charcount(self, ctx, *, characters: str):
    """Count how many characters are in a specified text."""
    spaces = "**Including spaces:** "
    nspaces = "**Excluding spaces:** "
    scount = ' '
    await ctx.send(f"{spaces}{str(len(characters))}\n{nspaces}{str(len(characters) - characters.count(scount))}`")
  
  @commands.command()
  async def wordcount(self, ctx, *, words: str):
    """Count how many words are in a specified text."""
    w = "**Total words:** "
    await ctx.send(w+str(len(words.split())))
    return
  
  @commands.command()
  async def removecommas(self, ctx, *, list: str):
    """Remove commas from text."""
    await ctx.send(list.replace(',', ''))

  @commands.command()
  async def escapemarkdown(self, ctx, *, words: str):
    """Escape markdown."""
    makeraw = discord.utils.escape_markdown(words)
    await ctx.send(makeraw)
    
  @commands.command()
  async def replace(self, ctx, to_replace: str, to_replace_with: str, *, message: str):
    """
    Replace any given character in a message.
    
    `characters` The characters you want to replace.
    
    `replacers` The characters which replace your characters (above).
    
    `message` The message where the above takes place.
    """
    await ctx.send(message.replace(to_replace, to_replace_with))
