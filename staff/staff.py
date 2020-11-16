import discord
from validator_collection import validators
from datetime import datetime
from redbot.core import commands, checks, Config
from .staffembed import Embed

class Staff(commands.Cog):
    """Cog for alerting Staff."""

    def __init__(self):
        self.config = Config.get_conf(
            self, 200730042020, force_registration=True)
        self.config.register_guild(
            role=None,
            channel=None
        )

    @commands.group()
    async def staffset(self, ctx):
        """Staff notifier configuration."""

    @staffset.command()
    @commands.mod()
    async def channel(self, ctx, channel: discord.TextChannel):
        """Sets the channel for staff to receive notifications."""
        await self.config.guild(ctx.guild).set_raw("channel", value=channel.id)
        embed =Embed.create(
            self, ctx, title="Successful <:success:777167188816560168>",
            description="{} will now receive notifications from users to notify the staff.".format(
                channel.mention
            )
        )
        await ctx.send(embed=embed)

    @staffset.command()
    @commands.mod()
    async def role(self, ctx, role: discord.Role):
        """Sets the Staff role."""
        try:
            await self.config.guild(ctx.guild).set_raw("role", value=role.id)
            embed = Embed.create(
                self, ctx, title="Successful <:success:777167188816560168>",
                description=f"{role.mention} will now be considered as the Staff role.",
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = Embed.create(
                self, ctx, title="Oopsies! <:error:777117297273077760>",
                description=f"Something went wrong during the setup process."
            )
            await ctx.send(embed=embed)

    @commands.command()
    #@commands.cooldown(1, 600, commands.BucketType.user)
    async def staff(self, ctx):
        """Notifies the staff."""
        embed = Embed.create(
            self, ctx, title='<:alert:777928824670388254> The Staff have been notified.',
            description = (
                "Please keep your cool, and if required, try to disperse the situation."
                "A member of our Staff team will be with you as soon as possible."
                )
        )
        role = ctx.guild.get_role(await self.config.guild(ctx.guild).get_raw("role"))
        chan = await self.config.guild(ctx.guild).get_raw("channel")
        channel = ctx.guild.get_channel(chan) if chan is not None\
            else ctx.channel
        if role is not None:
            embed = Embed.create(
                self, ctx, title='<:alert:777928824670388254> ALERT!',
                description=(
                    f"**{ctx.author}** has just called for the staff in {ctx.channel.mention}.\n\n**Requested at: {} on {}**"
                )
                footer=datetime.now(timezone.utc)
                    
            )
            await channel.send(content=role.mention, allowed_mentions=discord.AllowedMentions(roles=True), embed=embed)
        else:
            embed = Embed.create(
                self, ctx, title="The Staff team have not completed the command setup. <:error:777117297273077760>",
                description=(
                    "This is a requirement for the staff command to function.\n"
                )
            )
            await ctx.send(embed=embed)
