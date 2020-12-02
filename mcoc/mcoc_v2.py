import discord
from redbot.core import (commands, Config,)
import random
from typing import (Optional, Union, Tuple)
from .constants import (BCB, FEATUREDS,)


class Mcoc(commands.Cog):
    # I need some instace variables
    CRYSTAL_TYPES = {
        "grandmaster": (3, 4, 5),
        # I hope I didn't get this confused with legendary LOL
        "ultimate": (3, 4)
    }

    def __init__(self, bot):
        self.bot = bot
        self.embed = Embed(self.bot)
        self.config = Config.get_conf(
            self, 126573038446, force_registration=True)
        self.config.register_user(
            roster={
                "6": [],
                "5": [],
                "4": [],
                "3": []
            }
        )

    @commands.group(invoke_without_command=True)
    async def crystal(self, ctx: commands.Context):
        """Base Crystal command. If no subcommands are provided it will default to a Ultimate crystal"""
        embed = await self.crystal_logic(ctx.author, "ultimate")
        await ctx.send(embed=embed)

    async def crystal_logic(self, user: discord.Member, crystal_type: Optional[str] = "ultimate") -> discord.Embed:
        """[summary]

        Args:
            :user: discord.Member: [description]
            :crystal_type: Optional[str]: [description]. Defaults to "ultimate".

        Returns:
            discord.Embed: The embed that tells what the user got
        """
        if crystal_type not in ("ultimate", "grandmaster", "battlechip"):
            return None
        if crystal_type != "battlechip":
            prize = random.choice(self.CRYSTAL_TYPES[crystal_type])
            champion = random.choice(list(FEATUREDS.keys()))
            await self.config.user(user).set_raw("roster", str(prize), value=champion)
            title = "You got... <:crystal:776941489464672266>"
            description = "⭐" * prize
            image = FEATUREDS[champion][0]
        else:
            image, title = self.battlechip_logic()
            description = None

        return self.embed.create(user=user, title=title, description=description, image=image)

    def battlechip_logic(self) -> Tuple[str, str]:
        droprate = round(random.uniform(1, 100), 2)
        # I'm going to do something that I don't know if it'll work
        if droprate < 0.65:
            image = BCB[0]
            title = "{} Star Punisher".format(
                "4" if droprate < 0.2 else "3"
            )
        elif droprate < 0.35:
            image = BCB[1]
            title = "Energy Refill"
        elif droprate < 6:
            image = BCB[2]
            title = "{} Units".format(
                "45" if droprate < 2 else "15"
            )
        elif droprate < 30:
            image = BCB[3]
            title = "10,000 Gold"
        else:
            image = BCB[3]
            title = "{} Gold".format(
                "5,000" if droprate < 50 else "3,000"
            )
        return image, title


class Embed:
    def __init__(self, bot):
        self.bot = bot

    def create(
        self, ctx: commands.Context = None, user: discord.Member = None, title: str = None,
        description: str = None, color: discord.Colour = discord.Colour.gold(), image: str = None
    ):
        DEMARATUS = 'https://cdn.discordapp.com/attachments/758775890954944572/768452440785027132/demaratuscircle.png'
        # if isinstance(ctx.message.channel, discord.abc.GuildChannel):
        #     color = ctx.message.author.color
        data = discord.Embed(color=color, title=title)
        if description is not None:
            if len(description) < 1500:
                data.description = description

        if ctx:
            author = ctx.author.name
            author_url = ctx.author.avatar_url
        elif user:
            author = user.name
            author_url = user.avatar_url
        else:
            author = self.bot.user.name
            author_url = self.bot.user.avatar_url
        data.set_author(name=author, icon_url=author_url)
        if image is not None:
            data.set_image(url=image)
        data.set_footer(text="Demaratus | MCOC Commands", icon_url=DEMARATUS)
        return data
