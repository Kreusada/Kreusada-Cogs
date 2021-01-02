from redbot.core import commands, Config
from redbot.core.utils.predicates import ReactionPredicate
from redbot.core.utils.menus import start_adding_reactions
import discord

class WalleStacker(commands.Cog):
    """How much WALL-E trash can we stack?"""

    def __init__(self, bot):
        self.bot = bot
        self.emojis = self.bot.loop.create_task(self.init())
        self.config = Config.get_conf(self, 95873453487, force_registration=True)
        self.config.register_user(
            stack = 0
        )
        self.config.register_guild(
            stack = 0
        )
        self.config.register_global(
            stack = 0
        )

    def cog_unload(self):
        if self.emojis:
            self.emojis.cancel()

    async def red_delete_data_for_user(self, **kwargs):
        """
        Nothing to delete
        """
        return

    async def init(self):
        await self.bot.wait_until_ready()
        self.stackems = {
            "stack": discord.utils.get(self.bot.emojis, id=794141784577802250),
            "stackboard": discord.utils.get(self.bot.emojis, id=791308063935168522)
        }

# Thanks for this logic above, Flare!

    @commands.command()
    @commands.cooldown(1, 50, commands.BucketType.user)
    async def stack(self, ctx):
        """Stack WALL-E trash!"""
        stackglob = await self.config.stack()
        stackuser = await self.config.user(ctx.author).stack()
        stackguild = await self.config.guild(ctx.guild).stack()
        stackglob += 1
        stackuser += 1
        stackguild += 1
        await self.config.stack.set(stackglob)
        await self.config.user(ctx.author).stack.set(stackuser)
        await self.config.guild(ctx.guild).stack.set(stackguild)
        await ctx.send(
            f"{ctx.author.name} contributes towards the trash stack. {self.stackems['stack']}"
            f"\nYou can see the StackBoard by using `{ctx.clean_prefix}stackboard`."
            )

    @commands.command()
    async def stackboard(self, ctx):
        """View the stackboard."""
        glob = await self.config.stack()
        user = await self.config.user(ctx.author).stack()
        guild = await self.config.guild(ctx.guild).stack()
        embed = discord.Embed(title=f"WALL-E StackBoard {self.stackems['stackboard']}", color=0xf56060)
        embed.add_field(name="Global Stacks", value=glob, inline=False)
        embed.add_field(name="Guild Stacks", value=guild, inline=False)
        embed.add_field(name="Your contributions", value=user, inline=False)
        embed.set_footer(text="♻️ | Stackers")
        await ctx.send(embed=embed)

    @commands.group()
    async def stackset(self, ctx):
        """Settings for Stackers."""

    @stackset.command()
    @commands.is_owner()
    async def resetglobal(self, ctx):
        """Reset your global stack."""
        pred = await self.predicate(ctx, "global")
        if pred is True:
            await self.config.stack.clear()
        else:
            pass

    @stackset.command()
    @commands.guildowner()
    @commands.admin_or_permissions(administrator=True)
    async def resetguild(self, ctx):
        """Reset your guild's stack."""
        pred = await self.predicate(ctx, "guild")
        if pred is True:
            await self.config.guild(ctx.guild).stack.clear()
        else:
            pass

    @stackset.command()
    async def resetself(self, ctx):
        """Reset your personal count."""
        pred = await self.predicate(ctx, "user")
        if pred is True:
            await self.config.user(ctx.author).stack.clear()
        else:
            pass

    async def predicate(self, ctx: commands.Context, type: str) -> bool:
        msg = await ctx.send(f"Are you sure you would like to reset the {type} stack?")
        pred = ReactionPredicate.yes_or_no(msg, ctx.author)
        start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)
        if type == 'global':
            count = await self.config.stack()
            set = "Your bot's global"
        elif type == 'guild':
            count = await self.config.guild(ctx.guild).stack()
            set = f"{ctx.guild.name.title()}'s"
        else:
            count = await self.config.user(ctx.author).stack()
            set = 'Your personal'
        try:
            await self.bot.wait_for("reaction_add", check=pred, timeout=30)
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send("You took too long to respond.")
            return False
        if not pred.result:
            await msg.delete()
            await ctx.send(f"Okay. {set} stack remains at {count}.")
            return False
        else:
            await msg.delete()
            await ctx.send(f"Okay. {set.capitalize()} stack has been reset.")
            return True
