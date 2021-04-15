import asyncio
import json
import logging
import sys
import types
from distutils import sysconfig
from importlib import machinery
from pathlib import Path

import discord
import lavalink
import pip
import redbot
from redbot.core import commands
from redbot.core.utils.chat_formatting import bold, box
from redbot.core.utils.predicates import MessagePredicate
from stdlib_list import stdlib_list

log = logging.getLogger("red.kreusada.vinfo")

base = "{}: {}\n{}: {}.{}.{}\n{}: {}\n\n{}: {}\n{}: {}"


REDBOT_CORE_COGS = [
    "Admin",
    "Alias",
    "Audio",
    "Bank",
    "Cleanup",
    "CustomCom",
    "Downloader",
    "Economy",
    "Filter",
    "General",
    "Image",
    "Mod",
    "ModLog",
    "Mutes",
    "Permissions",
    "Reports",
    "Streams",
    "Trivia",
    "Warnings",
]

check_isinstance = lambda x, y: isinstance(getattr(x, y), (str, int, list, tuple))

class Vinfo(commands.Cog):
    """
    Get versions of 3rd party cogs, and modules.
    """

    __author__ = [
        "Kreusada",
    ]
    __version__ = "1.3.0"

    def __init__(self, bot):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    def check_attrs(self, module: types.ModuleType):
        # pypath = str(sysconfig.get_python_lib(standard_lib=True))
        builtin = [sys.version_info[:3], "(Core/Builtin Python)"]
        with open(Path(__file__).parent / "attrs.json") as fp:
            attrs_to_check = json.load(fp)["attrs"]
        for attr in attrs_to_check:
            if hasattr(module, attr) and check_isinstance(module, attr):
                return [getattr(module, attr), "." + attr]
        if module.__name__ in stdlib_list(".".join(sys.version_info[:2])):
            # Will bump on Red python bump, eventually
            return builtin
        # if hasattr(module, '__file__'):
        #     file = module.__file__.lower()
        #     if file.startswith(pypath.lower()):
        #         return builtin
        # if hasattr(module, '__spec__'):
        #     if isinstance(module.__spec__, machinery.ModuleSpec):
        #         if hasattr(module.__spec__, 'origin') and module.__spec__.origin:
        #             spec = module.__spec__.origin
        #             if spec.lower().startswith(pypath.lower()):
        #                 return builtin
        #             if spec.lower() == "built-in":
        #                 return builtin
        # if hasattr(module, '__path__'):
        #     path = module.__path__[0].lower()
        #     if path.startswith(pypath.lower()):
        #         return builtin
        # return None

    @staticmethod
    def modvinfo_format(mods):
        formatter = (
            bold("Red"),
            redbot.version_info,
            bold("Python (sys)"),
            *sys.version_info[:3],
            bold("discord.py"),
            discord.__version__,
            bold("PIP"),
            pip.__version__,
            bold("Lavalink"),
            lavalink.__version__,
        )
        description = mods.format(*formatter)
        return discord.Embed(
            title="Common Modules",
            description=description,
        )

    # Commands

    @commands.is_owner()
    @commands.group(aliases=["versioninfo"])
    async def vinfo(self, ctx):
        """Get versions of 3rd party cogs, and modules."""

    @vinfo.command()
    async def cog(self, ctx, cog: str):
        """
        Get the version information for a Red cog.

        The cog must be loaded, and provided in the correct casing.
        """
        await ctx.trigger_typing()
        
        if cog not in self.bot.cogs:
            return await ctx.send(box(f"- Could not find a cog matching `{cog}`.", lang='diff'))

        Cog = self.bot.get_cog(cog)

        # Note that cogs won't have a `version_info` attr unlike some modules, so
        # we'll skip finding that attr because it will return False 99% of the time.

        if hasattr(Cog, "__version__"):
            return await ctx.send(box(f"{cog} version: {getattr(Cog, '__version__')}", lang='yaml'))
        elif cog in REDBOT_CORE_COGS:
            return await ctx.send(
                box(
                    "Builtin Red cogs do not have version attributes by default.\n"
                    "Perhaps you're looking for your Red version, which would be {}.".format(redbot.version_info), 
                    lang="yaml"
                )
            )
        else:
            await ctx.send(box(f"- Could not find a version for {cog}.", lang='diff'))

    @vinfo.command(aliases=["module", "dep", "dependency"], usage="<module or dependency>")
    @commands.bot_has_permissions(embed_links=True)
    async def mod(self, ctx, module: str = None):
        """Get module versions."""
        
        if not module:
            embed = self.modvinfo_format(base)
            embed.color = await ctx.embed_colour()
            embed.set_footer(
                text="Find a specific module version by adding the module argument."
            )
            await ctx.send(embed=embed)
            return await ctx.send_help()

        await ctx.trigger_typing()

        try:
            MOD = __import__(module)
        except ModuleNotFoundError:
            none_found = "- You do not have an installed module named `{}`.".format(module)
            pipinstall = await ctx.send(box(none_found + "\n--- Would you like to pip install it? (yes/no)", lang="diff"))
            try:
                pred = MessagePredicate.yes_or_no(ctx, user=ctx.author)
                msg = await ctx.bot.wait_for("message", check=pred, timeout=20)
            except asyncio.TimeoutError:
                return await pipinstall.edit(content=box(none_found, lang="diff"))
            if pred.result:
                return await ctx.invoke(self.bot.get_command("pipinstall"), module)
            else:
                return await pipinstall.edit(content=box(none_found, lang="diff"))

        check_attrs = self.check_attrs(MOD)

        if not check_attrs:
            return await ctx.send(
                box("# Could not find a version for `{}`.", lang="cs").format(MOD.__name__)
            )

        vinfo = check_attrs

        if isinstance(vinfo[0], tuple) and vinfo[1] == "(Core/Builtin Python)":
            value = ("{}." * len(vinfo[0])).strip('.').format(*vinfo[0])
            attr = f"None {vinfo[1]}"
        
        elif isinstance(vinfo[0], (list, tuple)):
            value = ("{}." * len(vinfo[0])).strip('.').format(*vinfo[0])
            attr = f"`{MOD.__name__}{vinfo[1]}`"

        else:
            value = vinfo[0]
            attr = f"`{MOD.__name__}{vinfo[1]}`"


        await ctx.send(
            box(
                f"Attribute: {attr}\nFound version info for [{module}]: {value}",
                lang="yaml",
            )
        )
