import discord
from asyncio import sleep
from random import randint
from redbot.core import bank, commands, Config
from redbot.core.utils.chat_formatting import bold as b

from .generators import embed
from .cards import BACKALL

class HigherOrLower(commands.Cog):
    """
    Play the higher or lower card game!
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 439583, force_registration=True)
        self.config.register_guild(
            bank=False,
            round=0,
            per=0
            )
        self.config.register_user(
            score=0, 
            wins=0,
            draw=None,
            image=False
            )

    @commands.command()
    async def hol(self, ctx):
        """
        Play higher or lower!

        Guess if the next number will be higher or lower based on a standard pack of cards.
        For more information, please take a look [here](http://www.higherlowergame.com/how-to-play).
        """
        banke = await self.config.guild(ctx.guild).bank()
        currency = await bank.get_currency_name(ctx.guild)
        per = await self.config.guild(ctx.guild).per()
        round = await self.config.guild(ctx.guild).round()
        await ctx.send(f"Let's get started {ctx.author.name}. Remember to answer with either `higher` or `lower`.")

        def check(x):
            return x.author == ctx.author and x.channel == ctx.channel and x.content.startswith(("higher"m "lower", "h", "l"))

        for i in range(9):
            draw = await self.config.user(ctx.author).draw()
            if not draw:
                A = randint(2, 14)
            else:
                A = draw
            B = randint(2, 14)
            await sleep(1)
            E = await embed(ctx.author.name, A, await self.config.user(ctx.author).image())
            await ctx.send(embed=E)
            choice = await self.bot.wait_for("message", timeout=40, check=check)
            if choice.content.lower().startswith(("higher", "lower")) and B > A:
                e = discord.Embed(description=f"✅ Great work! The next number is...", color=0x00FF00)
                if banke is True:
                    await bank.deposit_credits(ctx.author, per)
                    e.set_footer(text=f"+{per} has been added to your bank account.")
                await ctx.send(embed=e)
                await self.config.user(ctx.author).draw.set(B)
                continue
            elif choice.content.startswith(("lower", "l")) and B < A:
                e = discord.Embed(description=f"✅ Great work! The next number is...", color=0x00FF00)
                if banke is True:
                    e.set_footer(text=f"+{per} has been added to your bank account.")
                    await bank.deposit_credits(ctx.author, per)
                await ctx.send(embed=e)
                await self.config.user(ctx.author).draw.set(B)
                continue
            elif choice.content.startswith("higher") and B == A or choice.content.startswith("lower") and B == A:
                e = discord.Embed(description=f"😌 The results were the same! The next number is...", color=0xFFFF00)
                if banke is True:
                    e.set_footer(text=f"+{per} has been added to your bank account.")
                    await bank.deposit_credits(ctx.author, per)
                await ctx.send(embed=e)
                await self.config.user(ctx.author).draw.set(B)
                continue
            else:
                break
        else:
            if banke is True:
                description = f"🎉 You MADE IT {ctx.author.name}!! Awesome work!\n{round} {currency} has been added to your bank account."
            E = discord.Embed(description=f"🎉 You MADE IT {ctx.author.name}!! Awesome work!")
            if banke is True:
                await self.config.guild(ctx.guild).deposit_credits(ctx.author, round)
            await self.config.user(ctx.author).draw.set(None)
        if B == 11:
            B = "Jack"
        elif B == 12:
            B = "Queen"
        elif B == 13:
            B = "King"
        elif B == 14:
            B = "Ace"
        else:
            B = B
        e = discord.Embed(description=f"❌ Oh no {ctx.author.name}! The next card was a {B}.", color=0xFF0000)
        await ctx.send(embed=e)
        await self.config.user(ctx.author).draw.set(None)

    @commands.group()
    async def holset(self, ctx):
        """Settings for higher or lower."""

    @holset.command()
    @commands.mod_or_permissions(administrator=True)
    async def perpayout(self, ctx, payout: int):
        """Sets the bank payout per answer."""
        currency = await bank.get_currency_name(ctx.guild)
        if payout > 1000:
            await ctx.send(f"{payout} exceeds the maximum payout. Please go lower.")
        else:
            await self.config.guild(ctx.guild).per.set(payout)
            await ctx.send(f"Done. Users will now receive {payout} {currency} when they correctly guess a card.")

    @holset.command()
    @commands.mod_or_permissions(administrator=True)
    async def roundpayout(self, ctx, payout: int):
        """Sets the bank payout if all 9 cards are correctly guessed."""
        currency = await bank.get_currency_name(ctx.guild)
        if payout > 100000:
            await ctx.send(f"{payout} exceeds the maximum payout. Please go lower.")
        else:
            await self.config.guild(ctx.guild).round.set(payout)
            await ctx.send(f"Done. Users will now receive {payout} {currency} when they correctly guess all nine cards.")
        
    @holset.command()
    @commands.mod_or_permissions(administrator=True)
    async def togglebank(self, ctx, true_or_false: bool = False):
        """Toggle the bank ON. Defaults to False."""
        if true_or_false is False:
            await self.config.guild(ctx.guild).bank.set(False)
            await ctx.send(
                f"The bank is now off.\n"
                f"You can turn it on by using `{ctx.clean_prefix}holset togglebank true`."
            )
        else:
            await self.config.guild(ctx.guild).bank.set(True)
            await ctx.send(
                f"The bank is now ON.\n"
                f"Round payout: {int(await self.config.guild(ctx.guild).round())} <-"
                f"`Modify using {ctx.clean_prefix}holset roundpayout`.\n"
                f"Per-card payout: {int(await self.config.guild(ctx.guild).per())} <-"
                f"`Modify using {ctx.clean_prefix}holset perpayout`."
            )

    @holset.command()
    async def image(self, ctx, true_or_false: bool):
        """
        Specify whether you would like an image card.

        Defaults are set to False (thumbnail).
        """
        if true_or_false is False:
            await self.config.user(ctx.author).image.set(False)
            E = discord.Embed(title="Thumbnail responses", description="Embeds will now be sent like this.", color=0xFF0000)
            E.set_thumbnail(url=BACKALL)
            E.set_footer(text="The image stays nice and small, perfect for mobile.")
            await ctx.send(embed=E)
        else:
            await self.config.user(ctx.author).image.set(True)
            E = discord.Embed(title="Image responses", description="Embeds will now be sent like this.", color=0xFF0000)
            E.set_image(url=BACKALL)
            E.set_footer(text="The image is nice and large, perfect for desktop.")
            await ctx.send(embed=E)
            
