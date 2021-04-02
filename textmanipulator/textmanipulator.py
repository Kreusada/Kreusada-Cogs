import discord
from redbot.core import commands

# TODO: Rewrite


class TextManipulator(commands.Cog):
    """
    Manipulate characters and text.
    """

    __author__ = ["Kreusada", ]
    __version__ = "1.5.0"

    def __init__(self, bot):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad."""
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """
        Nothing to delete
        """
        return

    @commands.group()
    async def convert(self, ctx: commands.Context):
        """Convert text into different types."""

    @commands.group()
    async def count(self, ctx: commands.Context):
        """Count the number of characters and words."""

    @count.command(aliases=["char"])
    async def characters(self, ctx: commands.Context, *, characters: str):
        """Count how many characters are in a specified text."""
        await ctx.send(
            f"**Including spaces:** {str(len(characters))}\n"
            f"**Excluding spaces:** {str(len(characters) - characters.count(' '))}`"
        )

    @count.command()
    async def words(self, ctx: commands.Context, *, words: str):
        """Count how many words are in a specified text."""
        await ctx.send(f"**Total words:** {str(len(words.split()))}")

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
        await ctx.send(characters.replace(" ", "_"))

    @convert.command()
    async def alt(self, ctx: commands.Context, *, characters: str):
        """Convert all characters to alternating case."""
        characters = list(characters)
        characters[0::2] = map(str.upper, characters[0::2])
        characters[1::2] = map(str.lower, characters[1::2])
        await ctx.send("".join(characters))