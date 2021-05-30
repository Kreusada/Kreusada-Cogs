import asyncio
import contextlib
import datetime
import json
import logging
from os import stat
import sys
import types

from importlib import import_module
from pathlib import Path
from sys import argv as cli_flags

import discord
import lavalink
import pip
import redbot

from redbot.cogs.audio.manager import JAR_BUILD
from redbot.core import commands
from redbot.core.utils.chat_formatting import bold, box
from redbot.core.utils.predicates import MessagePredicate
from stdlib_list import stdlib_list

log = logging.getLogger("red.kreusada.vinfo")
attrs = ["__version__", "version_info", "_version_", "version"]

with open(Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


check_isinstance = lambda x, y: isinstance(getattr(x, y), (str, int, float, list, tuple))

common_modules = f"""
**Red:** {redbot.version_info}
**Python (sys):** {sys.version_info[:3]}
**discord.py:** {discord.__version__}

**PIP**: {pip.__version__}

**Lavalink:** {lavalink.__version__}
**JAR Build:** {JAR_BUILD}
"""


class Vinfo(commands.Cog):
    """
    Get versions of 3rd party cogs, and modules.
    """

    __author__ = ["Kreusada"]
    __version__ = "1.4.1"

    def __init__(self, bot):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    def cog_unload(self):
        with contextlib.suppress(Exception):
            self.bot.remove_dev_env_value("vinfo")

    async def initialize(self) -> None:
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("vinfo", lambda x: self)

    @staticmethod
    def isdev():
        return "--dev" in cli_flags

    @property
    def is_dev(self):
        return self.isdev

    @staticmethod
    def check_attrs(module: types.ModuleType):
        builtin = [sys.version_info[:3], None]
        for attr in attrs:
            if hasattr(module, attr) and check_isinstance(module, attr):
                return [getattr(module, attr), attr]
        if module.__name__ in stdlib_list(".".join([str(x) for x in sys.version_info[:2]])):
            return builtin

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

        embed = discord.Embed(
            title=f"Version Information on {cog}",
            color=await ctx.embed_colour(),
            timestamp=datetime.datetime.now()
        )

        cog_obj = self.bot.get_cog(cog)
        dev_field_value = None

        if not cog_obj:
            version_info_field_value = box(f"- Could not find a cog matching `{cog}`.", lang='diff')
            if self.is_dev():
                dev_field_value = box(
                    f"getattr(bot.get_cog('{cog}'), '__version__')\n"
                    f">>> AttributeError: '{cog}' object has no attribute '__version__'",
                    lang="py"
                )
        else:
            _getattr = getattr(cog_obj, '__version__', None)
            if _getattr is not None:
                version_info_field_value = box(f"{_getattr} ({type(_getattr).__name__})", lang="py")
                if self.isdev():
                    dev_field_value = box(
                        f"getattr(bot.get_cog('{cog}'), '__version__')\n"
                        f">>> '{_getattr}'",
                        lang="py"
                )
            else:
                version_info_field_value = box(f"- Could not find a version for {cog}.", lang='diff')

        embed.add_field(
            name="Version Information",
            value=version_info_field_value,
            inline=False
        )
        if dev_field_value is not None:
            embed.add_field(
                name="Quick Debug",
                value=dev_field_value,
                inline=False
            )
        await ctx.send(embed=embed)

    @vinfo.command(aliases=["module", "dep", "dependency"], usage="<module or dependency>")
    async def mod(self, ctx, module: str = None):
        """Get module versions."""
        if not module:
            embed = discord.Embed(
                title="Common Modules",
                description=common_modules,
                color=await ctx.embed_colour()
            )
            embed.set_footer(
                text="Find a specific module version by adding the module argument."
            )
            await ctx.send(embed=embed)
            return await ctx.send_help()

        await ctx.trigger_typing()

        embed = discord.Embed(
            color=await ctx.embed_colour(),
            timestamp=datetime.datetime.now(),
        )
        try:
            MOD = import_module(module)
        except ModuleNotFoundError as e:
            embed.title = f"Information on {module.upper()}"
            embed.add_field(
                name="Version Information",
                value=box('- ' + str(e), lang="diff")
            )
            if self.isdev():
                embed.add_field(
                    name="Quick Debug",
                    value=box(f"__import__('{module}')\n>>> {e.__class__.__name__}: {e}", lang="py"),
                    inline=False
                )
            await ctx.send(embed=embed)
            return

        check_attrs = self.check_attrs(MOD)
        embed.title = f"Version Information on {MOD.__name__.upper()}"

        if not check_attrs:
            embed.add_field(
                name="Version Information",
                value=box("# Could not find a version for `{}`.", lang="cs").format(MOD.__name__)
            )
            embed.add_field(
                name="Attributes Checked",
                value=box("\n".join(f"- {v}" for v in attrs), lang="diff"),
                inline=False
            )
            await ctx.send(embed=embed)
            return

        attr = f"`{MOD.__name__}.{check_attrs[1]}`"

        if isinstance(check_attrs[0], tuple) and check_attrs[1] is not None:
            value = ("{}." * len(check_attrs[0])).strip('.').format(*check_attrs[0])
            attr = None
        
        elif isinstance(check_attrs[0], (list, tuple)):
            value = ("{}." * len(check_attrs[0])).strip('.').format(*check_attrs[0])

        elif isinstance(check_attrs[0], float):
            value = str(check_attrs[0])

        else:
            value = check_attrs[0]

        embed.add_field(
            name="Version Information",
            value=box(
                text=f"Attribute: {attr}\nFound version info for [{module}]: {value}",
                lang="yaml"
            ),
            inline=False
        )

        if check_attrs[1] is not None:
            reasons = []
            for v in attrs[:attrs.index(check_attrs[1])]:
                _getattr = getattr(MOD, v, None)
                if _getattr is None:
                    reasons.append(f"{v}\n\t| This attribute was not found.")
                else:
                    if not check_isinstance(_getattr):
                        reasons.append(f"{v}\n\t| This attribute was skipped because it was of an unsupported type ({type(_getattr).__name__}).")
                    else:
                        # This *should* never happen
                        reasons.append(f"{v}\n\t| This attribute failed for an unknown reason, consider reporting this.")
                
            embed.add_field(
                name="Attributes Checked",
                value=box("\n".join(f"- {v}" for v in reasons) + f"\n+ {check_attrs[1]}\n\t| Found attribute for {MOD.__name__}!", lang="diff"),
                inline=False
            )
        if not attr.startswith("None"):
            debug = box(
                text=f"getattr(__import__('{MOD.__name__}'), '{check_attrs[1]}')\n>>> {value}",
                lang="py"
            )
            if self.isdev():
                embed.add_field(
                    name="Quick Debug",
                    value=debug,
                    inline=False
                )
        else:
            embed.description = (
                "This library does not have it's own version attribute, "
                f"so it will follow python's version, which is {value}."
            )
        await ctx.send(embed=embed)
