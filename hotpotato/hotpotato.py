# DISCLAIMER: This cog is a custom fork from Redjumpman's `russianroulette`. I do not claim any of the mechanics for myself, I have just implemented design, theme and response changes.
# A custom fork of russian roulette by Redjumpman

# Standard Library
import asyncio
import itertools
import random
import discord
import contextlib

# Hot Potato
from .kill import outputs
from .hpemb import Embed

# Red
from redbot.core import Config, bank, checks, commands
from redbot.core.errors import BalanceTooHigh


__version__ = "3.1.07"
__author__ = "Redjumpman"


class HotPotato(commands.Cog):
    defaults = {
        "Cost": 50,
        "Chamber_Size": 6,
        "Wait_Time": 60,
        "Session": {"Pot": 0, "Players": [], "Active": False},
    }

    def __init__(self):
        self.config = Config.get_conf(self, 5074395004, force_registration=True)
        self.config.register_guild(**self.defaults)

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    @commands.guild_only()
    @commands.command()
    async def hotpotato(self, ctx):
        """Start or join a game of Hot Potato.
        The game will not start if no players have joined. You might 
        aswell just eat the potato.
        The maximum number of players in a circle is determined by the
        size of the chamber. For example, a chamber size of 6 means the
        maximum number of players will be 6.
        """
        settings = await self.config.guild(ctx.guild).all()
        if await self.game_checks(ctx, settings):
            await self.add_player(ctx, settings["Cost"])

    @commands.guild_only()
    @checks.admin_or_permissions(administrator=True)
    @commands.command(hidden=True)
    async def potatoreset(self, ctx):
        """ONLY USE THIS FOR DEBUGGING PURPOSES"""
        await self.config.guild(ctx.guild).Session.clear()
        await ctx.send("The Hot Potato sesssion on this server has been cleared.")

    @commands.command()
    async def hotpotatoversion(self, ctx):
        """Shows the cog version."""
        embed = Embed.create(
            self, ctx, title="Cog Version",
            description="You are using hot potato version {}".format(__version__)
        )
        await ctx.send(embed=embed)

    @commands.group(autohelp=True)
    @commands.guild_only()
    @checks.admin_or_permissions(administrator=True)
    async def setpotato(self, ctx):
        """Hot Potato Settings group."""
        pass

    @setpotato.command()
    async def table(self, ctx, size: int):
        """Sets the number of chairs the table has. MAX: 12."""
        if not 1 < size <= 12:
            embed = Embed.create(
                self, ctx, title="<:error:777117297273077760> Invalid",
                description="Invalid table size. Must be in the range of 2 - 12."
            )
            return await ctx.send(embed=embed)
        embed = Embed.create(
            self, ctx, title="<:success:777167188816560168> Success",
            description="Table size set to {}.".format(size)
        )
        await self.config.guild(ctx.guild).Chamber_Size.set(size)
        await ctx.send(embed=embed)
                

    @setpotato.command()
    async def cost(self, ctx, amount: int):
        """Sets the required cost to play."""
        if amount < 0:
            return await ctx.send("You are an idiot.")
        await self.config.guild(ctx.guild).Cost.set(amount)
        currency = await bank.get_currency_name(ctx.guild)
        await ctx.send("Required cost to play set to {} {}.".format(amount, currency))

    @setpotato.command()
    async def wait(self, ctx, seconds: int):
        """Set the wait time (seconds) before starting the game."""
        if seconds <= 0:
            embed = Embed.create(
                self, ctx, title="<:error:777117297273077760> Invalid",
                description="You are an idiot."
            )
            return await ctx.send(embed=embed)
        embed = Embed.create(
            self, ctx, title="<:success:777167188816560168> Success",
            description="The time before a hot potato game starts is now {} seconds.".format(seconds)
        )
        await self.config.guild(ctx.guild).Wait_Time.set(seconds)
        await ctx.send(embed=embed)

    async def game_checks(self, ctx, settings):
        if settings["Session"]["Active"]:
            with contextlib.suppress(discord.Forbidden):
                embed = Embed.create(
                    self, ctx, title="<:error:777117297273077760> Invalid",
                    description="You cannot join or start a game of hot potato while one is active."
                )
                await ctx.author.send(embed=embed)
            return False

        if ctx.author.id in settings["Session"]["Players"]:
            embed = Embed.create(
                self, ctx, title="<:error:777117297273077760> Invalid",
                description="You are already sat waiting to be served!"
            )
            await ctx.send(embed=embed)
            return False

        if len(settings["Session"]["Players"]) == settings["Chamber_Size"]:
                embed = Embed.create(
                    self, ctx, title="<:error:777117297273077760> Oopsies!",
                    description="There's no chairs left at the hot potato table. Wait for this game to finish to join."
                )
                await ctx.send(embed=embed)
                return false

        try:
            await bank.withdraw_credits(ctx.author, settings["Cost"])
        except ValueError:
            currency = await bank.get_currency_name(ctx.guild)
            embed = Embed.create(
                self, ctx, title="<:error:777117297273077760> Oopsies!",
                description="Insufficient funds! This game requires {} {}.".format(settings["Cost"], currency)
            )
            await ctx.send(embed=embed)
            return False
        else:
            return True

    async def add_player(self, ctx, cost):
        current_pot = await self.config.guild(ctx.guild).Session.Pot()
        await self.config.guild(ctx.guild).Session.Pot.set(value=(current_pot + cost))

        async with self.config.guild(ctx.guild).Session.Players() as players:
            players.append(ctx.author.id)
            num_players = len(players)

        if num_players == 1:
            wait = await self.config.guild(ctx.guild).Wait_Time()
            embed = Embed.create(
                self, ctx, title="Attention! :loudspeaker:",
                description=(
                    "{0.author.mention} is gathering players for a game of hot potato!"
                    "\nType `{0.prefix}hotpotato` to enter. "
                    "The round will start in {1} seconds."
                    .format(
                        ctx, wait
                    )
                )
            )
            await ctx.send(embed=embed)
            await asyncio.sleep(wait)
            await self.start_game(ctx)
        else:
            await ctx.send("**{} sat down at the table, ready to be served their hot potato.** :potato:".format(ctx.author.mention))

    async def start_game(self, ctx):
        await self.config.guild(ctx.guild).Session.Active.set(True)
        data = await self.config.guild(ctx.guild).Session.all()
        players = [ctx.guild.get_member(player) for player in data["Players"]]
        filtered_players = [player for player in players if isinstance(player, discord.Member)]
        if len(filtered_players) < 2:
            try:
                await bank.deposit_credits(ctx.author, data["Pot"])
            except BalanceTooHigh as e:
                await bank.set_balance(ctx.author, e.max_balance)
            await self.reset_game(ctx)
            return await ctx.send("You can't play by youself, or you'd might aswell just sizzle alone.\nGame reset and cost refunded.")
        chamber = await self.config.guild(ctx.guild).Chamber_Size()

        counter = 1
        while len(filtered_players) > 1:
            embed = Embed.create(
                self, ctx, title="**Round {}**".format(counter),
                description=(
                    "*{} takes the potato out of the oven "
                    "and gets ready to serve it... without "
                    "plates! I guess you'll just have to use your hands...*"
                    .format(
                        ctx.bot.user.name
                    )
                )
            )
            await ctx.send(embed=embed)
            await asyncio.sleep(3)
            await self.start_round(ctx, chamber, filtered_players)
            counter += 1
        await self.game_teardown(ctx, filtered_players)

    async def start_round(self, ctx, chamber, players):
        position = random.randint(1, chamber)
        while True:
            for turn, player in enumerate(itertools.cycle(players), 1):
                await ctx.send(
                    ":potato: {} holds the potato in their hands, bearing the extreme heat.".format(player.name)
                )
                await asyncio.sleep(5)
                if turn == position:
                    players.remove(player)
                    msg = ":fire: **Sizzled.** {0} was burnt to the stake.\n"
                    msg += random.choice(outputs)
                    await ctx.send(msg.format(player.mention, random.choice(players).name, ctx.guild.owner))
                    await asyncio.sleep(3)
                    break
                else:
                    await ctx.send("<:error:777117297273077760> **PHEW!** {} shakes their hand frantically as they pass the potato along.".format(player.name))
                    await asyncio.sleep(3)
            break

    async def game_teardown(self, ctx, players):
        winner = players[0]
        currency = await bank.get_currency_name(ctx.guild)
        total = await self.config.guild(ctx.guild).Session.Pot()
        embed = Embed.create(
            self, ctx, title="<:dollarbag:778687019944771616> Congratulations!",
            description="{}, you are the last person who hasn't been sizzled, and have won a total of {} {}. Play again using {}hotpotato!"
            .format(
                winner.mention,
                total,
                currency,
                ctx.clean_prefix
            )
        )
        try:
            await bank.deposit_credits(winner, total)
        except BalanceTooHigh as e:
            await bank.set_balance(winner, e.max_balance)
        await ctx.send(embed=embed)
        await self.reset_game(ctx)

    async def reset_game(self, ctx):
        await self.config.guild(ctx.guild).Session.clear()
