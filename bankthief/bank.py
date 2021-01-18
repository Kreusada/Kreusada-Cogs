import discord
import asyncio
from random import randint
from redbot.core import commands, bank, Config
from redbot.core import commands
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.predicates import ReactionPredicate
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.chat_formatting import box

_ = Translator("BankThief", __file__)

NOT_ACTIVE = (
    "BankThief has currently been disabled by an admin, therefore this command is not available.\n"
    "You can check up on the status by using `[p]robset settings`."
)

LOSE = (
    "- [p]rob\n"
    "- [p]robstore crook"
)

STATS_CHECK = f"You can check your stats by using `[p]robstats`."


@cog_i18n(_)
class BankThief(commands.Cog):
    """Rob other users."""
    
    __author__ = ["Kreusada"]
    __version__ = "2.0.0"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=5865146514315491, force_registration=True)
        self.config.register_guild(
            minimum=100, maximum=500, crookcost=300, disable=False
        )
        self.config.register_user(
            crooks=0, success=0,
            notsuccess=0, almost=0
        )

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    @commands.group()
    @commands.guild_only()
    async def robstore(self, ctx):
        """Store for bank property."""

    @commands.group()
    @commands.guild_only()
    async def robset(self, ctx):
        """Settings for BankThief."""

    @robset.command()
    @commands.admin_or_permissions(administrator=True)
    async def disable(self, ctx, true_or_false: bool):
        """Disable or enable BankThief."""
        if true_or_false is False:
            await ctx.send("BankThief is now active.")
        else:
            pred = await self.active(ctx)

    async def active(self, ctx):
        msg = await ctx.send(
            f"Are you sure you would like to disable BankThief for {ctx.guild.name}?\n"
            f"Users will lost access to the following commands: {box(LOSE.replace('[p]', ctx.clean_prefix), lang='diff')}"
            )
        pred = ReactionPredicate.yes_or_no(msg, ctx.author)
        start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)
        try:
            await self.bot.wait_for("reaction_add", check=pred, timeout=30)
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send(f":x: You took too long to respond.")
        if not pred.result:
            await ctx.send("Okay. No changes have been made.")
        else:
            await msg.delete()
            await self.config.guild(ctx.guild).disable.set(True)
            await ctx.send(f"BankThief is disabled. You can re-enable it by using `{ctx.clean_prefix}robset disable false`.")

    @robset.command()
    @commands.cooldown(1, 100, commands.BucketType.user)
    @commands.admin_or_permissions(administrator=True)
    async def crookcost(self, ctx, price: int):
        """Set the price for crooks."""
        await self.config.guild(ctx.guild).crookcost.set(price)
        await ctx.send(f"The cost to purchase a crook has been set to {price}.")

    @robset.command(name="max")
    @commands.admin_or_permissions(administrator=True)
    async def _max(self, ctx, price: int):
        """Set the maximum rob amount possible."""
        await self.config.guild(ctx.guild).maximum.set(price)
        await ctx.send(f"The maximum rob amount has been set to {price}.")

    @robset.command(name="min")
    @commands.admin_or_permissions(administrator=True)
    async def _min(self, ctx, price: int):
        """Set the maximum rob amount possible."""
        await self.config.guild(ctx.guild).minimum.set(price)
        await ctx.send(f"The minimum rob amount has been set to {price}.")

    @robset.command()
    async def settings(self, ctx):
        """Shows the guild's current settings."""
        min = await self.config.guild(ctx.guild).minimum()
        max = await self.config.guild(ctx.guild).maximum()
        crook = await self.config.guild(ctx.guild).crookcost()
        disabled = await self.config.guild(ctx.guild).disable()
        text = (
            f"Cost to purchase a crook: {crook}\n"
            f"Maximum rob amount: {max}\n"
            f"Minimum rob amount: {min}\n"
            f"Disabled: {disabled}"
        )
        await ctx.send(f"{box(text=f'[Settings for {ctx.guild.name}]', lang='ini')}{box(text, lang='yaml')}")

    @robstore.command()
    async def crook(self, ctx):
        """Purchase a crook to rob someone's bank account."""
        if await self.config.guild(ctx.guild).disable() is False:
            crookcost = await self.config.guild(ctx.guild).crookcost()
            pred = await self.confirm(ctx, 'crook', crookcost)
        else:
            await ctx.send(NOT_ACTIVE.replace('[p]', ctx.clean_prefix))

    async def confirm(self, ctx, type: str, cost: int):
        msg = await ctx.send(f"Please confirm that you would like to purchase a {type} for {cost}.")
        pred = ReactionPredicate.yes_or_no(msg, ctx.author)
        start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)
        try:
            await self.bot.wait_for("reaction_add", check=pred, timeout=30)
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send(f":x: You took too long to respond.")
        if not pred.result:
            await ctx.send("Okay. No changes have been made.")
        else:
            try:
                await msg.delete()
                await bank.withdraw_credits(ctx.author, cost)
                crooks = await self.config.user(ctx.author).crooks()
                crooks += 1; await self.config.user(ctx.author).crooks.set(crooks)
                await ctx.send(f"Done. A {type} was successfully purchased for {cost}.")
            except ValueError:
                await ctx.send(f"You do not have enough cash! A crook costs {cost}, you have {await bank.get_balance(ctx.author)}.")

    @commands.command()
    @commands.guild_only()
    async def rob(self, ctx, member: discord.Member):
        """Rob someone's bank account."""
        if await self.config.guild(ctx.guild).disable() is False:
            crook = await self.config.user(ctx.author).crooks()
            success = await self.config.user(ctx.author).success()
            no = await self.config.user(ctx.author).notsuccess()
            almost = await self.config.user(ctx.author).almost()
            if crook == 0:
                return await ctx.send(f"You do not have a crook to rob {member.name}. Perhaps buy one using `{ctx.clean_prefix}robstore crook`.")
            rob = randint(await self.config.guild(ctx.guild).minimum(), await self.config.guild(ctx.guild).maximum())
            chance = randint(1, 10)
            if rob > await bank.get_balance(member):
                await ctx.send(f"Sorry, {member.name} is broke enough as it is.")
            else:
                if chance <= 3:
                    crook -= 1; await self.config.user(ctx.author).crooks.set(crook)
                    success += 1; await self.config.user(ctx.author).success.set(success)
                    await ctx.send(
                        f"{ctx.author.name} **exceeds** in robbing {member.name}'s bank account.\n"
                        f"**+{int(rob)}** has been added to your bank account.\n"
                        f"One crook has been removed from your account. You now have **{crook}** crooks.\n{STATS_CHECK.replace('[p]', ctx.clean_prefix)}"
                        )
                    await bank.deposit_credits(ctx.author, int(rob))
                    await bank.withdraw_credits(member, int(rob))
                elif chance >= 7:
                    crook -= 1; await self.config.user(ctx.author).crooks.set(crook)
                    no += 1; await self.config.user(ctx.author).notsuccess.set(no)
                    await ctx.send(
                        f"{ctx.author.name} **fails** in robbing {member.name}'s bank account.\n"
                        f"One crook has been removed from your account. You now have **{crook}** crooks.\n{STATS_CHECK.replace('[p]', ctx.clean_prefix)}"
                    )
                else:
                    crook -= 1; await self.config.user(ctx.author).crooks.set(crook)
                    almost += 1; await self.config.user(ctx.author).almost.set(almost)
                    await ctx.send(
                        f"{ctx.author.name} **almost exceeds** in robbing {member.name}'s bank account.\n"
                        f"**+{round(int(rob)/2)}** has been added to your bank account. That is half of what you were expecting.\n"
                        f"One crook has been removed from your account. You now have **{crook}** crooks.\n{STATS_CHECK.replace('[p]', ctx.clean_prefix)}"
                    )
                    await bank.deposit_credits(ctx.author, round(int(rob)/2))
                    await bank.withdraw_credits(member, round(int(rob)/2))
        else:
            await ctx.send(NOT_ACTIVE.replace('[p]', ctx.clean_prefix))

    @commands.command()
    @commands.guild_only()
    async def robstats(self, ctx, member: discord.Member = None):
        """Find the robbing stats for you or a member."""
        if member is None:
            person = ctx.author
        else:
            person = member
        c = await self.config.user(person).crooks()
        s = await self.config.user(person).success()
        n = await self.config.user(person).notsuccess()
        a = await self.config.user(person).almost()
        if c == 0:
            c = "None"
        else:
            c = c
        if s == 0:
            s = "None"
        else:
            s = s
        if n == 0:
            n = "None"
        else:
            n = n
        if a == 0:
            a = "None"
        else:
            a = a
        text = (
            f"Number of crooks: {c}\n"
            f"Successful robberies: {s}\n"
            f"Unsuccessful robberies: {n}\n"
            f"Close robberies: {a}\n"
        )
        await ctx.send(f"{box(text=f'[Stats for {person.name} in {ctx.guild.name}]', lang='ini')}{box(text, lang='yaml')}")



