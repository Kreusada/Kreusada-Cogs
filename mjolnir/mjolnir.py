import discord
import random
from redbot.core import commands, checks, Config, bank
from .mjolnirutils import lifted, failed
import logging

log = logging.getLogger("red.kreusada.mjolnir")


class Mjolnir(commands.Cog):
    """Try and lift Thor's hammer!"""
    defaults = {
        "bank": 0,
        "role": None
    }

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(
            self, 200730042020, force_registration=True)
        self.config.register_guild(**self.defaults)

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def trylift(self, ctx):
        """Try and lift Thor's hammer!"""
        settings = await self.config.guild(ctx.guild).all()
        currency = await bank.get_currency_name(ctx.guild)
        # roler = await self.config.guild(ctx.guild).role()
        bankr = await self.config.guild(ctx.guild).bank()
        trylift_chance = round(random.uniform(0, 100), 2)
        if trylift_chance < 0.03:
            # user = bot.get_user(ctx.author.id)
            embed = Embed.create(
                self, ctx, title=f"{ctx.author.name} LIFTED THE HAMMER! :hammer::zap:", description=lifted)
            await ctx.author.send(f"**{bankr} {currency} was added to your bank account in {ctx.guild.name}.")
            await bank.deposit_credits(ctx.author, settings["bank"])
            await ctx.author.add_roles(settings["role"])
            # await ctx.send(embed=embed) # No need to repeat ourselves here
        else:
            embed = Embed.create(
                self, ctx, title=f"{ctx.author.name} attempted to lift the hammer. :hammer::zap:", description=random.choice(failed))
        # Embed is *always* defined so just have one sending
        await ctx.send(embed=embed)

    @commands.group()
    @checks.mod()
    async def liftset(self, ctx):
        """Mjolnir configuration."""

    @liftset.command()
    async def bank(self, ctx, amount: int):
        """Decides whether users win currency from lifting mjolnir. Defaults to 0."""
        currency = await bank.get_currency_name(ctx.guild)
        if amount <= 0:
            return await ctx.send(f"Those who lift Thor's hammer will not be given any {currency}.")
        await self.config.guild(ctx.guild).bank.set(amount)
        await ctx.send(f"Those who lift Thor's hammer will now be given **{amount} {currency}**.")

    @liftset.command()
    async def role(self, ctx, role: discord.Role):
        """Decides whether users win currency from lifting mjolnir."""
        try:
            await self.config.guild(ctx.guild).set_raw("role", value=role.id)
            await ctx.send(f"{role.mention} will now be granted for those who lift Thor's hammer. :hammer:.")
        except discord.Forbidden:
            await ctx.send("Hmm, I couldn't do that. Perhaps check my permissions?")


class Embed:
    def __init__(self, bot):
        self.bot = bot

    def create(self, ctx, color=discord.Color.red(), title='', description='', image=None,
               thumbnail=None, url=None, footer_text=None, footer_url=None, author_text=None):
        if isinstance(ctx.message.channel, discord.abc.GuildChannel):
            color = ctx.message.author.color
        data = discord.Embed(color=color, title=title, url=url)
        if description is not None:
            if len(description) < 1500:
                data.description = description
        data.set_author(name=ctx.message.author.display_name,
                        icon_url=ctx.message.author.avatar_url)
        if image is not None:
            # validators.url(image)
            # code = requests.get(image).status_code
            # if code == 200:
            data.set_image(url=image)
            # else:
            # print('Image URL Failure, code {}'.format(code))
            # print('Attempted URL:\n{}'.format(image))
        return data
