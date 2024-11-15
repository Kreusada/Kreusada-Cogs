import aiohttp
import discord
from redbot.core import Config, commands
from redbot.core.bot import Red
from redbot.core.utils import get_end_user_data_statement

__red_end_user_data_statement__ = get_end_user_data_statement(__file__)


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


class Rhymes(commands.Cog):
    """Generate rhymes."""

    __author__ = "Kreusada"
    __version__ = "1.0.0"

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, 408953096836490568, True)
        self.config.register_global(blocked_words=[])
        self.session = aiohttp.ClientSession()

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    async def cog_unload(self):
        await self.session.close()

    async def red_delete_data_for_user(self, **kwargs):
        return

    @commands.command()
    @commands.has_permissions(embed_links=True)
    async def rhymes(self, ctx: commands.Context, word: str):
        """Get rhymes for a word."""
        await ctx.typing()
        async with self.session.get("https://api.datamuse.com/words?rel_rhy=" + word) as session:
            data = await session.json()
        embed = discord.Embed(
            title=f"Words rhyming with '{word.lower()}' ({len(data)})",
            colour=await ctx.embed_colour(),
        )
        for rhymes in [["- " + rhyme["word"] for rhyme in chunk] for chunk in chunks(data, 10)]:
            embed.add_field(name="\u2800", value="\n".join(rhymes))
        await ctx.send(embed=embed)


async def setup(bot: Red):
    await bot.add_cog(Rhymes(bot))
