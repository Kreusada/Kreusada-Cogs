from redbot.core import commands, Config, bank, checks
from .mdtembed import Embed
import discord
import random
import json
import os
import discord
from discord.utils import get


class Collectables(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=153607829, force_registration=True)
        self.config.register_guild(
            trophy=100
        )
        self.config.register_user(
            collectables={}
        )

    def readable_dict(self, dictionary: dict):
        x = []
        for key, item in dictionary.items():
            y = "{0}: {1}".format(key, item)
            x.append(y)
        return "\n".join(x)

    @commands.group()
    async def collectable(self, ctx):
        """Commands working with the Collectable cog!"""

    @collectable.command(name="add")  # , aliases=["colladd", "addcoll"])
    @checks.guildowner_or_permissions(administrator=True)
    async def add_collectables(self, ctx, collectable_name: str, price: int = 100):
        """Adds collectables to a user."""
        author = ctx.message.author
        data = Embed.create(self, ctx, title='Adding {0} as a Collectable. :trophy:', description='Added {0} as a Collectable which can be purchased for {1}'.format(collectable_name, price))
        data.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=data)
        await self.config.guild(ctx.guild).set_raw(collectable_name, value=price)
        await ctx.send("Added {0} as a Collectable which can be purchased for {1}".format(collectable_name, price))

    @collectable.command(name="list")  # , aliases=["list", "collectlist"])
    async def collectable_list(self, ctx):  # , _global: bool = False):
        collectable_listing = await self.config.guild(ctx.guild).get_raw()
        collectable_list_readable = self.readable_dict(collectable_listing)
        await ctx.send(collectable_list_readable)

    @collectable.command()
    async def buy(self, ctx, collectable: str):
        try:
            cost = await self.config.guild(ctx.guild).get_raw(collectable)
        except KeyError:
            await ctx.send("I could not find that Collectable")
            return

        if await bank.can_spend(ctx.author, cost):
            await self.config.user(ctx.author).collectables.set_raw(
                collectable, value=cost
            )
            await ctx.send("You have purchased {0} for {1}!".format(collectable, cost))
            await bank.withdraw_credits(ctx.author, cost)

    @commands.command()
    async def collectables(self, ctx, user: discord.Member = None):
        """Displays a users collectables."""
        if user is None:
            user = ctx.author
        try:
            coll_list = await self.config.user(user).get_raw("collectables")
        except:
            await ctx.send("{0.display_name} does not have any collectables".format(user))
            return
        coll_list_clean = self.readable_dict(coll_list)
        await ctx.send("{0.display_name}'s collectables:\n{1}".format(user, coll_list_clean))

    @commands.command(name='99', help='Responds with a random quote from Brooklyn 99')
    async def nine_nine(self, ctx):
        brooklyn_99_quotes = [
            'I\'m the human form of the 💯 emoji.',
            'Bingpot!',
            (
                'Cool. Cool cool cool cool cool cool cool, '
                'no doubt no doubt no doubt no doubt.'
            ),
        ]

        await ctx.send(random.choice(brooklyn_99_quotes))
