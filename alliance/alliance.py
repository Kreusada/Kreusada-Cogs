import discord
from validator_collection import validators
from redbot.core import commands, checks, Config
from .allianceembed import Embed


class Alliance(commands.Cog):
    """Tools for your alliance on MCOC."""

    def __init__(self):
        self.config = Config.get_conf(
            self, 200730042020, force_registration=True)
        self.config.register_guild(
            role=None,
            channel=None
        )

    @commands.command()
    async def timezone(self, ctx, *, timezone: str = None):
        """
        Use this command to set your timezone on your nickname.
        For example - `Kreusada [+4]`
        """
        if timezone is None:
            await ctx.author.edit(nick=ctx.author.name)
            embed = Embed.create(
                self, ctx, title="Successful <:success:777167188816560168>",
                description=f"""
                You can set your nickname using `dem timezone <timezone>`.
                For example: `dem timezone +4` or `dem timezone -12`.
                Your timezone is no longer shown on your nickname (`{ctx.author.name}`)
                """
            )
            return await ctx.send(embed=embed)
        user = ctx.author
        before = ctx.author.name
        after = timezone
        tag = "{0} [{1}]".format(before, after)
        try:
            await user.edit(nick=tag)
            embed = Embed.create(
                self, ctx, title="Successful <:success:777167188816560168>",
                description="Your timezone is now displayed on your nickname as: ``{}``".format(
                    tag),
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = Embed.create(
                self, ctx, title="Oopsies! <:error:777117297273077760>",
                description="""
                    Something went wrong during the setup process, I could not change your nickname.
                    This may be due to the following errors:
                    :x: `Invalid Permissions`
                    :x: `Role Heirarchy`
                    Please resolve these issues before I can set nicknames.
                    If you are the server owner, the heirarchy between us cannot be justified.
                    If problems continue, please ask for help in our [support server](https://discord.gg/JmCFyq7).
                    """,
            )
            await ctx.send(embed=embed)

    @commands.group(name="alliancealert", aliases=["aa", ])#, autohelp=False)
    async def aa(self, ctx):
        """Alert your fellow alliance mates for movement."""
#        embed = Embed.create(
#            self, ctx, title="Alert Help Menu",
#            description=(
#                "**Alert your fellow alliance mates for alliance activity.**\n\n"
#                "`Syntax: {}alliancealert <alert_type>`\n\n"
#                "**__Subcommands__**\n"
#                "**aqglory** Announces for glory collection.\n"
#                "**aqstart** Announces for AQ starting.\n"
#                "**awattack** Announces for AW attack phase starting.\n"
#                "**awdefeat** Announces for AW defeat.\n"
#                "**awplacement** Announces for AW attack phase starting.\n"
#                "**awvictory** Announces for AW Victory.\n\n"
#                "**Additional Support**\n"
#                "Contact us in our [support server](https://discord.gg/JmCFyq7).".format(
#                    ctx.clean_prefix, ctx.clean_prefix
#                )
#            )
#        )
#        await ctx.send(embed=embed)

    @commands.group(name="alliancealertset", aliases=["aas"])#,autohelp=False)
    @commands.admin_or_permissions(manage_guild=True)
    async def aas(self, ctx):
        """Alliance alert configuration."""
#        embed = Embed.create(
#            self, ctx, title="Configuration Help Menu",
#            description=(
#                "**channel** Set the channel for alerts to be sent to.\n"
#                "**role** Set the role to be mentioned for alerts.\n\n"
#                "Need more support? Contact us in our [support server](https://discord.gg/JmCFyq7)."
#            )
#        )
#        await ctx.send(embed=embed)
            
    @aas.command()
    async def showsettings(self, ctx):
        """Shows the current alert settings."""
        rol = await self.config.guild(ctx.guild).get_raw("role")
        chan = await self.config.guild(ctx.guild).get_raw("channel")
        role = ctx.guild.get_role(rol) if rol is not None\
            else None
        channel = ctx.guild.get_channel(chan) if chan is not None\
            else None
        embed = Embed.create(
            self, ctx, title="{}'s Settings".format(ctx.guild.name),
            description="**Role:** {}\n**Channel:** {}".format(
                role.mention, channel.mention)
        )
        await ctx.send(embed=embed)

    @aas.command()
    async def channel(self, ctx, channel: discord.TextChannel):
        """Sets the discord channel for alerts to be sent to."""
        await self.config.guild(ctx.guild).set_raw("channel", value=channel.id)
        embed = Embed.create(
            self, ctx, title="Successful <:success:777167188816560168>",
            description="{} will now be the channel that the alerts will be sent to when Alliance events start".format(
                channel.mention
            )
        )
        await ctx.send(embed=embed)

    @aas.command(invoke_without_command=True)
    async def role(self, ctx, role: discord.Role):
        """Sets the discord role to be notified for alerts."""
        try:
            await self.config.guild(ctx.guild).set_raw("role", value=role.id)
            embed = Embed.create(
                self, ctx, title="Successful <:success:777167188816560168>",
                description=f"{role.mention} will now be mentioned when Alliance events start.",
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = Embed.create(
                self, ctx, title="Oopsies! <:error:777117297273077760>",
                description=f"Something went wrong during the setup process."
            )
            await ctx.send(embed=embed)

    @aa.command(invoke_without_command=True, pass_context=True, aliases=["aqs"])
    async def aqstart(self, ctx):
        """Alliance Quest has started!"""
        embed = Embed.create(
            self, ctx, title='<:info:777656123381383209> Alliance Quest has STARTED!',
            image = "https://media.discordapp.net/attachments/763066391107862550/777865269477376030/aqstarted.png?width=1442&height=481",
            description = "Time to join Alliance Quest."
        )
        role = ctx.guild.get_role(await self.config.guild(ctx.guild).get_raw("role"))
        chan = await self.config.guild(ctx.guild).get_raw("channel")
        channel = ctx.guild.get_channel(chan) if chan is not None\
            else ctx.channel
        if role is not None:
            embed = Embed.create(
                self, ctx, title='<:info:777656123381383209> Alliance Quest has STARTED!',
                image="https://media.discordapp.net/attachments/763066391107862550/777865269477376030/aqstarted.png?width=1442&height=481",
                description="Time to join Alliance Quest.",
            )
            await channel.send(content=role.mention, allowed_mentions=discord.AllowedMentions(roles=True), embed=embed)
        else:
            embed = Embed.create(
                self, ctx, title="Error! <:error:777117297273077760>",
                description=(
                    "Your guild does not have a role set up for the alerts!\n"
                    "This is a requirement for alliance alerts.\n"
                    "To set up a role, use `{}alliancealert set role <role>`".format(ctx.clean_prefix)
                )
            )
            await ctx.send(embed=embed)

    @aa.command(invoke_without_command=True, pass_context=True, aliases=["aqg"])
    async def aqglory(self, ctx):
        """Collect your glory rewards."""
        embed = Embed.create(
            self, ctx, title='<:info:777656123381383209> The Alliance Quest cycle has ended.',
            image = "https://media.discordapp.net/attachments/763066391107862550/777865235746783232/aqglory.png?width=1442&height=481",
            description = "Collect your glory rewards.",
            color = 0xffc64d
        )
        role = ctx.guild.get_role(await self.config.guild(ctx.guild).get_raw("role"))
        chan = await self.config.guild(ctx.guild).get_raw("channel")
        channel = ctx.guild.get_channel(chan) if chan is not None\
            else ctx.channel
        if role is not None:
            embed = Embed.create(
                self, ctx, title='<:info:777656123381383209> The Alliance Quest cycle has ended.',
                image = "https://media.discordapp.net/attachments/763066391107862550/777865235746783232/aqglory.png?width=1442&height=481",
                description = "Collect your glory rewards.",
                color = 0xffc64d
            )
            await channel.send(content=role.mention, allowed_mentions=discord.AllowedMentions(roles=True), embed=embed)
        else:
            embed = Embed.create(
                self, ctx, title="Error! <:error:777117297273077760>",
                description=(
                    "Your guild does not have a role set up for the alerts!\n"
                    "This is a requirement for alliance alerts.\n"
                    "To set up a role, use `{}alliancealert set role <role>`".format(ctx.clean_prefix)
                )
            )
            await ctx.send(embed=embed)

    @aa.command(invoke_without_command=True, pass_context=True, aliases=["awv"])
    async def awvictory(self, ctx):
        """Alliance War ended in Victory."""
        embed = Embed.create(
            self, ctx, title='<:aha:777867124706246687> Alliance War has ended in VICTORY!',
            image = "https://media.discordapp.net/attachments/763066391107862550/777865265882988564/awvictory.png?width=1442&height=481",
            description = "Good job everyone!",
            color = 0x59e1ac
        )
        role = ctx.guild.get_role(await self.config.guild(ctx.guild).get_raw("role"))
        chan = await self.config.guild(ctx.guild).get_raw("channel")
        channel = ctx.guild.get_channel(chan) if chan is not None\
            else ctx.channel
        if role is not None:
            embed = Embed.create(
                self, ctx, title='<:aha:777867124706246687> Alliance War has ended in VICTORY!',
                image = "https://media.discordapp.net/attachments/763066391107862550/777865265882988564/awvictory.png?width=1442&height=481",
                description = "Good job everyone!",
                color = 0x59e1ac
            )
            await channel.send(content=role.mention, allowed_mentions=discord.AllowedMentions(roles=True), embed=embed)
        else:
            embed = Embed.create(
                self, ctx, title="Error! <:error:777117297273077760>",
                description=(
                    "Your guild does not have a role set up for the alerts!\n"
                    "This is a requirement for alliance alerts.\n"
                    "To set up a role, use `{}alliancealert set role <role>`".format(ctx.clean_prefix)
                )
            )
            await ctx.send(embed=embed)

    @aa.command(invoke_without_command=True, pass_context=True, aliases=["awv, aww"])
    async def awdefeat(self, ctx):
        """Alliance War ended in Defeat."""
        embed = Embed.create(
            self, ctx, title='<:notlikecat:766419778822078524> Alliance War has ended in DEFEAT.',
            image = "https://media.discordapp.net/attachments/763066391107862550/777865262329626635/awdefeat.png?width=1442&height=481",
            description = "Better luck next time. :cry:",
            color = 0xd32f2f
        )
        role = ctx.guild.get_role(await self.config.guild(ctx.guild).get_raw("role"))
        chan = await self.config.guild(ctx.guild).get_raw("channel")
        channel = ctx.guild.get_channel(chan) if chan is not None\
            else ctx.channel
        if role is not None:
            embed = Embed.create(
                self, ctx, title='<:notlikecat:766419778822078524> Alliance War has ended in DEFEAT.',
                image = "https://media.discordapp.net/attachments/763066391107862550/777865262329626635/awdefeat.png?width=1442&height=481",
                description = "Better luck next time. :cry:",
                color = 0xd32f2f
            )
            await channel.send(content=role.mention, allowed_mentions=discord.AllowedMentions(roles=True), embed=embed)
        else:
            embed = Embed.create(
                self, ctx, title="Error! <:error:777117297273077760>",
                description=(
                    "Your guild does not have a role set up for the alerts!\n"
                    "This is a requirement for alliance alerts.\n"
                    "To set up a role, use `{}alliancealert set role <role>`".format(ctx.clean_prefix)
                )
            )
            await ctx.send(embed=embed)

    @aa.command(invoke_without_command=True, pass_context=True, aliases=["awa"])
    async def awattack(self, ctx):
        """Alliance War attack phase."""
        embed = Embed.create(
            self, ctx, title='<:info:777656123381383209> Attack Phase has started!',
            image = "https://media.discordapp.net/attachments/763066391107862550/777865273272565760/awattack.png?width=1442&height=481",
            description = "Time to join attack phase. Check with officers in case you need to take a certain path.",
            color = 0xffc64d
        )
        role = ctx.guild.get_role(await self.config.guild(ctx.guild).get_raw("role"))
        chan = await self.config.guild(ctx.guild).get_raw("channel")
        channel = ctx.guild.get_channel(chan) if chan is not None\
            else ctx.channel
        if role is not None:
            embed = Embed.create(
                self, ctx, title='<:info:777656123381383209> Attack Phase has started!',
                image = "https://media.discordapp.net/attachments/763066391107862550/777865273272565760/awattack.png?width=1442&height=481",
                description = "Time to join attack phase. Check with officers in case you need to take a certain path.",
                color = 0xffc64d
            )
            await channel.send(content=role.mention, allowed_mentions=discord.AllowedMentions(roles=True), embed=embed)
        else:
            embed = Embed.create(
                self, ctx, title="Error! <:error:777117297273077760>",
                description=(
                    "Your guild does not have a role set up for the alerts!\n"
                    "This is a requirement for alliance alerts.\n"
                    "To set up a role, use `{}alliancealert set role <role>`".format(ctx.clean_prefix)
                )
            )
            await ctx.send(embed=embed)

    @aa.command(invoke_without_command=True, pass_context=True, aliases=["awp"])
    async def awplacement(self, ctx):
        """Alliance War placement phase."""
        embed = Embed.create(
            self, ctx, title='<:info:777656123381383209> Placement Phase has started!',
            image = "https://media.discordapp.net/attachments/763066391107862550/777865276531671080/awplacement.png?width=1442&height=481",
            description = "Time to place your defenders, Check with officers in case you place your defenders in a certain place.",
            color = 0xffc64d
        )
        role = ctx.guild.get_role(await self.config.guild(ctx.guild).get_raw("role"))
        chan = await self.config.guild(ctx.guild).get_raw("channel")
        channel = ctx.guild.get_channel(chan) if chan is not None\
            else ctx.channel
        if role is not None:
            embed = Embed.create(
                self, ctx, title='<:info:777656123381383209> Placement Phase has started!',
                image = "https://media.discordapp.net/attachments/763066391107862550/777865276531671080/awplacement.png?width=1442&height=481",
                description = "Time to place your defenders, Check with officers in case you place your defenders in a certain place.",
                color = 0xffc64d
            )
            await channel.send(content=role.mention, allowed_mentions=discord.AllowedMentions(roles=True), embed=embed)
        else:
            embed = Embed.create(
                self, ctx, title="Error! <:error:777117297273077760>",
                description=(
                    "Your guild does not have a role set up for the alerts!\n"
                    "This is a requirement for alliance alerts.\n"
                    "To set up a role, use `{}alliancealert set role <role>`".format(ctx.clean_prefix)
                )
            )
            await ctx.send(embed=embed)
