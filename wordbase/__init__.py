"""The WordBase module. Generate rhymes, use a reverse dictionary, and more word related generators."""

import contextlib
import json
import pathlib
from typing import Dict, List, Literal, Union

import aiohttp
import discord
import redbot
from redbot import VersionInfo
from redbot.core import Config, commands
from redbot.core.bot import Red
from redbot.core.utils.chat_formatting import box, error, spoiler, warning
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu

if redbot.version_info >= VersionInfo.from_str("3.4.15"):
    from redbot.core.utils.chat_formatting import success
else:

    def success(text: str) -> str:
        return f"\N{WHITE HEAVY CHECK MARK} {text}"


DEFAULT_DESCRIPTION = """
These words are ordered based on a given score for their accuracy.
You should see the words at the first pages for more accurate findings.
""".strip()

WordType = Literal["rhy", "hom", "trg", "cns", "ml"]


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


TYPES = {
    "rhy": {
        "endpoint": "https://api.datamuse.com/words?rel_rhy=",
        "extra_description": "The number in squared brackets shows you how many syllables there are.",
        "title": 'Words rhyming with "{}"',
    },
    "hom": {
        "endpoint": "https://api.datamuse.com/words?rel_hom=",
        "extra_description": "The number in squared brackets shows you how many syllables there are.",
        "title": 'Homophones for the word "{}"',
    },
    "trg": {
        "endpoint": "https://api.datamuse.com/words?rel_trg=",
        "extra_description": "Most of these words will be closely related to your input.",
        "title": 'Triggers for the word "{}"',
    },
    "cns": {
        "endpoint": "https://api.datamuse.com/words?rel_cns=",
        "extra_description": "The number in squared brackets shows you how many syllables there are.",
        "title": 'Consonant matches for the word "{}"',
    },
    "ml": {
        "endpoint": "https://api.datamuse.com/words?ml=",
        "extra_description": "These are words that **could** match the definition provided.\n```yaml\nDefinition: {}\n```",
        "title": "Reverse dictionary words",
    },
}

