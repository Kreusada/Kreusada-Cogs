import os
import json
import random
import discord
import asyncio
import logging
from .embed import Embed
from discord.utils import get
from redbot.core.utils import menus
from redbot.core import commands, Config, bank, checks

log = logging.getLogger('red.kreusada.gifts')
log.setLevel(logging.INFO)

class Gifts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=153607829, force_registration=True)
        self.config.register_user(
        )
        self.config.register_user(
            collectables={}
        )
        
    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def gift(self, ctx):
        """Open a gift!"""
        gift, image = (random.choice(list(GIFTS.items())))
        collection = await self.config.user(ctx.author).collection.get_raw()
        await self.g_logistics(ctx, gift, collection)
        data = Embed.create(
            self, ctx, title='You got {}'.format(gift),
            description="Testing"
        )
        data.set_image(url=image)
        await ctx.send(embed=data)
    
    @commands.command(aliases=["c"])
    async def collection(self, ctx):
        try:
            collection: dict = await self.config.user(ctx.author).collection.get_raw()
        except KeyError:
            collection: dict = await self.config.user(ctx.author).collection.get_raw()
        if len(collection.values()) > 0:
            collection = "\n".join(
                ["{} | {}".format(gift, value) for gift, value in collection.items()]
            )
            embed = discord.Embed(
                title="{ctx.author.name}'s Collection", color=ctx.author.color, description="Testing"
            )
            embed.add_field(name=random.choice(COLLS).format(value=roster)
                            else:
                                embed = discord.Embed(
                                    title=random.choice(COLLN), color=ctx.author.color, description=(
                                        "It appears that you haven't opened any gifts yet.\n"
                                        "Collect some using `{ctx.clean_prefix}gift`!".
                                     )
                                  )
                            await ctx.send(embed=embed)

    async def g_logistics(self, ctx: commands.Context, gift: str, collection: dict) -> None:
        int = int
        try:
            addon = 1
        try:
            collection[gift] += addon
        except KeyError:
            collection[gift] = 0
        await self.config.user(ctx.author).collection.set_raw(value=collection)
