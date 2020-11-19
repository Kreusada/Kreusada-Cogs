import discord
from validator_collection import validators
from redbot.core import commands, checks, Config
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.predicates import ReactionPredicate, MessagePredicate
from contextlib import suppress
import asyncio
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
    async def aa(self, ctx):
        """Alert your fellow alliance mates for movement."""

    @commands.group(name="alertset", aliases=["aas", "as"])
    @commands.admin_or_permissions(manage_guild=True)
    async def aas(self, ctx):
        """Alliance alert settings"""

    @aas.command()
    async def showsettings(self, ctx):
      """Shows the curernt settings for alerts."""
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
      """Configures the channel where alerts are sent."""
      await self.config.guild(ctx.guild).set_raw("channel", value=channel.id)
      embed = Embed.create(
          self, ctx, title="Successful <:success:777167188816560168>",
          description="{} will now be the channel that the alerts will be sent to when Alliance events start".format(
              channel.mention)
      )
      await ctx.send(embed=embed)

    @aas.command()
    async def role(self, ctx, role: discord.Role):
      """Configures the role to be mentioned for alerts."""
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

    @aas.group()
    async def reset(self, ctx):
        """Reset the values for the alliance alert system"""

    @reset.command(name="role")
    async def _role(self, ctx: commands.Context):
        """Resets the role that is mentioned when alerting your alliance"""
        role = await self.config.guild(ctx.guild).get_raw("channel")
        if role is not None:
            await self.removal(ctx, "role")
        else:
            await ctx.send("You don't have a role set up!")

    @reset.command(name="channel")
    async def _channel(self, ctx: commands.Context):
        """Reset the channel"""
        channel = await self.config.guild(ctx.guild).get_raw("channel")
        if channel is not None:
            await self.removal(ctx, "channel")
        else:
            await ctx.send("You don't have a channel set up!")

    @aa.command(aliases=["aqs"])
    async def aqstart(self, ctx):
        """Alerts for alliance quest starting."""
        role = ctx.guild.get_role(await self.config.guild(ctx.guild).get_raw("role"))
        chan = await self.config.guild(ctx.guild).get_raw("channel")
        channel = ctx.guild.get_channel(chan) if chan is not None\
            else ctx.channel
        if role is not None:
            embed = Embed.create(
                self, ctx, title='Alliance Quest has STARTED!',
                image="https://media.discordapp.net/attachments/758775890954944572/779045288320303124/aqstarted.png?width=1442&height=481",
                description="Time to join Alliance Quest."
            )
            await channel.send(content=role.mention, allowed_mentions=discord.AllowedMentions(roles=True), embed=embed)
        else:
            embed = Embed.create(
                self, ctx, title='Alliance Quest has STARTED!',
                image="https://media.discordapp.net/attachments/758775890954944572/779045288320303124/aqstarted.png?width=1442&height=481",
                description="Time to join Alliance Quest."
            )
            await ctx.send(embed=embed)

    @aa.command(aliases=["aqg"])
    async def aqglory(self, ctx):
        """Alerts for glory collection."""
        role = ctx.guild.get_role(await self.config.guild(ctx.guild).get_raw("role"))
        chan = await self.config.guild(ctx.guild).get_raw("channel")
        channel = ctx.guild.get_channel(chan) if chan is not None\
            else ctx.channel
        if role is not None:
            embed = Embed.create(
                self, ctx, title='GLORY has arrived!',
                image="https://media.discordapp.net/attachments/758775890954944572/779045286517145610/aqglory.png?width=962&height=321",
                description="That feeling of topping up your glory balance..."
            )
            await channel.send(content=role.mention, allowed_mentions=discord.AllowedMentions(roles=True), embed=embed)
        else:
            embed = Embed.create(
                self, ctx, title='GLORY has arrived!',
                image="https://media.discordapp.net/attachments/758775890954944572/779045286517145610/aqglory.png?width=962&height=321",
                description="That feeling of topping up your glory balance..."
            )
            await ctx.send(embed=embed)

    @aa.command(aliases=["awp"])
    async def awplace(self, ctx):
        """Alerts for alliance war placement."""
        role = ctx.guild.get_role(await self.config.guild(ctx.guild).get_raw("role"))
        chan = await self.config.guild(ctx.guild).get_raw("channel")
        channel = ctx.guild.get_channel(chan) if chan is not None\
            else ctx.channel
        if role is not None:
            embed = Embed.create(
                self, ctx, title='Placement Phase has begun...',
                image="https://media.discordapp.net/attachments/758775890954944572/779045289579249694/awplacement.png?width=962&height=321",
                description="Place your defenders, and make sure you know where they're going!"
            )
            await channel.send(content=role.mention, allowed_mentions=discord.AllowedMentions(roles=True), embed=embed)
        else:
            embed = Embed.create(
                self, ctx, title='Placement Phase has begun...',
                image="https://media.discordapp.net/attachments/758775890954944572/779045289579249694/awplacement.png?width=962&height=321",
                description="Place your defenders, and make sure you know where they're going!"
            )
            await ctx.send(embed=embed)

    @aa.command(aliases=["awa"])
    async def awattack(self, ctx):
        """Alerts for alliance war attack."""
        role = ctx.guild.get_role(await self.config.guild(ctx.guild).get_raw("role"))
        chan = await self.config.guild(ctx.guild).get_raw("channel")
        channel = ctx.guild.get_channel(chan) if chan is not None\
            else ctx.channel
        if role is not None:
            embed = Embed.create(
                self, ctx, title='Attack Phase has begun...',
                image="https://media.discordapp.net/attachments/758775890954944572/779045289268871169/awattack.png?width=962&height=321",
                description="It's time to attack your opponent."
            )
            await channel.send(content=role.mention, allowed_mentions=discord.AllowedMentions(roles=True), embed=embed)
        else:
            embed = Embed.create(
                self, ctx, title='Attack Phase has begun...',
                image="https://media.discordapp.net/attachments/758775890954944572/779045289268871169/awattack.png?width=962&height=321",
                description="It's time to attack your opponent."
            )
            await ctx.send(embed=embed)

    @aa.command(aliases=["awv"])
    async def awvictory(self, ctx):
        """Alerts for alliance war victory."""
        role = ctx.guild.get_role(await self.config.guild(ctx.guild).get_raw("role"))
        chan = await self.config.guild(ctx.guild).get_raw("channel")
        channel = ctx.guild.get_channel(chan) if chan is not None\
            else ctx.channel
        if role is not None:
            embed = Embed.create(
                self, ctx, title='<:success:777167188816560168> Alliance War VICTORY',
                image="https://media.discordapp.net/attachments/758775890954944572/779045290237231164/awvictory.png?width=962&height=321",
                description="Give yourselves a pat on the back. Good job."
            )
            await channel.send(content=role.mention, allowed_mentions=discord.AllowedMentions(roles=True), embed=embed)
        else:
            embed = Embed.create(
                self, ctx, title='<:success:777167188816560168> Alliance War VICTORY',
                image="https://media.discordapp.net/attachments/758775890954944572/779045290237231164/awvictory.png?width=962&height=321",
                description="Give yourselves a pat on the back. Good job."
            )
            await ctx.send(embed=embed)

    @aa.command(aliases=["awd"])
    async def awdefeat(self, ctx):
        """Alerts for alliance war defeat."""
        role = ctx.guild.get_role(await self.config.guild(ctx.guild).get_raw("role"))
        chan = await self.config.guild(ctx.guild).get_raw("channel")
        channel = ctx.guild.get_channel(chan) if chan is not None\
            else ctx.channel
        if role is not None:
            embed = Embed.create(
                self, ctx, title='<:error:777117297273077760> Alliance War DEFEAT',
                image="https://media.discordapp.net/attachments/758775890954944572/779045290270261288/awdefeat.png?width=962&height=321",
                description="Unlucky, we'll get 'em next time."
            )
            await channel.send(content=role.mention, allowed_mentions=discord.AllowedMentions(roles=True), embed=embed)
        else:
            embed = Embed.create(
                self, ctx, title='<:error:777117297273077760> Alliance War DEFEAT',
                image="https://media.discordapp.net/attachments/758775890954944572/779045290270261288/awdefeat.png?width=962&height=321",
                description="Unlucky, we'll get 'em next time."
            )
            await ctx.send(embed=embed)

    # This function will remove a lot of unnecessary repetition in the code
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