with open(pathlib.Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


class WordBase(commands.Cog):
    """Generate rhymes, use a reverse dictionary, and more word related generators."""

    __author__ = ["Kreusada"]
    __version__ = "1.0.0"

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, 408953096836490568, True)
        self.config.register_global(blocked_words=[])
        self.session = aiohttp.ClientSession()
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(RuntimeError, ValueError):
                self.bot.add_dev_env_value(self.__class__.__name__.lower(), lambda x: self)

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(KeyError):
                self.bot.remove_dev_env_value(self.__class__.__name__.lower())

    async def create_menu(
        self,
        ctx: commands.Context,
        word_type: WordType,
        word: str,
        data: List[Dict[str, Union[str, int]]],
    ):
        blocked_words = await self.config.blocked_words()
        embed_list = []
        description = DEFAULT_DESCRIPTION + "\n" + TYPES[word_type].get("extra_description", "")
        description = description.format(word)
        for x in data:
            if x["word"] in blocked_words:
                data.remove(x)
        sorted_data = list(chunks(sorted(data, key=lambda x: x.get("score", 0), reverse=True), 10))
        if len(data) + 1 <= 9:
            filler = 1
        elif len(data) + 1 <= 99:
            filler = 2
        else:
            filler = 3
        placement = lambda x: str(data.index(x) + 1).zfill(filler)
        for w in sorted_data:
            message = ""
            for x in w:
                if word_type in ("rhy", "hom", "cns"):
                    message += f"#{placement(x)} [{x['numSyllables']}] > {x['word']}\n"
                else:
                    message += f"#{placement(x)} > {x['word']}\n"
            embed = discord.Embed(
                title=TYPES[word_type]["title"].format(word),
                description=description + box(message, "css"),
                color=await ctx.embed_colour(),
            )
            embed.set_footer(
                text=f"Page {sorted_data.index(w)+1}/{len(sorted_data)} | Powered by {self.bot.user.name}"
            )
            embed_list.append(embed)
        if len(embed_list) > 1:
            await menu(ctx, embed_list, DEFAULT_CONTROLS)
        else:
            await ctx.send(embed=embed_list[0])

    async def gettinfo(
        self,
        ctx: commands.Context,
        word_type: WordType,
        word: str,
    ):
        try:
            async with self.session.get(TYPES[word_type]["endpoint"] + word) as session:
                data = await session.json()
        except aiohttp.ClientError:
            await ctx.maybe_send_embed(warning("Failed to connect to the API."))
            return
        else:
            if not data:
                if word_type == "ml":
                    message = "No words found for this definition."
                else:
                    message = "No matches found for this word."
                return await ctx.maybe_send_embed(error(message))
            await self.create_menu(ctx, word_type, word, data)

    @commands.command()
    @commands.has_permissions(embed_links=True)
    async def rhymes(self, ctx: commands.Context, word: str):
        """Get rhymes for a word."""
        await ctx.trigger_typing()
        await self.gettinfo(ctx, "rhy", word)

    @commands.command()
    @commands.has_permissions(embed_links=True)
    async def homophones(self, ctx: commands.Context, word: str):
        """Get homophones for a word."""
        await ctx.trigger_typing()
        await self.gettinfo(ctx, "hom", word)

    @commands.command()
    @commands.has_permissions(embed_links=True)
    async def triggers(self, ctx: commands.Context, word: str):
        """Get triggers for a word."""
        await ctx.trigger_typing()
        await self.gettinfo(ctx, "trg", word)

    @commands.command()
    @commands.has_permissions(embed_links=True)
    async def consonants(self, ctx: commands.Context, word: str):
        """Get consonant matches for a word."""
        await ctx.trigger_typing()
        await self.gettinfo(ctx, "cns", word)

    @commands.command()
    @commands.has_permissions(embed_links=True)
    async def reversedefine(self, ctx: commands.Context, *, definition: str):
        """Get a list of words from a definition."""
        await ctx.trigger_typing()
        await self.gettinfo(ctx, "ml", definition)

    @commands.group()
    async def wordbase(self, ctx: commands.Context):
        """Manage WordBase."""

    @wordbase.command(name="block")
    @commands.is_owner()
    async def wordbase_block(self, ctx: commands.Context, word: str):
        """Block profanic words from appearing in WordBase commands."""
        word = word.strip("||")
        async with self.config.blocked_words() as blocked:
            if word in blocked:
                return await ctx.send(f"The word {spoiler(word)} is already blocked.")
            blocked.append(word)
        await ctx.maybe_send_embed(
            success(f"Word {spoiler(word)} added to the wordbase blocked words list.")
        )

    @wordbase.command(name="unblock")
    @commands.is_owner()
    async def wordbase_unblock(self, ctx: commands.Context, word: str):
        """Unblock profanic words to appear in WordBase commands."""
        word = word.strip("||")
        async with self.config.blocked_words() as blocked:
            if word not in blocked:
                return await ctx.send(f"The word {spoiler(word)} was not already blocked.")
            blocked.remove(word)
        await ctx.maybe_send_embed(
            success(f"Word {spoiler(word)} removed from the wordbase blocked words list.")
        )

    @wordbase.command(name="clrblock")
    @commands.is_owner()
    async def wordbase_clrblock(self, ctx: commands.Context):
        """Clear the WordBase blocklist."""
        async with self.config.blocked_words() as blocked:
            blocked.clear()
        await ctx.maybe_send_embed(success(f"Blocked word list cleared."))

    @wordbase.command(name="blocklist")
    @commands.is_owner()
    async def wordbase_blocklist(self, ctx: commands.Context, spoilers: bool = True):
        """See the current blocked words."""
        blocked_words = await self.config.blocked_words()
        if not blocked_words:
            return await ctx.send("There are no blocked words.")
        title = "**WordBase blocked words**\n\n"
        await ctx.maybe_send_embed(
            title + ", ".join(map(spoiler if spoilers else lambda x: x, blocked_words))
        )


def setup(bot):
    bot.add_cog(WordBase(bot))
