# Most of this code belongs to Jojo, which was authored under the MIT license.
# This cog was transferred to Kreusada (12/04/2021)
# https://github.com/Just-Jojo/JojoCogs

import asyncio
import logging
import random
import typing
from contextlib import suppress

import discord
from redbot.core import Config, commands
from redbot.core.bot import Red
from redbot.core.utils.chat_formatting import pagify

from . import menus

log = logging.getLogger("red.kreusada.mjolnir")

sayings = (
    "The hammer is strong, but so are you. Keep at it!",
    "Mjolnir budges a bit, but remains steadfast, as should you",
    "You've got this! I believe in you!",
    "Don't think it even moved... why don't you try again?",
)


class Mjolnir(commands.Cog):
    """Attempt to lift Thor's hammer!"""

    __version__ = "0.1.2"
    __author__ = ["Jojo", "Kreusada"]

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, 1242351245243535476356, True)
        self.config.register_user(lifted=0)

    async def red_delete_data_for_user(self, *, requester, user_id):
        await self.config.user_from_id(user_id).clear()

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    def cog_unload(self):
        with suppress(Exception):
            self.bot.remove_dev_env_value("mjolnir")

    async def initialize(self) -> None:
        for tester in [719988449867989142, 544974305445019651]:
            if tester in self.bot.owner_ids:
                with suppress(Exception):
                    self.bot.add_dev_env_value("mjolnir", lambda x: self)
                break

    @commands.command()
    async def lifted(self, ctx):
        """Shows how many times you've lifted the hammer."""
        lifted = await self.config.user(ctx.author).lifted()
        plural = "s" if lifted != 1 else ""
        await ctx.send(f"You have lifted Mjolnir {lifted} time{plural}.")

    @commands.cooldown(1, 60.0, commands.BucketType.user)
    @commands.command()
    async def trylift(self, ctx):
        """Try and lift Thor's hammer!"""
        lifted = random.randint(0, 100)
        if lifted >= 95:
            await ctx.send(
                "The sky opens up and a bolt of lightning strikes the ground\nYou are worthy. Hail, son of Odin."
            )
            return await self.config.user(ctx.author).lifted.set(
                (await self.config.user(ctx.author).lifted()) + 1
            )
        await ctx.send(random.choice(sayings))

    @commands.command()
    async def liftedboard(self, ctx):
        """Shows the leaderboard for those who have lifted the hammer."""
        all_users = await self.config.all_users()
        board = sorted(all_users.items(), key=lambda m: m[1]["lifted"], reverse=True)
        sending = []
        for user in board:
            _user = await self.bot.get_or_fetch_user(user[0])
            name = _user.display_name
            amount = user[1]["lifted"]
            sending.append(f"**{name}:** {amount}")
        sending = list(pagify("\n".join(sending)))
        if not len(sending):
            msg = f"No one has lifted Mjolnir yet!\nWill you be the first? Try `{ctx.clean_prefix}trylift`"
            if await ctx.embed_requested():
                embed = discord.Embed(
                    title="Mjolnir!",
                    description=msg,
                    colour=discord.Colour.blue(),
                )
                return await ctx.send(embed=embed)
            return await ctx.send(msg)
        await menus.MjolnirMenu(source=menus.MjolnirPages(sending)).start(
            ctx=ctx, channel=ctx.channel
        )

    async def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            with suppress(discord.Forbidden):
                await ctx.send("Sorry, this is only for guilds!")
            return False
        return True
