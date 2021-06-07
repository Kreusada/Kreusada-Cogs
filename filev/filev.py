import asyncio
import contextlib
import discord
import json
import pathlib
import yaml

from redbot.core import commands
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.chat_formatting import pagify, box, humanize_list
from redbot.core.utils.predicates import ReactionPredicate, MessagePredicate


with open(pathlib.Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


class Filev(commands.Cog):
    """Easy and quick tools to validate various file syntax."""

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
            self.bot.remove_dev_env_value("filev")


    async def initialize(self) -> None:
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("filev", lambda x: self)

    @staticmethod
    def cleanup_code(content) -> str:
        # From redbot.core.dev_commands, thanks will :P
        if content.startswith("```") and content.endswith("```"):
            return "\n".join(content.split("\n")[1:-1])
        return content.strip("` \n")

    @staticmethod
    def tick(text) -> str:
        return "{} {}".format("\N{BALLOT BOX WITH CHECK}\N{VARIATION SELECTOR-16}", text)
    
    @staticmethod
    def cross(text) -> str:
        return "{} {}".format("\N{CROSS MARK}", text)


    @commands.command(usage="[file]")
    async def jsonscan(self, ctx: commands.Context):
        """Scan json to see if its correct.

        Your next message will be used to as the json to scan.
        You can also upload a JSON file.
        """

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
            json.loads(self.cleanup_code(content))
        except json.JSONDecodeError as e:
            message = self.cross("This was **not** valid JSON. Would you like to see the exception details?")
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
                    await message.edit(content=self.cross("This was **not** valid JSON."))

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
                    await message.edit(content=self.cross("This was **not** valid JSON."))
            return

        await ctx.send(self.tick("This JSON looks good!"))


    @commands.command(usage="[file]")
    async def yamlscan(self, ctx: commands.Context):
        """Scan yaml to see if its correct.

        Your next message will be used to as the yaml to scan.
        You can also upload a YAML file.
        """

        if ctx.message.attachments[0]:
            # attachments will take priority
            file = ctx.message.attachments[0]
            if not file.filename.split('.')[-1] in ("yaml", "yml", "mir"):
                return await ctx.send("Please upload a valid YAML file.")
            try:
                file = await file.read()
                print(file.decode(encoding="utf-8"))
                content = file.decode(encoding="utf-8")
            except UnicodeDecodeError:
                return await ctx.send("Something went wrong whilst trying to decode the provided file.")
        
        else:

            message = await ctx.send(
                "Your next message will be your YAML content:"
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
            yaml.full_load(self.cleanup_code(content))
        except yaml.parser.MarkedYAMLError as e:
            message = self.cross("This was **not** valid YAML. Would you like to see the exception details?")
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
                    await message.edit(content=self.cross("This was **not** valid YAML."))

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
                    await message.edit(content=self.cross("This was **not** valid YAML."))
            return

        await ctx.send(self.tick("This YAML looks good!"))