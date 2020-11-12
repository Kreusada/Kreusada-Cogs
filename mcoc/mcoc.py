from redbot.core import commands, checks, Config
from redbot.core.utils import menus
import asyncio
import discord
import random
import logging
from .mdtembed import Embed
from .crystal import FEATUREDS, BCB

log = logging.getLogger(name="red.demaratus.mcoc")


class Mcoc(commands.Cog):
    """Fun Games and Tools for Marvel Contest of Champions."""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=153607829, force_registration=True
        )
        self.config.register_user(
            roster={
                "5": {},
                "4": {},
                "3": {}
            }
        )

    @commands.command()
    async def supportserver(self, ctx):
        """Support Server invite link."""
        await ctx.send("https://discord.gg/JmCFyq7")

    @commands.command()
    # @commands.cooldown(1, 30, commands.BucketType.user)
    async def crystal(self, ctx):
        """Chooses a random champion from MCOC."""
        star = random.choice(['3', '4', '5'])
        key, image = (random.choice(list(FEATUREDS.items())))
        roster = await self.config.user(ctx.author).roster.get_raw()
        await self.roster_logistics(ctx, star, key, roster)
        data = Embed.create(
            self, ctx, title='You got... :gem:',
            description="⭐" * int(star)
        )
        data.set_image(url=image)
        await ctx.send(embed=data)

    @commands.command()
    async def roster(self, ctx, star: str = None):
        if star is None:
            star = "5"
        try:
            roster: dict = await self.config.user(ctx.author).roster.get_raw(star)
        except KeyError:
            roster: dict = await self.config.user(ctx.author).roster.get_raw("5")
        if len(roster.values()) > 0:
            roster = "\n".join(
                ["{} s{}".format(key, value) for key, value in roster.items()]
            )
            embed = discord.Embed(
                title="Crystal roster", color=ctx.author.color
            )
            embed.add_field(name="{}'s Roster".format(
                ctx.author), value=roster)
        else:
            embed = discord.Embed(
                title="Crystal roster", color=ctx.author.color, description=(
                    "You don't have any {} star champions!\n"
                    "Collect some using `{}crystal`!".format(
                        star, ctx.clean_prefix
                    )
                )
            )
        await ctx.send(embed=embed)

    @commands.group()
    async def battlechip(self, ctx):
        """Opens a battlechip crystal from MCOC."""

    @battlechip.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def basic(self, ctx):
        """Open a basic battlechip crystal."""
        drop_rate = round(random.uniform(0, 100), 2)
        if drop_rate < 0.02:
            link = BCB[0]
            title = "4 Star Punisher"
            description = (
                "This tier has a `0.02%` chance.\nCongratulations!\n"
                "Message Kreusada#0518 with a screenshot to be added to the hall of fame!"
            )
        elif drop_rate < 0.65:
            link = BCB[0]
            title = "3 Star Punisher"
            description = "This tier has a `0.65%` chance.\nCongratulations!"
        elif drop_rate < 0.35:
            link = BCB[1]
            title = "Energy Refill"
            description = "This tier has a `0.35%` chance.\nCongratulations!"
        elif drop_rate < 2:
            link = BCB[2]
            title = "45 Units"
            description = ""
        elif drop_rate < 6:
            link = BCB[2]
            title = "15 Units"
            description = ""
        elif drop_rate < 30:
            link = BCB[3]
            title = "10,000 Gold"
            description = ""
        else:
            link = BCB[3]
            title = "2,500 Gold"
            description = ""
        data = Embed.create(self, ctx, description=description, image=link)
        await ctx.send(embed=data)

    @battlechip.command()
    async def uncollected(self, ctx):
        """Open an uncollected battlechip crystal."""
        drop_rate = round(random.uniform(0, 100), 2)
        if drop_rate < 0.02:
            link = BCB[0]
            title = "5 Star Punisher"
            description = (
                "This tier has a `0.02%` chance.\nCongratulations!\n"
                "Message Kreusada#0518 with a screenshot to be added to the hall of fame!"
            )
        elif drop_rate < 0.65:
            link = BCB[0]
            title = "4 Star Punisher"
            description = "This tier has a `0.65%` chance.\nCongratulations!"
        elif drop_rate < 0.35:
            link = BCB[1]
            title = "Five Energy Refills"
            description = "This tier has a `0.35%` chance.\nCongratulations!"
        elif drop_rate < 2:
            link = BCB[2]
            title = "225 Units"
            description = ""
        elif drop_rate < 6:
            link = BCB[2]
            title = "75 Units"
            description = ""
        elif drop_rate < 30:
            link = BCB[3]
            title = "50,000 Gold"
            description = ""
        elif drop_rate < 45:
            link = BCB[3]
            title = "25,000 Gold"
            description = ""
        else:
            link = BCB[3]
            title = "10,000 Gold"
            description = ""
        data = Embed.create(
            self, ctx,
            title="You got {}!".format(title), description="{}".format(description),
            image=link
        )
        await ctx.send(embed=data)

    async def roster_logistics(self, ctx: commands.Context, star: str, champion: str, roster: dict) -> None:
        intstar = int(star)
        if intstar <= 0 or intstar > 6:
            intstar = 6
            star = "6"
        if intstar == 1 or intstar == 2:
            sigs = 1
        elif intstar == 3:
            sigs = 8
        else:
            sigs = 20
        try:
            roster[star][champion] += sigs
        except KeyError:
            roster[star][champion] = 0
        await self.config.user(ctx.author).roster.set_raw(value=roster)

    # @commands.group()
    # async def awbadge(self, ctx):
    #     """The Alliance War badge index."""

    # @awbadge.group()
    # async def master(self, ctx):
    #     """Master Alliance War Badges."""

    # @awbadge.group()
    # async def platinum(self, ctx):
    #     """Platinum Alliance War Badges."""

    # @awbadge.group()
    # async def gold(self, ctx):
    #     """Gold Alliance War Badges."""

    # @awbadge.group()
    # async def silver(self, ctx):
    #     """Silver Alliance War Badges."""

    # @awbadge.group()
    # async def bronze(self, ctx):
    #     """Bronze Alliance War Badges."""

    # @awbadge.group()
    # async def stone(self, ctx):
    #     """Stone Alliance War Badges."""

    # @awbadge.group()
    # async def participation(self, ctx):
    #     """Participation Alliance War Badges."""

    # @master.group(name="1", invoke_without_command=True)
    # async def one(self, ctx):
    #     """Master Rank 1 Badge."""
    #     data = Embed.create(self, ctx, title='Master Rank One Badge :trophy:')
    #     image = (f"https://media.discordapp.net/attachments/401476363707744257/738083791654092940/47EFB6D4D1380ABD2C40D2C7B0533A29245F7955.png")
    #     data.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    #     data.set_image(url=image)
    #     await ctx.send(embed=data)

    # @master.group(name="2", invoke_without_command=True)
    # async def two(self, ctx):
    #     """Master Rank 2 Badge."""
    #     data = Embed.create(self, ctx, title='Master Rank Two Badge :trophy:')
    #     image = (f"https://media.discordapp.net/attachments/401476363707744257/738083791113027654/650E29ADB8C5C382FF5A358113B2C02B8EADA415.png")
    #     data.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    #     data.set_image(url=image)
    #     await ctx.send(embed=data)

    # @master.group(name="3", invoke_without_command=True)
    # async def three(self, ctx):
    #     """Master Rank 3 Badge."""
    #     data = Embed.create(
    #         self, ctx, title='Master Rank Three Badge :trophy:')
    #     image = (f"https://media.discordapp.net/attachments/401476363707744257/738083791440052294/08BA0A081A9D56E35E60E3FD61FAB7ED9A10CD00.png")
    #     data.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    #     data.set_image(url=image)
    #     await ctx.send(embed=data)

    # @master.group(name="20", invoke_without_command=True)
    # async def four(self, ctx):
    #     """Master Top 20 Badge."""
    #     data = Embed.create(self, ctx, title='Master Badge :trophy:')
    #     image = (f"https://media.discordapp.net/attachments/401476363707744257/738083791301509191/28A5CCCA9CA8294C76D8BE94CC0ADD2734B26570.png")
    #     data.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    #     data.set_image(url=image)
    #     await ctx.send(embed=data)

    # @platinum.group(name="1", invoke_without_command=True)
    # async def five(self, ctx):
    #     """Platinum 1 Badge."""
    #     data = Embed.create(self, ctx, title='Platinum One Badge :trophy:')
    #     image = (f"https://media.discordapp.net/attachments/401476363707744257/738083790718631937/E78E2BAF9B0C9BA6C7FE45BE726FFB0B0B0CACFD.png")
    #     data.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    #     data.set_image(url=image)
    #     await ctx.send(embed=data)

    # @platinum.group(name="2", invoke_without_command=True)
    # async def six(self, ctx):
    #     """Platinum 2 Badge."""
    #     data = Embed.create(self, ctx, title='Platinum Two Badge :trophy:')
    #     image = (f"https://media.discordapp.net/attachments/401476363707744257/738083790362116116/487EA26A1BA0F2C2848E7C87F10430BD218C2178.png")
    #     data.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    #     data.set_image(url=image)
    #     await ctx.send(embed=data)

    # @platinum.group(name="3", invoke_without_command=True)
    # async def seven(self, ctx):
    #     """Platinum 3 Badge."""
    #     data = Embed.create(self, ctx, title='Platinum Three Badge :trophy:')
    #     image = (f"https://media.discordapp.net/attachments/401476363707744257/738083790559117352/0ED8BD10441C6D086AEB7BBA5271269F46E009D1.png")
    #     data.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    #     data.set_image(url=image)
    #     await ctx.send(embed=data)

    # @platinum.group(name="4", invoke_without_command=True)
    # async def eight(self, ctx):
    #     """Platinum 4 Badge."""
    #     data = Embed.create(self, ctx, title='Platinum Four Badge :trophy:')
    #     image = (f"https://media.discordapp.net/attachments/401476363707744257/738083789934166046/71703F9C740FFDC3223A570CC1C252D8392534BC.png")
    #     data.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    #     data.set_image(url=image)
    #     await ctx.send(embed=data)

    # @gold.group(name="1", invoke_without_command=True)
    # async def nine(self, ctx):
    #     """Gold 1 Badge."""
    #     data = Embed.create(self, ctx, title='Gold One Badge :trophy:')
    #     image = (f"https://media.discordapp.net/attachments/401476363707744257/738083790131298375/76BC21BF523A415866D19814BD8AF4BE16EF30A9.png")
    #     data.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    #     data.set_image(url=image)
    #     await ctx.send(embed=data)

    # @gold.group(name="2", invoke_without_command=True)
    # async def ten(self, ctx):
    #     """Gold 2 Badge."""
    #     data = Embed.create(self, ctx, title='Gold Two Badge :trophy:')
    #     image = (f"https://media.discordapp.net/attachments/401476363707744257/738083998462509096/8CD52FEB7540016B6ABA1EC67B9F1777E3C29878.png")
    #     data.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    #     data.set_image(url=image)
    #     await ctx.send(embed=data)

    # @gold.group(name="3", invoke_without_command=True)
    # async def eleven(self, ctx):
    #     """Gold 3 Badge."""
    #     data = Embed.create(self, ctx, title='Gold Three Badge:trophy:')
    #     image = (f"https://media.discordapp.net/attachments/401476363707744257/738084001926873098/3A9A8FDA006D0BE225242AAA5909021CD52BCFB3.png")
    #     data.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    #     data.set_image(url=image)
    #     await ctx.send(embed=data)

    # @silver.group(name="1", invoke_without_command=True)
    # async def twelve(self, ctx):
    #     """Silver 1 Badge."""
    #     data = Embed.create(self, ctx, title='Silver One Badge :trophy:')
    #     image = (f"https://media.discordapp.net/attachments/401476363707744257/738084001465499789/4B389D377A94EDA747B38DF640C0B33A3A3F61AE.png")
    #     data.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    #     data.set_image(url=image)
    #     await ctx.send(embed=data)

    # @silver.group(name="2", invoke_without_command=True)
    # async def thirteen(self, ctx):
    #     """Silver 2 Badge."""
    #     data = Embed.create(self, ctx, title='Silver Two Badge :trophy:')
    #     image = (f"https://media.discordapp.net/attachments/401476363707744257/738084001465499789/4B389D377A94EDA747B38DF640C0B33A3A3F61AE.png")
    #     data.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    #     data.set_image(url=image)
    #     await ctx.send(embed=data)

    # @silver.group(name="3", invoke_without_command=True)
    # async def fourteen(self, ctx):
    #     """Silver 3 Badge."""
    #     data = Embed.create(self, ctx, title='Silver Three Badge :trophy:')
    #     image = (f"https://media.discordapp.net/attachments/401476363707744257/738083994612006914/5302FA8FA04735224847C8BBF82D1D54C8567B9C.png")
    #     data.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    #     data.set_image(url=image)
    #     await ctx.send(embed=data)

    # @bronze.group(name="1", invoke_without_command=True)
    # async def fifteen(self, ctx):
    #     """Bronze 1 Badge."""
    #     data = Embed.create(self, ctx, title='Bronze One Badge :trophy:')
    #     image = (f"https://media.discordapp.net/attachments/401476363707744257/738083995211792404/719AC2C2AB5833D815C899DAF9ADB7CF11819CBA.png")
    #     data.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    #     data.set_image(url=image)
    #     await ctx.send(embed=data)

    # @bronze.group(name="2", invoke_without_command=True)
    # async def sixteen(self, ctx):
    #     """Bronze 2 Badge."""
    #     data = Embed.create(self, ctx, title='Bronze Two Badge :trophy:')
    #     image = (f"https://media.discordapp.net/attachments/401476363707744257/738083993043337276/E636A90C3F0DFFDAED0176D972AA0C73F3E40FF8.png")
    #     data.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    #     data.set_image(url=image)
    #     await ctx.send(embed=data)

    # @bronze.group(name="3", invoke_without_command=True)
    # async def seventeen(self, ctx):
    #     """Bronze 3 Badge."""
    #     data = Embed.create(self, ctx, title='Bronze Three Badge :trophy:')
    #     image = (f"https://media.discordapp.net/attachments/401476363707744257/738083997866786876/5B06D509847E0FA1405A50021486C1A5D8C6F9B2.png")
    #     data.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    #     data.set_image(url=image)
    #     await ctx.send(embed=data)

    # @stone.group(name="1", invoke_without_command=True)
    # async def eighteen(self, ctx):
    #     """Stone 1 Badge."""
    #     data = Embed.create(self, ctx, title='Stone One Badge :trophy:')
    #     image = (f"https://media.discordapp.net/attachments/401476363707744257/738083996054978730/9AC92A2FDC2996C346125296356C664373147F2F.png")
    #     data.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    #     data.set_image(url=image)
    #     await ctx.send(embed=data)

    # @stone.group(name="2", invoke_without_command=True)
    # async def nineteen(self, ctx):
    #     """Stone 2 Badge."""
    #     data = Embed.create(self, ctx, title='Stone Two Badge :trophy:')
    #     image = (f"https://media.discordapp.net/attachments/401476363707744257/738083993681002586/BF3D13EACC9F44216E754884AA183185761C84CF.png")
    #     data.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    #     data.set_image(url=image)
    #     await ctx.send(embed=data)

    # @stone.group(name="3", invoke_without_command=True)
    # async def twenty(self, ctx):
    #     """Stone 3 Badge."""
    #     data = Embed.create(self, ctx, title='Stone Three Badge :trophy:')
    #     image = (f"https://media.discordapp.net/attachments/401476363707744257/738084098857238670/EA938C0B0C2AE3E6DB91514F5F8768C4F033D373.png")
    #     data.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    #     data.set_image(url=image)
    #     await ctx.send(embed=data)

    # @participation.group(name="1", invoke_without_command=True, pass_context=True)
    # async def twentyone(self, ctx):
    #     """Participation Badge."""
    #     data = Embed.create(self, ctx, title='Participation Badge :trophy:')
    #     image = (f"https://media.discordapp.net/attachments/401476363707744257/738083790886535228/DA7D39277836A9CF1B39A68D37EAF99999B366C7.png")
    #     data.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    #     data.set_image(url=image)
    #     await ctx.send(embed=data)
