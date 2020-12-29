import discord
import asyncio
from redbot.core import commands, Config

BAG = "\N{SHOPPING BAGS}\N{VARIATION SELECTOR-16}"
CART = "\N{SHOPPING TROLLEY}"


class ShoppingCart(commands.Cog):
    """Add items to your shopping list."""
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 1234567890, force_registration=True)
        self.config.register_user(items={})
    
    @commands.group()
    async def shopping(self, ctx):
        """Manage your shopping cart."""
        
    @shopping.command(name="list", aliases=["cart"])
    async def _list(self, ctx):
        """View your current shopping list."""
        items = await self.config.user(ctx.author).items()
        title=f"{CART} {ctx.author.name.capitalize()}'s Shopping List"
        color=0xe1ac59
        if len(items) >= 1:
            description=", ".join(items)
        else:
            description = f"You don't have any items in your shopping cart. {CART}"
        embed = discord.Embed(title=title, description=description, color=color)
        await ctx.send(embed=embed)
        
    @shopping.command()
    async def add(self, ctx, item: str):
        """Add an item to your shopping list."""
        items = await self.config.user(ctx.author).items()
        items[item.capitalize()] = {'items': item}
        await self.config.user(ctx.author).items.set(items)
        embed = discord.Embed(title=f"You added {item} to your shopping list.", color=0xe1ac59)
        await ctx.send(embed=embed)
        
    @shopping.command(name="del")
    async def de(self, ctx, item: str):
        """Deletes items off your shopping list."""
        await self.config.user(ctx.author).items.clear_raw(item)
        try:
            await ctx.send(f"{item} was cleared off your shopping list.")
        except KeyError:
            await ctx.send(f"{item} is not on your shopping list!")
        
    @shopping.command()
    async def checkout(self, ctx):
        """Clears your entire shopping list."""
        await self.config.user(ctx.author).items.clear_raw()
        await ctx.send(f"Done. Your shopping list has been successfully cleared! Thanks for using us to shop today! {BAG}")