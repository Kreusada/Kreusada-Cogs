import discord
from typing import Literal
from random import randint
from asyncio import sleep, TimeoutError
from redbot.core import bank, commands, Config
from redbot.core.i18n import Translator, cog_i18n

from .generators import embed
from .cards import BACKALL

_ = Translator("HigherOrLower", __file__)

@cog_i18n(_)
class HigherOrLower(commands.Cog):
    """
    Play the higher or lower card game!
    
    For more information, take a read [here](https://kreusadacogs.readthedocs.io/en/latest/higherorlower.html#higherorlower).
    """

    __author__ = ["Kreusada"]
    __version__ = "1.3.0"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 439583, force_registration=True)
        self.config.register_guild(
            bank=False,
            round=0,
            per=0,
            qs=9
            )
        self.config.register_user(
            draw=None,
            image=False,
            count=1
            )

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad."""
        return f"{super().format_help_for_context(ctx)}\nAuthor: {self.__author__}\nVersion: {self.__version__}"
        
    async def red_delete_data_for_user(
        self,
        requester: Literal["discord", "owner", "user", "user_strict"],
        user_id: int
    ) -> None:
        await self.config.user_from_id(user_id).clear()

    @commands.command()
    async def hol(self, ctx: commands.Context):
        """
        Play higher or lower!
        Guess if the next number will be higher or lower based on a standard pack of cards.
        For more information, please take a look [here](https://kreusadacogs.readthedocs.io/en/latest/higherorlower.html#higherorlower).
        """
        banke = await self.config.guild(ctx.guild).bank()
        currency = await bank.get_currency_name(ctx.guild)
        per = await self.config.guild(ctx.guild).per()
        round = await self.config.guild(ctx.guild).round()
        qs = await self.config.guild(ctx.guild).qs()
        await ctx.send(f"Let's get started {ctx.author.name}. Remember to answer with either `higher`, `h`, `lower` or `l`.")

        def check(x):
            return x.author == ctx.author and x.channel == ctx.channel and x.content.lower().startswith(("h", "l"))

        for i in range(int(qs)):
            draw = await self.config.user(ctx.author).draw()
            msg = f"❌ Oh no {ctx.author.name}! "
            if not draw:
                A = randint(2, 14)
            else:
                A = draw
            B = randint(2, 14)
            await sleep(1)
            E = await embed(ctx.author.name, A, await self.config.user(ctx.author).image(), await self.config.user(ctx.author).count(), qs)
            await ctx.send(embed=E)
            try:
                choice = await self.bot.wait_for("message", timeout=40, check=check)
            except TimeoutError:
                e = discord.Embed(description=msg + "You took too long to respond.", color=0xFF0000)
                await ctx.send(embed=e)
                await self.config.user(ctx.author).draw.set(None)
                await self.config.user(ctx.author).count.set(1)
                break
            if choice.content.lower().startswith(("h")) and B > A or choice.content.lower().startswith(("l")) and B < A:
                e = discord.Embed(description=f"✅ Great work! The next number is...", color=0x00FF00)
                if banke is True:
                    await bank.deposit_credits(ctx.author, per)
                    e.set_footer(text=f"+{per} has been added to your bank account.")
                await ctx.send(embed=e)
                await self.config.user(ctx.author).draw.set(B)
                count = await self.config.user(ctx.author).count()
                count += 1
                await self.config.user(ctx.author).count.set(count)
                continue
            elif choice.content.lower().startswith("h") and B == A or choice.content.lower().startswith("l") and B == A:
                e = discord.Embed(description=f"😌 The results were the same! The next number is...", color=0xFFFF00)
                if banke is True:
                    e.set_footer(text=f"+{per} has been added to your bank account.")
                    await bank.deposit_credits(ctx.author, per)
                await ctx.send(embed=e)
                await self.config.user(ctx.author).draw.set(B)
                count = await self.config.user(ctx.author).count()
                count += 1
                await self.config.user(ctx.author).count.set(count)
                continue
            else:
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
                await self.config.user(ctx.author).count.set(1)
                break
        else:
            if banke is True:
                await bank.deposit_credits(ctx.author, round)
                description = f"🎉 You MADE IT {ctx.author.name}!! Awesome work!\n{round} {currency} has been added to your bank account."
                E = discord.Embed(description=description, color=0x00FF00)
                await ctx.send(embed=E)
            else:
                E = discord.Embed(description=f"🎉 You MADE IT {ctx.author.name}!! Awesome work!", color=0x00FF00)
                await ctx.send(embed=E)
            await self.config.user(ctx.author).draw.set(None)
            await self.config.user(ctx.author).count.set(1)

    @commands.group()
    async def holset(self, ctx: commands.Context):
        """Settings for higher or lower."""

    @holset.command()
    @commands.mod_or_permissions(administrator=True)
    async def perpayout(self, ctx: commands.Context, payout: int):
        """Sets the bank payout per answer."""
        currency = await bank.get_currency_name(ctx.guild)
        if payout > 1000:
            await ctx.send(f"{payout} exceeds the maximum payout. Please go lower.")
        else:
            await self.config.guild(ctx.guild).per.set(payout)
            await ctx.send(f"Done. Users will now receive {payout} {currency} when they correctly guess a card.")

    @holset.command()
    @commands.mod_or_permissions(administrator=True)
    async def total(self, ctx: commands.Context, cards: int):
        """
        Set the total of answered cards needed to win.
        
        This value defaults to 9.
        """
        currency = await bank.get_currency_name(ctx.guild)
        if cards <= 3:
            await ctx.send(f"Setting the required cards to {int(cards)} would be too easy. Please go higher.")
        elif cards >= 20:
            await ctx.send(f"Setting the required cards to {int(cards)}... would that even be possible? Please go lower.")
        else:
            await self.config.guild(ctx.guild).qs.set(cards)
            await ctx.send(f"Users will now have to answer {int(cards)} cards correctly before winning.")
            
    @holset.command()
    @commands.mod_or_permissions(administrator=True)
    async def roundpayout(self, ctx: commands.Context, payout: int):
        """Sets the bank payout if all 9 cards are correctly guessed."""
        currency = await bank.get_currency_name(ctx.guild)
        if payout > 100000:
            await ctx.send(f"{payout} exceeds the maximum payout. Please go lower.")
        else:
            await self.config.guild(ctx.guild).round.set(payout)
            await ctx.send(f"Done. Users will now receive {payout} {currency} when they correctly guess all nine cards.")
        
    @holset.command()
    @commands.mod_or_permissions(administrator=True)
    async def togglebank(self, ctx: commands.Context, true_or_false: bool = False):
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
    async def image(self, ctx: commands.Context, true_or_false: bool):
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