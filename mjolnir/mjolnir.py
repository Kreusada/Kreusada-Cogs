"""
MIT License

Copyright (c) 2020-2021 Jojo#7711

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

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

_sayings = (
    "The hammer is strong, but so are you. Keep at it!",
    "Mjolnir budges a bit, but remains steadfast, as should you",
    "You've got this! I believe in you!",
    "Don't think it even moved... why don't you try again?",
)


class Mjolnir(commands.Cog):
    """Attempt to lift Thor's hammer!"""

    __version__ = "0.1.2"

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, 1242351245243535476356, True)
        self.config.register_user(lifted=0)

    async def red_delete_data_for_user(self, *, requester, user_id):
        await self.config.user_from_id(user_id).clear()

    @commands.command()
    async def lifted(self, ctx):
        """Shows how many times you've lifted the hammer."""
        lifted = await self.config.user(ctx.author).lifted()
        plural = "s" if lifted > 1 else ""
        sending = f"You have lifted Mjolnir {lifted} time{plural}."
        await ctx.send(content=sending)

    @commands.cooldown(1, 60.0, commands.BucketType.user)
    @commands.command()
    async def trylift(self, ctx):
        """Try and lift Thor's hammer!"""
        lifted = random.randint(0, 100)
        if lifted >= 95:
            await ctx.send(
                "The sky opens up and a bolt of lightning strikes the ground\nYou are worthy. Hail, son of Odin"
            )
            return await self.config.user(ctx.author).lifted.set(
                (await self.config.user(ctx.author).lifted()) + 1
            )

        await ctx.send(random.choice(_sayings))

    @commands.command()
    async def liftedboard(self, ctx):
        """Shows the leaderboard for those who have lifted the hammer."""
        all_users = await self.config.all_users()
        board = sorted(
            all_users.items(),
            key=lambda m: m[1]["lifted"],
            reverse=True,
        )  # Wow, that was easy
        sending = []
        for user in board:
            _user = await self.bot.get_or_fetch_user(user[0])
            name = _user.display_name
            amount = user[1]["lifted"]
            sending.append(f"**{name}:** {amount}")
        sending = list(pagify("\n".join(sending)))
        if not len(sending):
            if await ctx.embed_requested():
                msg = f"No one has lifted Mjolnir yet!\nWill you be the first? Try `{ctx.clean_prefix}trylift`"
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
                await ctx.send("This cog is only for guilds! Sorry!")
            return False
        return True
