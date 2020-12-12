import discord
import requests
import asyncio
from datetime import datetime, timedelta
from validator_collection import validators
from datetime import datetime
from redbot.core import commands, checks, Config, modlog


class Staff(commands.Cog):
    """Cog for alerting Staff."""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(
            self, 200730042020, force_registration=True)
        default_guild = {
            "role": None,
            "channel": None
        }
        self.config.register_guild(**default_guild)

    @commands.group()
    async def staffset(self, ctx):
        """Staff notifier configuration."""

    @staffset.command()
    @checks.admin_or_permissions(manage_guild=True)
    async def channel(self, ctx, channel: discord.TextChannel):
        """Sets the channel for staff to receive notifications."""
        await self.config.guild(ctx.guild).set_raw("channel", value=channel.id)
        embed = Embed.create(
            self, ctx, title="Successful <:success:777167188816560168>",
            description=f"{channel.mention} will now receive notifications from users to notify the staff."
        )
        await ctx.send(embed=embed)

    @staffset.command()
    @checks.admin_or_permissions(manage_guild=True)
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
        return
    
    @staffset.command()
    @checks.admin_or_permissions(manage_guild=True)
    async def factoryreset(self, ctx: commands.Context):
        """Resets the full staff configuration."""
        role = await self.config.guild(ctx.guild).get_raw("channel")
        channel = await self.config.guild(ctx.guild).get_raw("channel")
        if role is not None and channel is not None:
            await self.removal(ctx, "role", "channel")
        elif role is None and channel is not None:
            await self.removal(ctx, "channel")
        elif role is not None and channel is None:
            await self.removal(ctx, "role")
        else:
            await ctx.send("Something went wrong.")
        
    @commands.command()
   # @commands.cooldown(1, 600, commands.BucketType.user)
    async def staff(self, ctx):
        """Notifies the staff."""
        message = ctx.message
        await message.add_reaction("✅")
        await asyncio.sleep(1)
        await ctx.send("**:warning: We have sent a report to the staff team. They will be with you as soon as possible.**")
        
        role = ctx.guild.get_role(await self.config.guild(ctx.guild).get_raw("role"))
        chan = await self.config.guild(ctx.guild).get_raw("channel")
        channel = ctx.guild.get_channel(chan) if chan is not None\
            else ctx.channel
        bot = self.bot
        jumper_link = ctx.message.jump_url
        author_id = ctx.author.id
        msgtime = f"**Occurance at:** {datetime.now()}"
        authid = f"\n**Author ID:** {author_id}"
        chfmi = "Click here for more information"
        call = " has just called for the staff in "
        jumper_f = "\n\n**[{}]({})**".format(chfmi, jumper_link)
        if channel is not None:
            embed = Embed.create(
                self, ctx, title=":warning: ALERT!",
                description=f"**{ctx.author.name}**{call}{ctx.channel.mention}.{authid}{msgtime}{jumper_f}",
                footer_text=f"{bot.user.name} | Staff",
                footer_url=f"{bot.user.avatar_url}"
            )
            await channel.send(content=f":warning: {role.mention}", allowed_mentions=discord.AllowedMentions(roles=True), embed=embed, delete_after=43200)
        else:
            embed = Embed.create(
                self, ctx, title=":x: The Staff team have not completed the command setup.",
                description="This is a requirement for the staff command to function.\n"
            )
            await ctx.send(embed=embed)

class Embed:
    def __init__(self, bot):
        self.bot = bot

    def create(self, ctx, color=discord.Color.red(), title='', description='', image=None,
               thumbnail=None, url=None, footer_text=None, footer_url=None, author_text=None):
        if isinstance(ctx.message.channel, discord.abc.GuildChannel):
            color = 0xe15d59
        data = discord.Embed(color=color, title=title, url=url)
        if description is not None:
            if len(description) < 1500:
                data.description = description
        if image is not None:
            data.set_image(url=image)
        if thumbnail is not None:
            data.set_thumbnail(url=thumbnail)
        if footer_text is None:
            footer_text = "Staff"

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
