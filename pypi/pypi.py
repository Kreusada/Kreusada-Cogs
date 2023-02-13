import io
import json
import re
from pathlib import Path

import aiohttp
import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import box, humanize_list, inline, italics, pagify

from .utils import JumpUrlView

URL_RE = re.compile(r"(https?|s?ftp)://(\S+)", re.I)
PYTHON_LOGO = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/2048px-Python-logo-notext.svg.png"


class PyPi(commands.Cog):
    """Get information about a package available on PyPi."""

    __author__ = ["Kreusada", "OofChair"]
    __version__ = "1.1.0"

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = humanize_list(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def cog_unload(self):
        await self.session.close()

    @staticmethod
    def format_classifier_url(classifier: str, include_prefix: bool = False) -> str:
        split = classifier.split(" :: ")
        replace = lambda x: x.replace(" ", "+")
        url = "+%3A%3A+".join(map(replace, split))
        if include_prefix:
            return "https://pypi.org/search/?c=" + url
        return url

    def format_classifiers_url(self, classifiers, include_prefix: bool = True):
        return ("https://pypi.org/search/?c=" if include_prefix else "") + "&c=".join(
            map(self.format_classifier_url, classifiers)
        )

    @staticmethod
    def get_send_kwargs(embed: discord.Embed, **kwargs):
        embed.set_author(
            name="Python Package Index", icon_url=PYTHON_LOGO, url="https://pypi.org/"
        )
        embed.color = 0x3498DB
        kwargs["embed"] = embed
        return kwargs

    async def make_request(self, url: str):
        async with self.session.get(url) as request:
            if request.status != 200:
                raise ValueError
            return await request.json()

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def pypi(self, ctx, project: str):
        """Get information about a project on PyPi."""
        await ctx.typing()
        try:
            request = await self.make_request(f"https://pypi.org/pypi/{project}/json")
        except ValueError:
            embed = discord.Embed(description=f'There were no results for "{project}".')
            kwargs = self.get_send_kwargs(embed)
            return await ctx.send(embed=embed)

        info = request["info"]
        releases = request["releases"]

        kwargs = {}

        embed = discord.Embed(title=f"{info['name']} {info['version']}", url=info["package_url"])
        embed.description = info["summary"] or italics(
            "No description was provided for this project."
        )

        if (author := info["author"]) and author != " ":
            embed.add_field(name="Author", value=author)

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
        if len(license) > 35:
            bytesio = io.BytesIO(license.encode("utf-8"))
            license = "[TRUNCATED] See file attached"
            kwargs["file"] = discord.File(bytesio, filename="LICENSE")
        embed.add_field(name="License", value=license)

        embed.add_field(name="Releases", value=len(releases))

        if python_requires := info["requires_python"]:
            name = "Python Version Requirement"
            if len(python_requires.split(",")) > 1:
                name += "s"
            embed.add_field(
                name=name,
                value="\n".join(f"- {inline(x.strip())}" for x in python_requires.split(",")),
                inline=False,
            )

        value = f"• [PyPi Stats (provided by PePy)](https://pepy.tech/project/{info['name']})"
        classifier_url = f"\n• [Other projects with this project's classifiers]({self.format_classifiers_url(info['classifiers'])})"

        if len(classifier_url) <= 900:
            value += classifier_url

        embed.add_field(
            name="Other URLs",
            value=value,
            inline=False,
        )

        embed.add_field(
            name="Installation",
            value=box(f"pip install -U {info['name']}"),
            inline=False
        )

        filtered_links = dict(filter(lambda x: URL_RE.match(x[1]), list(info["project_urls"].items())))
        for link in info["project_urls"].values():
            if "github.com" in link and "issues" not in link and "pulls" not in link:
                link = ("https://api.github.com/repos/" + link[19:]).rstrip(".git")
                details = await self.make_request(link)
                default_branch = details["default_branch"]
                break
        else:
            default_branch = None
        
        if default_branch:
            embed.add_field(
                name="Development Installation",
                value=box(f"pip install -U git+{link}@{default_branch}#egg={info['name']}", lang="fix"),
                inline=False,
            )

        values = []
        for release in list(releases.keys())[-5:]:
            release_time = releases[release][-1]['upload_time'][:10]
            release_time = "-".join(reversed(release_time.split("-"))) # format date properly
            values.append(f"+ {release} (~{release_time})")
        embed.add_field(
            name="Recent Releases",
            value=box("\n".join(values), lang="diff"),
            inline=False
        )

        if requires_dist := info["requires_dist"]:
            value = "\n".join("• " + d.replace("(", "[").replace(")", "]") for d in requires_dist[:10])
            if remaining := requires_dist[10:]:
                value += f"\nand {len(remaining)} more..."
            embed.add_field(
                name="Requires Dist",
                value=box(value, lang="ini"),
                inline=False,
            )

        if classifiers := info["classifiers"]:
            sort = sorted(classifiers, key=lambda x: len(x.split("::")[0]))
            data = "\n".join(sort)
            if len(data) <= 1000:
                embed.add_field(
                    name=f"Classifiers ({len(classifiers)})",
                    value=box("\n".join(sort), lang="asciidoc"),
                    inline=False,
                )
            else:
                for _, page in enumerate(pagify(data, page_length=1000)):
                    title = "Classifiers"
                    if _:  # Non-zero ints == True
                        title += " (continued)"
                    embed.add_field(name=title, value=box(page, lang="asciidoc"), inline=False)

        kwargs["view"] = JumpUrlView(info["package_url"], project_urls=filtered_links)
        proper_kwargs = self.get_send_kwargs(embed, **kwargs)
        await ctx.send(**proper_kwargs)
