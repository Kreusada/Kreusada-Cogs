import pip
import sys
import redbot
import discord
import lavalink
import logging
import distutils

from redbot.core import commands
from redbot.core.utils.chat_formatting import box, bold

log = logging.getLogger("red.kreusada.vinfo")

base = "{}: {}\n{}: {}.{}.{}\n{}: {}\n\n{}: {}\n{}: {}"

RETURN_TYPE_1 = box("Could not find a version for `{}`. If this is a builtin module, if will follow your python version ({}.{}.{}).", lang='py')
RETURN_TYPE_2 = box("- You do not have an installed module named `{}`.", lang='diff')
RETURN_TYPE_3 = "Builtin Red cogs do not have version attributes by default. Perhaps you're looking for your Red version, which would be {}."

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


class Vinfo(commands.Cog):
    """
    Get versions of 3rd party cogs, and modules.
    """

    __author__ = ["Kreusada", ]
    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def modvinfo_format(mods):
        formatter = (
            bold("Red"),
            redbot.version_info,
            bold("Python"),
            *sys.version_info[:3],
            bold("discord.py"),
            discord.__version__,
            bold("PIP"),
            pip.__version__,
            bold("Lavalink"),
            lavalink.__version__,
        )
        description = mods.format(*formatter)
        embed = discord.Embed(
            title="Common Modules",
            description=description,
        )
        return embed

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad."""
        context = super().format_help_for_context(ctx)
        authors = ", ".join(a for a in self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

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

        if cog not in self.bot.cogs:
            return await ctx.send(f"Could not find a cog matching `{cog}`.")
        
        Cog = self.bot.get_cog(cog)
        
        # Note that cogs won't have a `version_info` attr unlike some modules, so
        # we'll skip finding that attr because it will return False 99% of the time.

        if hasattr(Cog, '__version__'):
            return await ctx.send(f"{cog} version: `{getattr(Cog, '__version__')}`.")
        elif cog in REDBOT_CORE_COGS:
            return await ctx.send(RETURN_TYPE_3.format(redbot.version_info))
        else:
            await ctx.send(f"Could not find a version for {cog}.")

    @vinfo.command(aliases=["module"])
    @commands.bot_has_permissions(embed_links=True)
    async def mod(self, ctx, module: str = None):
        """Get module versions."""
        if not module:
            embed = self.modvinfo_format(base)
            embed.color = await ctx.embed_colour()
            embed.set_footer(text="Find a specific module version by adding the module argument.")
            await ctx.send(embed=embed)
            return await ctx.send_help()

        # If `version_info` is defined, we should refer to this first.
        version_info = 'version_info'
        versionattr = '__version__'
        
        pypath = str(distutils.sysconfig.get_python_lib(standard_lib=True))

        try:
            MOD = __import__(module)
        except ModuleNotFoundError as mnfe:
            return await ctx.send(RETURN_TYPE_2.format(module))

        if hasattr(MOD, version_info):
            vinfo = [getattr(MOD, version_info), '.' + version_info]
        elif hasattr(MOD, versionattr):
            vinfo = [getattr(MOD, versionattr), '.' + version_info]
        elif MOD.__file__.lower().startswith(pypath.lower()):
                vinfo = [(sys.version_info[:3]), " [Python Builtin]"]
        else:
            log.info(f"[From {ctx.channel.id}] {module} path: {MOD.__file__}")
            return await ctx.send(RETURN_TYPE_1.format(MOD.__name__, *sys.version_info[:3]))

        if isinstance(vinfo[0], tuple):
            value = "{}.{}.{}".format(*vinfo[0])
        elif isinstance(vinfo[0], list):
            value = "{}.{}.{}".format(*vinfo[0][:3])
        else:
            value = vinfo[0]

        await ctx.send(
            box(
                f'Attribute: `{MOD.__name__}{vinfo[1]}`\nFound version info for [{module}]: {value}', lang='yaml'
            )
        )