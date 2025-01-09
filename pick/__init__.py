import random
from typing import Optional

import discord
from redbot.core import commands
from redbot.core.utils import get_end_user_data_statement
from redbot.core.utils.chat_formatting import inline

__red_end_user_data_statement__ = get_end_user_data_statement(__file__)


class Pick(commands.Cog):
    """Pick a random member."""

    __version__ = "1.0.1"
    __author__ = "Kreusada, saurichable, AAA3A"

    async def red_delete_data_for_user(self, **kwargs):
        # nothing to delete
        return

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nVersion: {self.__version__}\nAuthors : {self.__author__}"

    @commands.command()
    @commands.guild_only()
    async def pick(self, ctx: commands.Context, *, role: Optional[discord.Role] = None):
        """Pick a random member. You may supply a role to pick from."""
        role = role or ctx.guild.default_role
        if not role.members:
            return await ctx.send("That role has no members to pick from.")
        winner = random.choice(role.members)
        embed = discord.Embed(
            description=f"- Mention: {winner.mention} ({inline(winner.mention)})\n- ID: {winner.id}",
            colour=await ctx.embed_colour(),
        )
        embed.set_image(url=winner.banner.url if winner.banner else None)
        embed.add_field(
            name="Chosen amongst:",
            value=f"{role.mention} ({role.id})" if role != ctx.guild.default_role else "Everyone",
        )
        embed.set_author(name=winner, icon_url=winner.avatar.url if winner.avatar else None)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def pickid(self, ctx: commands.Context, *, role: Optional[discord.Role] = None):
        """Pick a random member, displaying the ID only. You may supply a role to pick from.

        This can be integrated with [nestedcommands by tmerc](https://github.com/tmercswims/tmerc-cogs)
        Example of usage: `[p]say Congratulations <@$(pick True)>! You won!`
        """
        if not role.members:
            return await ctx.send("That role has no members to pick from.")
        await ctx.send(str(random.choice((role or ctx.guild.default_role).members).id))


async def setup(bot):
    cog = Pick()
    await bot.add_cog(cog)
