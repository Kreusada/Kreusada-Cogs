import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import box

class TextManipulator(commands.Cog):
  """Manipulate characters and text."""
  
  def __init__(self, bot):
    self.bot = bot
    
  @commands.group()
  async def convert(self, ctx):
    """Convert text into different types."""
    
  @convert.command()
  async def upper(self, ctx, *, characters: str):
    """Convert all characters to uppercase."""
    await ctx.send(f"`{characters.upper()}`")

  @convert.command()
  async def lower(self, ctx, *, characters: str):
    """Convert all characters to lowercase."""
    await ctx.send(f"`{characters.lower()}`")

  @convert.command()
  async def title(self, ctx, *, characters: str):
    """Convert all characters to titlecase."""
    await ctx.send(f"`{characters.title()}`")

  @convert.command()
  async def snake(self, ctx, *, characters: str):
    """Convert all spaces to underscores."""
    replace = characters.replace(' ', '_')
    await ctx.send(f"`{replace}`")

  @convert.command()
  async def alt(self, ctx, *, characters: str):
    """Convert all characters to alternating case."""
    characters = list(characters)
    characters[0::2] = map(str.upper, characters[0::2])
    characters[1::2] = map(str.lower, characters[1::2])
    inputer = ''
    await ctx.send(f"`{inputer.join(characters)}`")
    
  @commands.command()
  async def charcount(self, ctx, *, characters: str):
    """Count how many characters are in a specified text."""
    spaces = "**Including spaces:** "
    nspaces = "**Excluding spaces:** "
    scount = ' '
    await ctx.send(f"{spaces}`{str(len(characters))}`\n{nspaces}`{str(len(characters) - characters.count(scount))}`")
  
  @commands.command()
  async def wordcount(self, ctx, *, words: str):
    """Count how many words are in a specified text."""
    w = "**Total words:** "
    await ctx.send(f"{w}`{str(len(words.split()))}`")
    return
  
  @commands.command()
  async def removecommas(self, ctx, *, list: str):
    """Remove commas from text."""
    await ctx.send(f"`{list.replace(',', '')}`")

  @commands.command()
  async def codepython(self, ctx, *, words: str):
    """Convert usual text into python codeblock escaping markdown."""
    msg = f"{box(words, lang='python')}"
    makeraw = discord.utils.escape_markdown(msg)
    await ctx.send(makeraw)

  @commands.command()
  async def escapemarkdown(self, ctx, *, words: str):
    """Escape markdown."""
    makeraw = discord.utils.escape_markdown(words)
    await ctx.send(makeraw))
    
  @commands.command()
  async def replace(self, ctx, characters: str, replacers: str, *, message: str):
    """
    Replace any given character in a message.
    **characters** The characters you want to replace.
    **replacers** The characters which replace yor characters (above).
    **message** The message where the above takes place.
    """
    await ctx.send(f"`{message.replace(characters, replacers)}`")
