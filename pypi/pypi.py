import contextlib
import json
import re
from pathlib import Path

import aiohttp
import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import box, inline, italics

URL_RE = re.compile(r"(https?|s?ftp)://(\S+)", re.I)
PYTHON_LOGO = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/2048px-Python-logo-notext.svg.png"


with open(Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


class PyPi(commands.Cog):
    """Get information about a package available on PyPi."""

    __author__ = ["Kreusada", "OofChair"]
    __version__ = "1.0.0"
    __dev_ids__ = [719988449867989142, 572944636209922059]

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    def __init__(self, bot):
        self.bot = bot
        for user in self.__dev_ids__:
            if user in self.bot.owner_ids:
                with contextlib.suppress(RuntimeError, ValueError):
                    self.bot.add_dev_env_value(self.__class__.__name__.lower(), lambda x: self)

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())
        with contextlib.suppress(Exception):
            self.bot.remove_dev_env_value(self.__class__.__name__.lower())

    @commands.command()
    async def pypi(self, ctx, project: str):
        async with self.session.get(f"https://pypi.org/pypi/{project}/json") as request:
            if request.status != 200:
                return await ctx.send("Project not found.")
            request = await request.json()

        info = request["info"]

        embed = discord.Embed(
            title=f"{info['name']} {info['version']}", color=0x3498DB, url=info["package_url"]
        )
        embed.description = info["summary"] or italics(
            "No description was provided for this project."
        )

        embed.add_field(name="Author", value=info["author"] or "Unknown")

        license = info["license"] or "UNKNOWN"
        # License is UNKNOWN if unprovided
        if license == "UNKNOWN":
            for c in info["classifiers"]:
                if "License" in c:
                    license = c.split("::")[-1].strip()
                    break
            if license == "UNKNOWN":
                #  If it's still unknown
                license = license.capitalize()
        embed.add_field(name="License", value=license)

        if (python_requires := info["requires_python"]) :
            name = "Python Version Requirement"
            if len(python_requires.split(",")) > 1:
                name += "s"
            embed.add_field(
                name=name,
                value="\n".join(f"- {inline(x.strip())}" for x in python_requires.split(",")),
                inline=False,
            )

        if (links := info["project_urls"]) :
            filtered_links = filter(lambda x: re.match(URL_RE, x[1]), list(links.items()))
            embed.add_field(
                name="Project URLs",
                value="\n".join(f"- [{k}]({v})" for k, v in filtered_links),
                inline=False,
            )

        if (classifiers := info["classifiers"]) :
            sort = sorted(classifiers, key=lambda x: len(x.split("::")[0]))
            embed.add_field(
                name=f"Classifiers ({len(classifiers)})",
                value=box("\n".join(sort), lang="asciidoc"),
            )

        embed.set_author(
            name="Python Package Index", icon_url=PYTHON_LOGO, url="https://pypi.org/"
        )
        await ctx.send(embed=embed)
