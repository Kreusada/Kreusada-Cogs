import asyncio
import datetime
import pathlib
import sys
from typing import Literal

import discord
import yaml
from redbot.core import commands, Config
from redbot.core.utils.chat_formatting import italics, humanize_list, inline, box
from yaml.parser import (
    MarkedYAMLError, ParserError, ScannerError
)

with open(pathlib.Path(__file__).parent / "cog_creation.yaml") as f:
    example_cog_creation_yaml = f.readlines()


class ParserInvalidStackError(Exception):
    """
    Raised when an unsupported type is present in a dict key.
    This exception is incomprehensible.

    Attributes:
        key: str
            The name of the key which is an invalid type.
        data: dict
            The data from which the key has been raised from.
    """

    def __init__(self, key: str, data: dict):
        self.key = key 
        self.data = data

    def __str__(self):
        key = self.key
        key_type = type(self.data.get(self.key)).__name__
        if key in ("name", "description", "end_user_data_statement", "github_url"):
            supported_type = str
        elif key in ("author", "requirements", "tags"):
            supported_type = list
        elif key in ("smart_link_title", "installation_guide"):
            supported_type = bool
        else:
            return "Something went wrong whilst reading your data."
        accept_nonetype = ""
        if not key in ("name", "end_user_data_statement", "github_url"):
            accept_nonetype += " or null"
        return (
            f"The {self.key} key type must be a {supported_type.__name__}{accept_nonetype}, not {key_type}"
        )

class ParserInvalidTypeError(Exception):
    """
    Raised when an unsupported type is provided to the parser.

    Attributes:
        field: str
            The yaml dict field where the exception has been raised.
        invalid_type: type
            The invalid passed type.
        supported_types: tuple
            The supported types for the field.
    """
    
    def __init__(self, field: str, invalid_type: type, supported_types: tuple):
        self.field_name = field
        self.invalid_type = invalid_type
        self.supported_types = supported_types

    def __str__(self):
        humanized = humanize_list(items=[x.__name__ for x in self.supported_types], style='or')
        return (
            f"The '{self.field_name}' field's type must be "
            f"{humanized}, not {self.invalid_type.__name__}"
        )

class ParserRequiredKeyError(Exception):
    """
    Raised when a required key does not exist in the data.

    Attributes:
        key: str
            The name of the required key that is missing.
    """

    def __init__(self, key):
        self.key = key

    def __str__(self):
        return f"The \"{self.key}\" key is required"

class ParserGhostURLError(Exception):
    """
    Raised when installation guide has been opted into without
    a github_url key.
    """
    pass


PublishType = Literal["creation", "removal"]


