import asyncio
import contextlib
import discord
import json

from redbot.core import commands
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.chat_formatting import pagify, box, humanize_list
from redbot.core.utils.predicates import ReactionPredicate, MessagePredicate


class JsonScanner(commands.Cog):
    """An easy and quick tool to validate json."""

    __author__ = ["Kreusada"]
    __version__ = "1.0.0"


    def __init__(self, bot):
        self.bot = bot


    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = humanize_list(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"


    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return


    def cog_unload(self):
        with contextlib.suppress(Exception):
            self.bot.remove_dev_env_value("jsonscanner")


    async def initialize(self) -> None:
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("jsonscanner", lambda x: self)


    @commands.command(usage="[file]")
    async def jsonscan(self, ctx: commands.Context):
        """Scan json to see if its correct.

        Your next message will be used to as the json to scan.
        You can also upload a JSON file.
        """

        def cleanup_code(content) -> str:
            # From redbot.core.dev_commands, thanks will :P
            if content.startswith("```") and content.endswith("```"):
                return "\n".join(content.split("\n")[1:-1])
            return content.strip("` \n")

        def tick(text) -> str:
            return "{} {}".format("\N{BALLOT BOX WITH CHECK}\N{VARIATION SELECTOR-16}", text)
        
        def cross(text) -> str:
            return "{} {}".format("\N{CROSS MARK}", text)

        if ctx.message.attachments:
            # attachments will take priority
            file = ctx.message.attachments[0]
            if not file.filename.split('.')[-1] == "json":
                return await ctx.send("Please upload a valid JSON file.")
            try:
                file = await file.read()
                content = file.decode(encoding="utf-8")
            except UnicodeDecodeError:
                return await ctx.send("Something went wrong whilst trying to decode the provided file.")
        
        else:

            message = await ctx.send(
                "Your next message will be your JSON content:"
            )

            check = lambda x: x.channel == ctx.channel and x.author == ctx.author


            try:
                content = await self.bot.wait_for("message", check=check, timeout=100)
                content = content.content
            except asyncio.TimeoutError:
                with contextlib.suppress(discord.NotFound):
                    await message.edit("You took too long to respond.")
                    return
                await ctx.send("You took too long to respond.")
                return


        try:
            json.loads(cleanup_code(content))
        except json.JSONDecodeError as e:
            message = cross("This was **not** valid JSON. Would you like to see the exception details?")
            can_react = ctx.channel.permissions_for(ctx.me).add_reactions

            if not can_react:
                message += " (yes/no)"

            message = await ctx.send(message)

            if can_react:
                start_adding_reactions(message, ReactionPredicate.YES_OR_NO_EMOJIS)
                predicate = ReactionPredicate.yes_or_no(message, ctx.author)
                event_type = "reaction_add"

            else:
                predicate = MessagePredicate.yes_or_no(ctx)
                event_type = "message"

            try:
                await self.bot.wait_for(event_type, check=predicate, timeout=30)
            except asyncio.TimeoutError:
                with contextlib.suppress(discord.NotFound):
                    await message.edit(content=cross("This was **not** valid JSON."))

            if predicate.result:
                description = box(str(e), lang="py")
                await message.clear_reactions()
                if await ctx.embed_requested():
                    embed = discord.Embed(
                        title="Exception details",
                        description=description,
                        color=0xff7575
                    )
                    await message.edit(embed=embed, content=None)
                else:
                    await message.edit(content=description)
            else:
                with contextlib.suppress(discord.NotFound):
                    await message.edit(content=cross("This was **not** valid JSON."))
            return

        await ctx.send(tick("This JSON looks good!"))