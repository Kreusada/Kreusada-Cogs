import discord
import random
from redbot.core import commands, bank, Config

from redbot.core import commands
from redbot.core.i18n import Translator, cog_i18n

_ = Translator("RobTheBank", __file__)

def yes_no_returner(fail: bool, ctx: commands.Context) -> str:
    """A bool-returner which will choose a random response."""
    yes = [
        "Dispatch, we've lost the suspect.\n",
        f"Looks like {ctx.author.name} made it out alive, somehow...\n",
        "We let you loose on purpose, we really did.\n"
    ]
    no = [
        "Oh I caught you red handed there!\n",
        "Get some good detective skills before trying to rob my bank!\n",
        f"Oh, it's you again... {ctx.author.name} is it?\n",
        "Ladies and gentlemen, we gottem.\n"
    ]
    return random.choice(yes) if fail else random.choice(no)

@cog_i18n(_)
class RobTheBank(commands.Cog):
    """Rob the bank. Gain or get fired"""

    def __init__(self, bot):
        default_guild = {
            "Fine": 400,
            "Deposit": 400
        }
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=5865146514315491, force_registration=True
        )
        self.config.register_guild(
            **default_guild
        )

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def rob(self, ctx: commands.Context):
        """Attempt to rob the bank... **Attempt**"""
        currency = await bank.get_currency_name(ctx.guild)
        settings = await self.config.guild(ctx.guild).all()
        if random.randint(1, 6) > 4:
            fine = await self.config.guild(ctx.guild).get_raw("Fine")
            description = yes_no_returner(
                False, ctx) + "You have been fined {} {}!".format(fine, currency)
            title = f"{ctx.author.name} failed, dismally."
            try:
                await bank.withdraw_credits(ctx.author, fine)
            except ValueError:
                await bank.set_balance(ctx.author, 0)
                return await ctx.send(f"Oh no! You were fined more cash than you have! Get some more using `{ctx.clean_prefix}payday`!")
        else:
            deposit = await self.config.guild(ctx.guild).get_raw("Deposit")
            description = yes_no_returner(True, ctx) + \
                "You have earnt yourself {} {}!".format(deposit, currency)
            title = f"{ctx.author.name} successfully robbed the bank."
            await bank.deposit_credits(ctx.author, deposit)
        embed = discord.Embed(title=title, description=description, color=0x85bb65)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.group(name="robset")
    @commands.mod()
    async def rob_set(self, ctx: commands.Context):
        """Configurations for robbing the bank"""

    @rob_set.command()
    async def deposit(self, ctx: commands.Context, amount: int):
        """Set the amount a user can steal"""
        if amount < 1:
            await ctx.send("Stealing from a bank, but receiving no profit? That's not stealing my friend! Please enter a valid integer.")
        cur = await bank.get_currency_name(ctx.guild)

        await self.config.guild(ctx.guild).set_raw("Deposit", value=amount)
        await ctx.send("Deposits will now give out **{} {}**.".format(
            amount, cur
        ))

    @rob_set.command()
    async def fine(self, ctx: commands.Context, amount: int):
        """Set the fine amount"""
        if amount < 1:
            await ctx.send("You might as well not be fined!")
        cur = await bank.get_currency_name(ctx.guild)

        await self.config.guild(ctx.guild).set_raw("Fine", value=amount)
        await ctx.send("Fines will now withdraw **{} {}**.".format(amount, cur))

    @rob_set.command()
    async def showsettings(self, ctx: commands.Context):
        """Show the current settings for Rob the bank"""
        fine = await self.config.guild(ctx.guild).get_raw("Fine")
        deposit = await self.config.guild(ctx.guild).get_raw("Deposit")
        if fine == 400 and deposit == 400:
            s = "Standard"
        else:
            s = "Custom"
        embed = discord.Embed(
            title="{}'s Settings".format(ctx.guild.name),
            description=(
                f"Fine Expense: **{fine}**\n"
                f"Deposit to Receive: **{deposit}**\n"
                f"Setting Configuration: **{s}**"
            ),
            color=0x85bb65
        )
        await ctx.send(embed=embed)