class EmbedBuilder(object):
    """
    Builds the embed image for the provided and relevant data.
    The YAML will have been validated before it reaches this point.
    Irrelvant keys are ignored as we are only getting the keys we need
    through dict.get()

    Attributes:
    data: dict
        The extracted data from the yaml conversion
    publish_type: str
        Must be one of PublishTypes
    """

    def __init__(self, data: dict, publish_type: PublishType,):
        super().__init__()
        self.data = data
        self.name = data.get("name")
        self.author = data.get("author")
        self.description = data.get("description")
        self.requirements = data.get("requirements")
        self.tags = data.get("tags")
        self.end_user_data_statement = data.get("end_user_data_statement")
        self.show_installation_guide = data.get("installation_guide", False)
        self.github_url = data.get("github_url")
        self.smart_link_title = data.get("smart_link_title")
        # removal publishtype
        self.reason = data.get("reason", None)
        # list of all viable keys
        self.key_list = [
            "name", 
            "author",
            "description",
            "requirements",
            "tags",
            "end_user_data_statement",
            "installation_guide",
            "github_url",
            "smart_link_title",
            "reason",
        ]
        # misc
        self.publish_type = publish_type

    def __repr__(self) -> str:
        return f"<class {self.__class__.__name__}(data={self.data})>"

    @property
    def __str__(self):
        return self.__repr__

    def __len__(self) -> int:
        return len(self.data.keys())

    def format_build(self, ctx):
        # This will elimate any other types from the parser
        for key in self.data.keys():
            value = self.data.get(key)
            if not isinstance(value, (str, list, bool)) or value is not None and value in self.key_list:
                raise ParserInvalidStackError(key=key, data=self.data)

        plural_author = "Author"
        if self.author:
            if not isinstance(self.author, (list, str)):
                raise ParserInvalidTypeError(
                    field="author",
                    invalid_type=type(self.author),
                    supported_types=(list, str),
                )
            if isinstance(self.author, list):
                if not len(self.author) == 1:
                    plural_author += "s"
        else:
            self.author = ctx.author.name

        if not self.name:
            raise ParserRequiredKeyError("name")

        if self.publish_type == "creation":
            # All the error handling will be done under this statement
            if not self.name:
                raise ParserRequiredKeyError("name")
            if not self.end_user_data_statement:
                raise ParserRequiredKeyError("end_user_data_statement")

            if self.description:
                if not isinstance(self.description, str):
                    raise ParserInvalidTypeError(
                        field="description",
                        invalid_type=type(self.description),
                        supported_types=(str),
                    )
            else:
                self.description = italics("No description was provided.")
            if not isinstance(self.name, str):
                raise ParserInvalidTypeError(
                    field="name",
                    invalid_type=type(self.name),
                    supported_types=(str),
                )
            if self.github_url:
                if not isinstance(self.github_url, str):
                    raise ParserInvalidTypeError(
                        field="github_url",
                        invalid_type=type(self.github_url),
                        supported_types=(str),
                    )
            else:
                if self.show_installation_guide:
                    raise ParserGhostURLError(
                        "You must provide a `github_url` key if you wish to opt into "
                        "adding an installation guide."
                    )
            if self.requirements:
                if not isinstance(self.requirements, list):
                    raise ParserInvalidTypeError(
                        field="requirements",
                        invalid_type=type(self.requirements),
                        supported_types=(list),
                    )
            if self.tags:
                if not isinstance(self.tags, list):
                    raise ParserInvalidTypeError(
                        field="tags",
                        invalid_type=type(self.tags),
                        supported_types=(list),
                    )
            if self.end_user_data_statement:
                if not isinstance(self.end_user_data_statement, str):
                    raise ParserInvalidTypeError(
                        field="end_user_data_statement",
                        invalid_type=type(self.end_user_data_statement),
                        supported_types=(str),
                    )
            else:
                raise ParserRequiredKeyError("end_user_data_statement")
            if self.show_installation_guide:
                if not isinstance(self.show_installation_guide, bool):
                    raise ParserInvalidTypeError(
                        field="show_installation_guide",
                        invalid_type=type(self.show_installation_guide),
                        supported_types=(bool),
                    )

            if isinstance(self.author, list):
                a = self.author[0]
            else:
                a = self.author
            install_description = (
                f"[p]repo add {a} {self.github_url}\n"
                f"[p]cog install {a} {self.name}\n\n"
                "Replace [p] with your prefix."
            )

            kwargs = {
                "title": self.name,
                "description": self.description,
                "timestamp": datetime.datetime.now(),
                "color": 0x6ac6af
            }
            if self.smart_link_title and self.github_url:
                kwargs["url"] = f"{self.github_url}/{self.name.lower()}"
                
            embed = discord.Embed(**kwargs)

            if isinstance(self.author, list):
                self.author = ", ".join(self.author)

            embed.add_field(name=plural_author, value=self.author, inline=True)
            if self.requirements:
                embed.add_field(name="Requirements", value=", ".join(self.requirements), inline=True)
            if self.end_user_data_statement:
                embed.add_field(name="End User Data Statement", value=self.end_user_data_statement, inline=False)
            if self.show_installation_guide:
                embed.add_field(name="Installation Instructions", value=install_description, inline=False)
            if self.tags:
                embed.set_footer(text="Tags: " + ", ".join(self.tags[:7]))

            embed.set_author(name="Added cog", icon_url=ctx.author.avatar_url)

        else:
            if not self.removal:
                raise ParserRequiredKeyError("removal")
            if not self.name:
                raise ParserRequiredKeyError("name")
            if not self.reason:
                raise ParserRequiredKeyError("reason")

            embed = discord.Embed(
                title=f"Removed Cog",
                timestamp=datetime.datetime.now(),
                color=0xe84e4e
            )

            embed.add_field(name="Name", value=self.name, inline=True)
            embed.add_field(name=plural_author, value=self.author, inline=True)
            embed.add_field(name="Reason", value=self.reason, inline=False)
        
        return embed


    def __eq__(self, o) -> bool:
        return isinstance(o, self.__class__) and o.id == self.id

    def __ne__(self, o) -> bool:
        return not self.__eq__(o)
            

