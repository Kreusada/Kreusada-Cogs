import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import box

class Codify(commands.Cog):
    """Get a message and wrap it in a codeblock."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def codify(self, ctx, message_id: int, language: str = "python"): 
        """Get a message and wrap it in a codeblock."""
        try:
            message = await ctx.fetch_message(message_id)
            await ctx.send(box(message.content, lang=language))
        except discord.NotFound:
            await ctx.send(f"Could not find a message with the ID: `{message_id}`.")