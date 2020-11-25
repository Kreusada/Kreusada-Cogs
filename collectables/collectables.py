from redbot.core import commands, Config, bank, checks
from redbot.core.utils import menus
import asyncio
from .embed import Embed
import discord
import random
import json
import os
import discord
from discord.utils import get
import logging

log = logging.getLogger('red.jojo.collectables')
log.setLevel(logging.INFO)

__version__ = "1.0.0"


class Collectables(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=153607829, force_registration=True)
        self.config.register_guild(
            Vanguards=100
        )
        self.config.register_user(
            collectables={}
        )

    async def page_logic(self, ctx: commands.Context, dictionary: dict, item: str, field_num: int = 15) -> None:
        """Convert a dictionary into a pagified embed"""
        embeds = []
        count = 0
        title = item
        embed = Embed.create(self,
                             ctx=ctx, title=title, thumbnail=ctx.guild.icon_url
                             )
        if len(dictionary.keys()) > field_num:
            for key, value in dictionary.items():
                if count == field_num - 1:
                    embed.add_field(name=key, value=value, inline=True)
                    embeds.append(embed)
                    embed = Embed.create(
                        self, ctx=ctx, title=title, thumbnail=ctx.guild.icon_url
                    )
                    count = 0
                else:
                    embed.add_field(name=key, value=value, inline=True)
                    count += 1
            else:
                embeds.append(embed)
        else:
            for key, value in dictionary.items():
                embed.add_field(name=key, value=value, inline=True)
            embeds.append(embed)
        msg = await ctx.send(embed=embeds[0])
        control = menus.DEFAULT_CONTROLS if len(embeds) > 1 else {
            "\N{CROSS MARK}": menus.close_menu
        }
        asyncio.create_task(menus.menu(ctx, embeds, control, message=msg))
        menus.start_adding_reactions(msg, control.keys())

    @commands.Cog.listener()
    async def on_member_remove(self, member) -> None:
        try:
            await self.config.user(member).clear()
            log.info(
                "Cleared the collectables for {} as they left the server".format(member.name))
        except KeyError:
            return

    @commands.group()
    async def collectable(self, ctx):
        """Commands working with the Collectable cog!"""

    @collectable.command()
    @commands.admin_or_permissions(manage_guild=True)
    async def add(self, ctx, user: discord.Member = None, *, collectable: str = None):
        """Add a collectable to someone's collection"""
        if collectable is not None:
            try:
                collectable_data = await self.config.guild(ctx.guild).get_raw(collectable)
            except KeyError:
                return await ctx.send("I could not find that collectable!")
            data = Embed.create(self, ctx, description="Success!", title="Adding {} to {}'s collection".format(
                collectable, user.display_name), footer="Collectables | Collect them all!")
            await ctx.send(embed=data)
            await self.config.user(user).collectables.set_raw(collectable, value=collectable_data)

    @collectable.command()
    @checks.guildowner_or_permissions(administrator=True)
    async def create(self, ctx, collectable_name: str, price: int = 100):
        """Adds collectables to a user."""
        data = Embed.create(self, ctx, title='Adding {} as a Collectable. :trophy:'.format(collectable_name),
                            description='Added {} as a Collectable which can be purchased for {1}'.format(collectable_name, price))
        await self.config.guild(ctx.guild).set_raw(collectable_name, value=price)
        await ctx.send(embed=data)

    @collectable.command(name="list")
    async def collectable_list(self, ctx):
        """List all of the collectables in your guild"""
        try:
            coll = await self.config.guild(ctx.guild).get_raw()
        except Exception:
            return await ctx.send("Your guild does not have any collectables!\nHave an admin run `{}collectable create <collectable> [cost]` to start collecting!".format(ctx.clean_prefix))
        await self.page_logic(ctx, coll, item="{}'s Collectables".format(ctx.guild.name))

    @collectable.command()
    async def buy(self, ctx, collectable: str):
        """Buys a collectable"""
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
            collectable_list = await self.config.user(user).get_raw("collectables")
        except Exception:
            return await ctx.send("{} doesn't have any collectables!".format(user.display_name))
        await self.page_logic(ctx, collectable_list, item="{}'s items".format(user.display_name))
