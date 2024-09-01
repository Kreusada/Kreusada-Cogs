from __future__ import annotations

import aiohttp
import discord
from redbot.core import Config, commands
from redbot.core.bot import Red

FAVOURITE_ICON = "https://cdn-icons-png.freepik.com/256/676/676624.png?semt=ais_hybrid"


class CocktailFavouriteButton(discord.ui.Button):
    def __init__(self, *, cog: Cocktail, cocktail: str, favourite: bool):
        if favourite:
            super().__init__(
                style=discord.ButtonStyle.red,
                label="Unfavourite",
            )
        else:
            super().__init__(
                style=discord.ButtonStyle.green,
                label="Favourite",
            )
        self.view: CocktailView
        self.cog = cog
        self.cocktail = cocktail
        self.favourite = favourite

    async def callback(self, interaction: discord.Interaction):
        if self.favourite:
            self.style = discord.ButtonStyle.green
            self.label = "Favourite"
            message = "Cocktail removed from favourites."
            async with self.cog.config.user(
                interaction.user
            ).favourites() as favourites:
                favourites.remove(self.cocktail)
            embed = self.view.message.embeds[0]
            embed.remove_author()
        else:
            self.style = discord.ButtonStyle.red
            self.label = "Unfavourite"
            message = f"Cocktail added to favourites."
            async with self.cog.config.user(
                interaction.user
            ).favourites() as favourites:
                favourites.append(self.cocktail)
            embed = self.view.message.embeds[0]
            embed.set_author(
                name="This cocktail is in your favourites!", icon_url=FAVOURITE_ICON
            )
        self.favourite = not self.favourite
        await interaction.response.send_message(message, ephemeral=True)
        await self.view.message.edit(view=self.view, embed=embed)

    async def on_timeout(self):
        self.disabled = True
        await self.view.message.edit(view=self.view)


class CocktailView(discord.ui.View):
    def __init__(self, *, cog: Cocktail, cocktail: str, favourite: bool):
        super().__init__()
        self.message: discord.Message
        self.add_item(
            CocktailFavouriteButton(cog=cog, cocktail=cocktail, favourite=favourite)
        )


class Cocktail(commands.Cog):
    """Get information about different cocktails and their ingredients."""

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, 719988449867989142, force_registration=True)
        self.config.register_user(favourites=[])

    __author__ = "Kreusada"
    __version__ = "1.0.1"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        return

    @commands.group(invoke_without_command=True)
    async def cocktail(self, ctx: commands.Context, *, name: str):
        """Get information about a cocktail / cocktail related commands. Supply 'random' to retrieve a random cocktail."""
        if name == "random":
            req_str = "https://www.thecocktaildb.com/api/json/v1/1/random.php"
        else:
            req_str = "https://www.thecocktaildb.com/api/json/v1/1/search.php?s=" + name
        async with aiohttp.ClientSession() as session:
            async with session.get(req_str) as request:
                req = await request.json()
        drinks = req["drinks"]
        if not drinks:
            return await ctx.send(
                f"Couldn't find a cocktail named '{name.title()}'. \N{SHRUG}\N{ZERO WIDTH JOINER}\N{MALE SIGN}\N{VARIATION SELECTOR-16} \N{TROPICAL DRINK}"
            )
        drink = drinks[0]
        embed = discord.Embed(
            title="\N{TROPICAL DRINK} " + drink["strDrink"],
            colour=await ctx.embed_colour(),
        )
        if drink["strAlcoholic"] == "Alcoholic":
            embed.description = "-# This drink contains alcohol."
        else:
            embed.description = "-# This is an alcohol-free drink."
        embed.set_image(url=drink["strDrinkThumb"])
        embed.set_footer(text="\N{FIRE} Best served in a " + drink["strGlass"])

        favourite = drink["strDrink"] in await self.config.user(ctx.author).favourites()

        if favourite:
            embed.set_author(
                name="This cocktail is in your favourites!",
                icon_url=FAVOURITE_ICON,
            )
        embed.add_field(
            name="Instructions",
            value=drink["strInstructions"],
            inline=False,
        )

        ingredients = []
        for i in range(1, 16):
            ingredient = drink[f"strIngredient{i}"]
            if ingredient is None:
                break
            measure = drink[f"strMeasure{i}"]

            if measure is None:
                string = ingredient
            else:
                string = f"{ingredient} ({measure.rstrip()})"
            ingredients.append(string)
        embed.add_field(
            name="Ingredients", value="\n".join(f"- {x}" for x in ingredients)
        )

        view = CocktailView(cog=self, cocktail=drink["strDrink"], favourite=favourite)
        view.message = await ctx.send(embed=embed, view=view)

    @cocktail.command()
    async def favourites(self, ctx: commands.Context):
        """See your favourite cocktails."""
        favourites = await self.config.user(ctx.author).favourites()
        embed = discord.Embed(
            title=f"\N{TROPICAL DRINK} {ctx.author.name}'s Favourite Cocktails",
            description="\n".join(f"- {x}" for x in sorted(favourites)),
        )
        await ctx.send(embed=embed)

    @cocktail.command()
    async def ingredient(self, ctx: commands.Context, *, name: str):
        """Get information about a cocktail ingredient."""
        req_str = "https://www.thecocktaildb.com/api/json/v1/1/search.php?i=" + name
        async with aiohttp.ClientSession() as session:
            async with session.get(req_str) as request:
                req = await request.json()
        ingredients = req["ingredients"]
        if not ingredients:
            return await ctx.send(
                f"Couldn't find an ingredients named '{name.title()}'. \N{SHRUG}\N{ZERO WIDTH JOINER}\N{MALE SIGN}\N{VARIATION SELECTOR-16} \N{TROPICAL DRINK}"
            )
        ingredient = ingredients[0]
        embed = discord.Embed(
            title=ingredient["strIngredient"],
            colour=await ctx.embed_colour(),
        )
        if desc := ingredient["strDescription"]:
            embed.description = desc.split("\n")[0]
        embed.set_image(
            url=f"https://www.thecocktaildb.com/images/ingredients/{name.replace(' ', '%20')}.png"
        )
        await ctx.send(embed=embed)