class PublishCogs(commands.Cog):
    """Publish your cogs to a new channel."""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 953478905834590284, force_registration=True)
        self.config.register_guild(
            channel=None,
        )

    @staticmethod
    def has_cli_flag(flag):
        return f"--{flag}" in sys.argv

    @staticmethod
    def cleanup_code(content):
        # From redbot.core.dev_commands, thanks will :P
        if content.startswith("```") and content.endswith("```"):
            return "\n".join(content.split("\n")[1:-1])
        return content.strip("` \n")

    @staticmethod
    def format_traceback(exc):
        boxit = lambda x, y: box(f"{x}: {y}", lang="yaml")
        return boxit(exc.__class__.__name__, exc)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        _channel = await self.config.guild(channel.guild).channel()
        if channel.id == _channel:
            await self.config.guild(channel.guild).channel.clear()

    async def yaml_parser(self, ctx, content, publish_type: PublishType):
        # Passing ctx for self.prepare_builder
        content = self.cleanup_code(content)
        try:
            loader = yaml.full_load(content)
        except (ParserError, MarkedYAMLError, ScannerError):
            return await ctx.send("Please provide valid YAML.")
        await self.prepare_builder(ctx, loader, publish_type)

    async def prepare_builder(self, ctx, content, publish_type: PublishType):
        approved_cog_creators = await self.config.guild(ctx.guild).approved_cog_creators()
        try:
            builder = EmbedBuilder(
                data=content, 
                publish_type=publish_type,
            )
            builder = builder.format_build(ctx)
        except Exception as e:
            return await ctx.send(self.format_traceback(e))
        channel = await self.config.guild(ctx.guild).channel()
        channel = self.bot.get_channel(channel)
        if not channel:
            await ctx.send("Looks like the publishcogs channel doesn't exist anymore.")
            await self.config.guild(ctx.guild).channel.clear()
            return
        if not channel.permissions_for(ctx.me).send_messages:
            await ctx.send("I don't have permissions to send messages to the publishcogs channel.")
            return
        if not channel.permissions_for(ctx.me).embed_links or not await ctx.embed_requested():
            await ctx.send("I don't have permissions to send embeds to the publishcogs channel.")
            return
        await channel.send(embed=builder)
        await ctx.send("Publish cog successful!")

    @commands.command()
    async def publishcog(self, ctx):
        """Publish your new cog to a new channel."""
        def check(x):
            return x.author == ctx.author and x.channel == ctx.channel
        await ctx.send(
            "Now you need to compose your YAML. For reference, see below: "
            + box("".join(example_cog_creation_yaml), lang="yaml")
        )
        try:
            content = await self.bot.wait_for("message", timeout=250, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("You took too long to respond.")
        content = content.content
        publish_type = "creation"
        async with ctx.typing():
            await self.yaml_parser(ctx, content, publish_type)

    @commands.group()
    async def publishcogset(self, ctx):
        """Settings with PublishCogs."""

    @publishcogset.command(name="channel")
    async def publishcogset_channel(self, ctx, channel: discord.TextChannel):
        """Set the publishcogs feed channel."""
        await self.config.guild(ctx.guild).channel.set(channel.id)
        await ctx.tick()