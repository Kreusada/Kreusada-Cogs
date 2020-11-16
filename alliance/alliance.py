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

    @commands.group(name="alliancealert", aliases=["aa", ])
    async def aa(self, ctx):  # aliases: aa, alert):
        """Alert your fellow alliance mates for movement."""

    @aa.group(name="set")
    @commands.admin_or_permissions(manage_guild=True)
    async def aas(self, ctx):
        """Alliance alert settings"""

    @aas.command()
    async def showsettings(self, ctx):
        rol = await self.config.guild(ctx.guild).get_raw("role")
        chan = await self.config.guild(ctx.guild).get_raw("channel")
        role = ctx.guild.get_role(rol) if rol is not None\
            else None
        channel = ctx.guild.get_channel(chan) if chan is not None\
            else None
        embed = Embed.create(
            self, ctx, title="{}'s Settings".format(ctx.guild.name),
            description="**Role:** {}\n**Channel:** {}".format(
                role.mention, channel.mention),
            thumbnail=ctx.guild.icon_url
        )
        await ctx.send(embed=embed)

    @aas.command()
    async def channel(self, ctx, channel: discord.TextChannel):
        await self.config.guild(ctx.guild).set_raw("channel", value=channel.id)
        embed = Embed.create(
            self, ctx, title="Successful <:success:777167188816560168>",
            description="{} will now be the channel that the alerts will be sent to when Alliance events start".format(
                channel.mention,
                thumbnail=ctx.guild.icon_url
            )
        )
        await ctx.send(embed=embed)

    @aas.command()
    async def role(self, ctx, role: discord.Role):
        try:
            await self.config.guild(ctx.guild).set_raw("role", value=role.id)
            embed = Embed.create(
                self, ctx, title="Successful <:success:777167188816560168>",
                description=f"{role.mention} will now be mentioned when Alliance events start.",
                thumbnail=ctx.guild.icon_url
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
                thumbnail=ctx.guild.icon_url
            )
            await channel.send(content=role.mention, allowed_mentions=discord.AllowedMentions(roles=True), embed=embed)
        else:
            embed = Embed.create(
                self, ctx, title="Error! <:error:777117297273077760>",
                description=(
                    "Your guild does not have a role set up for the alerts!\n"
                    "To set up a role, use `{}alliancealert|aa set role <role>`".format(
                        ctx.clean_prefix
                    )
                ),
                thumbnail=ctx.guild.icon_url
            )
            await ctx.send(embed=embed)

    @aa.command(invoke_without_command=True, pass_context=True, aliases=["aqg"])
    async def aqglory(self, ctx):
        """Collect your glory rewards."""
        embed = Embed.create(
            self, ctx, title='<:info:777656123381383209> The Alliance Quest cycle has ended.',
            image = "https://media.discordapp.net/attachments/763066391107862550/777865235746783232/aqglory.png?width=1442&height=481",
            description = "Collect your glory rewards."
        )
        role = ctx.guild.get_role(await self.config.guild(ctx.guild).get_raw("role"))
        chan = await self.config.guild(ctx.guild).get_raw("channel")
        channel = ctx.guild.get_channel(chan) if chan is not None\
            else ctx.channel
        if role is not None:
            embed = Embed.create(
                self, ctx, title='<:info:777656123381383209> The Alliance Quest cycle has ended.',
                image = "https://media.discordapp.net/attachments/763066391107862550/777865235746783232/aqglory.png?width=1442&height=481",
                description = "Collect your glory rewards."
                thumbnail=ctx.guild.icon_url
            )
            await channel.send(content=role.mention, allowed_mentions=discord.AllowedMentions(roles=True), embed=embed)
        else:
            embed = Embed.create(
                self, ctx, title="Error! <:error:777117297273077760>",
                description=(
                    "Your guild does not have a role set up for the alerts!\n"
                    "To set up a role, use `{}alliancealert set role <role>`".format(
                        ctx.clean_prefix
                    )
                ),
                thumbnail=ctx.guild.icon_url
            )
            await ctx.send(embed=embed)

    @aa.command(invoke_without_command=True, pass_context=True, aliases=["awv, aww"])
    async def awvictory(self, ctx):
        """Alliance War ended in Victory."""
        embed = Embed.create(
            self, ctx, title='<:aha:777867124706246687> Alliance War has ended in VICTORY!',
            image = "https://media.discordapp.net/attachments/763066391107862550/777865265882988564/awvictory.png?width=1442&height=481",
            description = "Good job everyone!"
        )
        role = ctx.guild.get_role(await self.config.guild(ctx.guild).get_raw("role"))
        chan = await self.config.guild(ctx.guild).get_raw("channel")
        channel = ctx.guild.get_channel(chan) if chan is not None\
            else ctx.channel
        if role is not None:
            embed = Embed.create(
                self, ctx, title='<:aha:777867124706246687> Alliance War has ended in VICTORY!',
                image = "https://media.discordapp.net/attachments/763066391107862550/777865265882988564/awvictory.png?width=1442&height=481",
                description = "Good job everyone!"
                thumbnail=ctx.guild.icon_url
            )
            await channel.send(content=role.mention, allowed_mentions=discord.AllowedMentions(roles=True), embed=embed)
        else:
            embed = Embed.create(
                self, ctx, title="Error! <:error:777117297273077760>",
                description=(
                    "Your guild does not have a role set up for the alerts!\n"
                    "To set up a role, use `{}alliancealert set role <role>`".format(
                        ctx.clean_prefix
                    )
                ),
                thumbnail=ctx.guild.icon_url
            )
            await ctx.send(embed=embed)

    @aa.command(invoke_without_command=True, pass_context=True, aliases=["awv, aww"])
    async def awdefeat(self, ctx):
        """Alliance War ended in Defeat."""
        embed = Embed.create(
            self, ctx, title='<:notlikecat:766419778822078524> Alliance War has ended in DEFEAT.',
            image = "https://media.discordapp.net/attachments/763066391107862550/777865262329626635/awdefeat.png?width=1442&height=481",
            description = "Better luck next time. :cry:"
        )
        role = ctx.guild.get_role(await self.config.guild(ctx.guild).get_raw("role"))
        chan = await self.config.guild(ctx.guild).get_raw("channel")
        channel = ctx.guild.get_channel(chan) if chan is not None\
            else ctx.channel
        if role is not None:
            embed = Embed.create(
                self, ctx, title='<:notlikecat:766419778822078524> Alliance War has ended in DEFEAT.',
                image = "https://media.discordapp.net/attachments/763066391107862550/777865262329626635/awdefeat.png?width=1442&height=481",
                description = "Better luck next time. :cry:"
                thumbnail=ctx.guild.icon_url
            )
            await channel.send(content=role.mention, allowed_mentions=discord.AllowedMentions(roles=True), embed=embed)
        else:
            embed = Embed.create(
                self, ctx, title="Error! <:error:777117297273077760>",
                description=(
                    "Your guild does not have a role set up for the alerts!\n"
                    "To set up a role, use `{}alliancealert set role <role>`".format(
                        ctx.clean_prefix
                    )
                ),
                thumbnail=ctx.guild.icon_url
            )
            await ctx.send(embed=embed)

    @aa.command(invoke_without_command=True, pass_context=True, aliases=["awa"])
    async def awattack(self, ctx):
        """Alliance War attack phase."""
        embed = Embed.create(
            self, ctx, title='<:info:777656123381383209> Attack Phase has started!',
            image = "https://media.discordapp.net/attachments/763066391107862550/777865273272565760/awattack.png?width=1442&height=481",
            description = "Time to join attack phase. Check with officers in case you need to take a certain path."
        )
        role = ctx.guild.get_role(await self.config.guild(ctx.guild).get_raw("role"))
        chan = await self.config.guild(ctx.guild).get_raw("channel")
        channel = ctx.guild.get_channel(chan) if chan is not None\
            else ctx.channel
        if role is not None:
            embed = Embed.create(
                self, ctx, title='<:info:777656123381383209> Attack Phase has started!',
                image = "https://media.discordapp.net/attachments/763066391107862550/777865273272565760/awattack.png?width=1442&height=481",
                description = "Time to join attack phase. Check with officers in case you need to take a certain path."
                thumbnail=ctx.guild.icon_url
            )
            await channel.send(content=role.mention, allowed_mentions=discord.AllowedMentions(roles=True), embed=embed)
        else:
            embed = Embed.create(
                self, ctx, title="Error! <:error:777117297273077760>",
                description=(
                    "Your guild does not have a role set up for the alerts!\n"
                    "To set up a role, use `{}alliancealert set role <role>`".format(
                        ctx.clean_prefix
                    )
                ),
                thumbnail=ctx.guild.icon_url
            )
            await ctx.send(embed=embed)

    @aa.command(invoke_without_command=True, pass_context=True, aliases=["awp"])
    async def awplacement(self, ctx):
        """Alliance War placement phase."""
        embed = Embed.create(
            self, ctx, title='<:info:777656123381383209> Placement Phase has started!',
            image = "https://media.discordapp.net/attachments/763066391107862550/777865276531671080/awplacement.png?width=1442&height=481",
            description = "Time to place your defenders, Check with officers in case you place your defenders in a certain place."
        )
        role = ctx.guild.get_role(await self.config.guild(ctx.guild).get_raw("role"))
        chan = await self.config.guild(ctx.guild).get_raw("channel")
        channel = ctx.guild.get_channel(chan) if chan is not None\
            else ctx.channel
        if role is not None:
            embed = Embed.create(
                self, ctx, title='<:info:777656123381383209> Placement Phase has started!',
                image = "https://media.discordapp.net/attachments/763066391107862550/777865276531671080/awplacement.png?width=1442&height=481",
                description = "Time to place your defenders, Check with officers in case you place your defenders in a certain place."
                thumbnail=ctx.guild.icon_url
            )
            await channel.send(content=role.mention, allowed_mentions=discord.AllowedMentions(roles=True), embed=embed)
        else:
            embed = Embed.create(
                self, ctx, title="Error! <:error:777117297273077760>",
                description=(
                    "Your guild does not have a role set up for the alerts!\n"
                    "To set up a role, use `{}alliancealert set role <role>`".format(
                        ctx.clean_prefix
                    )
                ),
                thumbnail=ctx.guild.icon_url
            )
            await ctx.send(embed=embed)
