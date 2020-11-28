from redbot.core import commands, checks, Config
from redbot.core.utils import menus
import asyncio
import discord
import random
import logging
from .mcocresources import Embed
from .crystal import FEATUREDS, BCB

log = logging.getLogger(name="red.demaratus.mcoc")


class Mcoc(commands.Cog):
    """Fun Games and Tools for Marvel Contest of Champions."""

    __version__ = "1.3.1"

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
        
    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    @commands.group()
    async def mcocsupport(self, ctx):
        """Cog support and information."""

    @mcocsupport.command()
    async def version(self, ctx):
        """Version of the mcoc cog"""
        embed = Embed.create(
            self, ctx, title="Cog Version",
            description="Current version: `{}`".format(self.__version__),
        )
        await ctx.send(embed=embed)

    @commands.group()
    async def crystal(self, ctx):
        """Chooses a random champion."""
        
    @crystal.command()
    async def alias(self, ctx):
        """Shows the full list for crystal aliases."""
        await ctx.send(
            "```rst\n"
            f"+ grandmaster (gm)[{ctx.clean_prefix}crystal gm\n"
            f"+ ultimate (u)[{ctx.clean_prefix}crystal u]\n\n"
            "- Aliases are used to shorten the command, to make it easier for you! :D```"
        )
        
    @crystal.command(aliases=["gm"])
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def grandmaster(self, ctx):
        """Open a Grandmaster crystal."""
        starr = round(random.uniform(0, 100), 2)
        if starr < 2.4:
            star = "5"
        elif starr < 12:
            star = "4"
        else:
            star = "3"
        key, image = (random.choice(list(FEATUREDS.items())))
        roster = await self.config.user(ctx.author).roster.get_raw()
        await self.roster_logistics(ctx, star, key, roster)
        data = Embed.create(
            self, ctx, title='You got {}!'.format(key.title()),
            description="⭐" * int(star), footer_text="Demaratus | Grandmaster Crystal"
        )
        data.set_image(url=image)
        await ctx.send(embed=data)

    @crystal.command(aliases=["u"])
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def ultimate(self, ctx):
        """Open an Ultimate crystal."""
        starr = round(random.uniform(0, 100), 2)
        if starr < 20:
            star = "4"
        else:
            star = "3"
        key, image = (random.choice(list(FEATUREDS.items())))
        roster = await self.config.user(ctx.author).roster.get_raw()
        await self.roster_logistics(ctx, star, key, roster)
        data = Embed.create(
            self, ctx, title='You got {}!'.format(key.title()),
            description="⭐" * int(star), footer_text="Demaratus | Ultimate Crystal"
        )
        data.set_image(url=image)
        await ctx.send(embed=data)
    
    @commands.group(invoke_without_command=True)
    async def roster(self, ctx):
        """Access your crystal rosters."""
        await ctx.send("You'll be pleased to know, roster is getting worked on right now, this is Kreusada's top priority.")
    
    @roster.command(name="5")
    async def five(self, ctx, star: str = None):
        if await self.bot.is_owner(ctx.author) is False:
            return await ctx.send(_("<:success:777167188816560168> - `You are eligible for a roster, the champions you collect now will be stored.`\n<:error:777117297273077760> - `This feature is currently unavailable.`"), delete_after=10)
        if star is None:
            star = "5"
        try:
            roster: dict = await self.config.user(ctx.author).roster.get_raw(star)
        except KeyError:
            roster: dict = await self.config.user(ctx.author).roster.get_raw("5")
        if len(roster.values()) > 0:
            roster = "\n".join(
                ["{} s{}".format(key.title(), value) for key, value in roster.items()]
            )
            embed = discord.Embed(
                title="Crystal Roster: {} Star".format(star), color=ctx.author.color, description=":star::star::star::star::star:"
            )
            embed.add_field(name="{}'s Roster :arrow_down:".format(
                ctx.author.name), value=roster)
        else:
            embed = discord.Embed(
                title="Crystal Roster: {} Star :star:".format(star), color=ctx.author.color, description=(
                    "You don't have any {} star champions!\n"
                    "Collect some using `{}crystal`!".format(
                        star, ctx.clean_prefix
                    )
                )
            )
        await ctx.send(embed=embed)

    @roster.command(name="4")
    async def four(self, ctx, star: str = None):
        if await self.bot.is_owner(ctx.author) is False:
            return await ctx.send("<:success:777167188816560168> - `You are eligible for a roster, the champions you collect now will be stored.`\n<:error:777117297273077760> - `This feature is currently unavailable.`")
        if star is None:
            star = "4"
        try:
            roster: dict = await self.config.user(ctx.author).roster.get_raw(star)
        except KeyError:
            roster: dict = await self.config.user(ctx.author).roster.get_raw("4")
        if len(roster.values()) > 0:
            roster = "\n".join(
                ["{} s{}".format(key.title(), value) for key, value in roster.items()]
            )
            embed = discord.Embed(
                title="Crystal Roster: {} Star".format(star), color=ctx.author.color, description=":star::star::star::star:"
            )
            embed.add_field(name="{}'s Roster :arrow_down:".format(
                ctx.author.name), value=roster)
        else:
            embed = discord.Embed(
                title="Crystal Roster: {} Star :star:".format(star), color=ctx.author.color, description=(
                    "You don't have any {} star champions!\n"
                    "Collect some using `{}crystal`!".format(
                        star, ctx.clean_prefix
                    )
                )
            )
        await ctx.send(embed=embed)

    @roster.command(name="3")
    async def three(self, ctx, star: str = None):
