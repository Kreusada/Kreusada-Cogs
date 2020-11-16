import discord
from validator_collection import validators
from datetime import datetime
from redbot.core import commands, checks, Config, modlog
from .staffembed import Embed

class Staff(commands.Cog):
    """Cog for alerting Staff."""

    def __init__(self):
        self.config = Config.get_conf(
            self, 200730042020, force_registration=True)
        default_guild = {"modlog": True}
        self.config.register_guild(
            role=None,
            channel=None
        )
        
    @staticmethod
    async def register_casetypes():
        new_types = [
            {
                "name": "alert_created",
                "default_setting": True,
                "image": "\N{BALLOT BOX WITH BALLOT}\N{VARIATION SELECTOR-16}",
                "case_str": "Alert created",
            }
        ]
        await modlog.register_casetypes(new_types)

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
            description=f"{channel.mention} will now receive notifications from users to notify the staff."
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

    @staffset.command()
    @commands.mod()
    async def modlog(self, ctx, true_or_false: bool):
        """Decide if alerts should log to modlog."""
        await self.config.guild(ctx.guild).modlog.set(true_or_false)
        embed = Embed.create(
            self, ctx, title="Successful <:success:777167188816560168>",
            description="Logging to modlog has been {}.".format("enabled" if true_or_false else "disabled")
        )
        await ctx.send(embed=embed

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
                description=f"**{ctx.author.name}** has just called for the staff in {ctx.channel.mention}."
#                embed.set_footer(datetime.now(timezone.utc))  
            )
            msg = await channel.send(content=role.mention, allowed_mentions=discord.AllowedMentions(roles=True), embed=embed)
            await msg.add_reaction("✅")
        else:
            embed = Embed.create(
                self, ctx, title="The Staff team have not completed the command setup. <:error:777117297273077760>",
                description=(
                    "This is a requirement for the staff command to function.\n"
                )
            )
            await ctx.send(embed=embed)
