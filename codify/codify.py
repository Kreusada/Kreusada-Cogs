import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import box

class Codify(commands.Cog):
    """
    Get a message and wrap it in a codeblock.
    """

    __author__ = ["Kreusada"]
    __version__ = "1.3.0"

    def __init__(self, bot):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        return f"{super().format_help_for_context(ctx)}\n\nCog Version: {self.__version__}"
        # Thanks Sinbad.

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    @commands.command()
    async def codify(self, ctx: commands.Context, message_id: int, language: str = "python"): 
        """
        Get a message and wrap it in a codeblock.
        
        Arguments:
        `language`: The language to transform the message content to.
        Defaults to python.
        """
        try:
            message = await ctx.fetch_message(message_id)
            await ctx.send(box(message.content, lang=language))
        except discord.NotFound:
            await ctx.send(f"Could not find a message with the ID: `{message_id}`.")