#        if await self.bot.is_owner(ctx.author) is False:
#            return await ctx.send("<:success:777167188816560168> - `You are eligible for a roster, the champions you collect now will be stored.`\n<:error:777117297273077760> - `This feature is currently unavailable.`")
        if star is None:
            star = "3"
        try:
            roster: dict = await self.config.user(ctx.author).roster.get_raw(star)
        except KeyError:
            roster: dict = await self.config.user(ctx.author).roster.get_raw("3")
        if len(roster.values()) > 0:
            roster = "\n".join(
                ["{} s{}".format(key.title(), value) for key, value in roster.items()]
            )
            embed = discord.Embed(
                title="Crystal Roster: {} Star".format(star), color=ctx.author.color, description=":star::star::star:"
            )
            embed.add_field(name="{}'s Roster :arrow_down:".format(
                ctx.author.name), value=roster)
        else:
            embed = discord.Embed(
                title="Crystal Roster: {} Star :star:".format(star), color=ctx.author.color, description=(
                    "<error:777117297273077760> You don't have any {} star champions!\n"
                    "Collect some using `{}crystal`!".format(
                        star, ctx.clean_prefix
                    )
                )
            )
        await ctx.send(embed=embed)
     
    @commands.group()
    async def rosterset(self, ctx):
        """Additional roster configuration."""
        
    @rosterset.group()
    async def reset(self, ctx):
        """Reset your roster."""
    
    @reset.command(name="roster3")
    async def _roster3(self, ctx):
        """Reset your 3 star roster."""
        r3 = await self.config.guild(ctx.guild).get_raw("3")
        if r3 is not None:
            await self.removal(ctx, r3)
        else:
            await ctx.send("You don't have any 3 star champions in your roster!")

    @reset.command(name="roster4")
    async def _roster4(self, ctx):
        """Reset your 4 star roster."""
        r4 = await self.config.guild(ctx.guild).get_raw("4")
        if r4 is not None:
            await self.removal(ctx, r4)
        else:
            await ctx.send("You don't have any 4 star champions in your roster!")


    @reset.command(name="roster5")
    async def _roster5(self, ctx):
        """Reset your 5 star roster."""
        r5 = await self.config.guild(ctx.guild).get_raw("5")
        if r5 is not None:
            await self.removal(ctx, r5)
        else:
            await ctx.send("You don't have any 5 star champions in your roster!")
        

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
        data = Embed.create(self, ctx, title=title,
                            description=description, image=link)
        await ctx.send(embed=data)

    @battlechip.command()
    async def uncollected(self, ctx):
        """Open an uncollected battlechip crystal."""
        drop_rate = round(random.uniform(0, 100), 2)
        if drop_rate < 0.02:
            link = BCB[0]
            title = "5 Star Punisher"
            description = "This tier has a `0.02%` chance.\nCongratulations!"
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
            roster[star][champion] += sigs  # Test
        except KeyError:
            roster[star][champion] = 0
        await self.config.user(ctx.author).roster.set_raw(value=roster)

    @commands.command()
    async def awbadge(self, ctx, tier: str = None, group: int = None):
        """Get alliance war badges."""
        if group is not None and group >= 1 and group < 4:
            group_num = group - 1  # This is to make sure that it will work with the urls
        tiers = {
            "master": [
                "https://media.discordapp.net/attachments/401476363707744257/738083791654092940/47EFB6D4D1380ABD2C40D2C7B0533A29245F7955.png",
                "https://media.discordapp.net/attachments/401476363707744257/738083791113027654/650E29ADB8C5C382FF5A358113B2C02B8EADA415.png",
                "https://media.discordapp.net/attachments/401476363707744257/738083791440052294/08BA0A081A9D56E35E60E3FD61FAB7ED9A10CD00.png"
            ],
            "platinum": [
                "https://media.discordapp.net/attachments/401476363707744257/738083790718631937/E78E2BAF9B0C9BA6C7FE45BE726FFB0B0B0CACFD.png",
                "https://media.discordapp.net/attachments/401476363707744257/738083790362116116/487EA26A1BA0F2C2848E7C87F10430BD218C2178.png",
                "https://media.discordapp.net/attachments/401476363707744257/738083790559117352/0ED8BD10441C6D086AEB7BBA5271269F46E009D1.png"
            ],
            "gold": [
                "https://media.discordapp.net/attachments/401476363707744257/738083790131298375/76BC21BF523A415866D19814BD8AF4BE16EF30A9.png",
                "https://media.discordapp.net/attachments/401476363707744257/738083998462509096/8CD52FEB7540016B6ABA1EC67B9F1777E3C29878.png",
                "https://media.discordapp.net/attachments/401476363707744257/738084001926873098/3A9A8FDA006D0BE225242AAA5909021CD52BCFB3.png"
            ],
            "silver": [
                "https://media.discordapp.net/attachments/401476363707744257/738084001465499789/4B389D377A94EDA747B38DF640C0B33A3A3F61AE.png",
                "https://media.discordapp.net/attachments/401476363707744257/738084001465499789/4B389D377A94EDA747B38DF640C0B33A3A3F61AE.png",
                "https://media.discordapp.net/attachments/401476363707744257/738083994612006914/5302FA8FA04735224847C8BBF82D1D54C8567B9C.png"
            ],
            "bronze": [
                "https://media.discordapp.net/attachments/401476363707744257/738083995211792404/719AC2C2AB5833D815C899DAF9ADB7CF11819CBA.png",
                "https://media.discordapp.net/attachments/401476363707744257/738083993043337276/E636A90C3F0DFFDAED0176D972AA0C73F3E40FF8.png",
                "https://media.discordapp.net/attachments/401476363707744257/738083997866786876/5B06D509847E0FA1405A50021486C1A5D8C6F9B2.png"
            ],
            "stone": [
                "https://media.discordapp.net/attachments/401476363707744257/738083996054978730/9AC92A2FDC2996C346125296356C664373147F2F.png",
                "https://media.discordapp.net/attachments/401476363707744257/738083993681002586/BF3D13EACC9F44216E754884AA183185761C84CF.png",
                "https://media.discordapp.net/attachments/401476363707744257/738084098857238670/EA938C0B0C2AE3E6DB91514F5F8768C4F033D373.png"
            ]
        }
        tier = tier.lower() if tier is not None else None
        if tier is None or tier not in tiers:
            embed = Embed.create(
                self, ctx, title="Alliance War Badge Tiers",
                description="Please choose one of the tiers below :arrow_down:\nSyntax: `,awbadge <tier>`"
            )
            normal = "\n".join([t.capitalize() for t in tiers.keys()])
            embed.add_field(
                # Unfortunatly I have to do this to make sure that participation gets in the list :/
                name="Badges", value="{}\nParticipation".format(normal)
            )

            normal = "\n".join(tiers)
            return await ctx.send(embed=embed)
        if tier == "participation":
            embed = Embed.create(
                self, ctx, title="Participation",
                image="https://media.discordapp.net/attachments/401476363707744257/738083790886535228/DA7D39277836A9CF1B39A68D37EAF99999B366C7.png"
            )
            return await ctx.send(embed=embed)
        if group is None:
            embeds = []
            for i in range(3):
                embed = Embed.create(
                    self, ctx,
                    title="{} Badges".format(tier.capitalize()), image=tiers[tier][i]
                )
                embeds.append(embed)
            msg = await ctx.send(embed=embeds[0])
            control = menus.DEFAULT_CONTROLS if len(embeds) > 1 else {
                "\N{CROSS MARK}": menus.close_menu
            }
            asyncio.create_task(menus.menu(ctx, embeds, control, message=msg))
            menus.start_adding_reactions(msg, control.keys())
        else:
            embed = Embed.create(
                self, ctx,
                title="{} Badge".format(tier.capitalize()), description="{} {}".format(tier.capitalize(), group),
                image=tiers[tier][group_num]
            )
            await ctx.send(embed=embed)

    async def removal(self, ctx: commands.Context, action: str):
        message = "Would you like to reset the {}?".format(action)
        can_react = ctx.channel.permissions_for(ctx.me).add_reactions
        if not can_react:
            message += " (y/n)"
        question: discord.Message = await ctx.send(message)
        if can_react:
            start_adding_reactions(
                question, ReactionPredicate.YES_OR_NO_EMOJIS
            )
            pred = ReactionPredicate.yes_or_no(question, ctx.author)
            event = "reaction_add"
        else:
            pred = MessagePredicate.yes_or_no(ctx)
            event = "message"
        try:
            await ctx.bot.wait_for(event, check=pred, timeout=20)
        except asyncio.TimeoutError:
            await question.delete()
            await ctx.send("Okay then :D")
        if not pred.result:
            await question.delete()
            return await ctx.send("Canceled!")
        else:
            if can_react:
                with suppress(discord.Forbidden):
                    await question.clear_reactions()
        await self.config.guild(ctx.guild).set_raw(action, value=None)
        await ctx.send("Removed the {}!".format(action))
