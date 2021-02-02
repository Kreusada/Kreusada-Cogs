import discord
from redbot.core import commands
from redbot.core.i18n import Translator, cog_i18n

_ = Translator("TextManipulator", __file__)

@cog_i18n(_)
class TextManipulator(commands.Cog):
    """
    Manipulate characters and text.
    """

    __author__ = "Kreusada"
    __version__ = "1.5.0"
  
    def __init__(self, bot):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad."""
        return f"{super().format_help_for_context(ctx)}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """
        Nothing to delete
        """
        return
      
    @commands.group()
    async def convert(self, ctx: commands.Context):
        """Convert text into different types."""
      
    @convert.command()
    async def upper(self, ctx: commands.Context, *, characters: str):
        """Convert all characters to uppercase."""
        await ctx.send(characters.upper())

    @convert.command()
    async def lower(self, ctx: commands.Context, *, characters: str):
        """Convert all characters to lowercase."""
        await ctx.send(characters.lower())

    @convert.command()
    async def title(self, ctx: commands.Context, *, characters: str):
        """Convert all characters to titlecase."""
        await ctx.send(characters.title())

    @convert.command()
    async def snake(self, ctx: commands.Context, *, characters: str):
        """Convert all spaces to underscores."""
        await ctx.send(characters.replace(' ', '_'))

    @convert.command()
    async def alt(self, ctx: commands.Context, *, characters: str):
        """Convert all characters to alternating case."""
        characters = list(characters)
        characters[0::2] = map(str.upper, characters[0::2])
        characters[1::2] = map(str.lower, characters[1::2])
        inputer = ''
        await ctx.send(f"{inputer.join(characters)}")
      
    @commands.command()
    async def charcount(self, ctx: commands.Context, *, characters: str):
        """Count how many characters are in a specified text."""
        space = ' '
        await ctx.send(
            f"**Including spaces:** {str(len(characters))}\n"
            f"**Excluding spaces:** {str(len(characters) - characters.count(space))}`"
        )
    
    @commands.command()
    async def wordcount(self, ctx: commands.Context, *, words: str):
        """Count how many words are in a specified text."""
        await ctx.send(**Total words:** str(len(words.split())))
    
    @commands.command()
    async def removecommas(self, ctx: commands.Context, *, list: str):
        """Remove commas from text."""
        await ctx.send(list.replace(',', ''))

    @commands.command()
    async def escapemarkdown(self, ctx: commands.Context, *, words: str):
        """Escape markdown."""
        makeraw = discord.utils.escape_markdown(words)
        await ctx.send(makeraw)
      
    @commands.command()
    async def replace(self, ctx: commands.Context, to_replace: str, to_replace_with: str, *, message: str):
        """
        Replace any given character in a message.
        
        `characters` The characters you want to replace.
        
        `replacers` The characters which replace your characters (above).
        
        `message` The message where the above takes place.
        """
        await ctx.send(message.replace(to_replace, to_replace_with))
