import discord
from datetime import datetime, timedelta
from redbot.core import commands, Config


class ModMail(commands.Cog):
    """This cog allows you to see any dms your bot receives"""

    default_global = {
        "Channel": None
    }

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(
            self, 12386760762, force_registration=True)
        self.config.register_global(**self.default_global)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not isinstance(message.channel, discord.DMChannel):
            return
        if message.author.bot:
            return
        app = await self.bot.application_info()
        if message.author.id == app.owner.id:
            return
        channel = self.bot.get_channel(await self.config.get_raw("Channel"))
        if not message.content[0] in await self.bot.get_prefix(message) and channel is not None:
            embed = discord.Embed(self, message, title="Mod Mail 📬", description=message.content, color=await ctx.embed_colour(), timestamp=datetime.now())
            await channel.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def modmail(self, ctx, toggle: discord.TextChannel = None):
        """Enable/disable the Mod mail"""

        if toggle is None:
            await ctx.send("Would you like to disable the Mod Mail? (y/n)")
            try:
                msg = await self.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout=30)
                if msg.content[0].lower() == "y":
                    await self.config.set_raw("Channel", value=None)
                    msg = "Successfully removed the Mod Mail channel!"
                elif msg.content[0].lower() == "n":
                    msg = "Aborted the removal of the Mod Mail channel"
            except TimeoutError:
                msg = "Canceled the removal of the Mod Mail channel"
            return await ctx.send(msg)
        await self.config.set_raw("Channel", value=toggle.id)
        await ctx.send("Channel changed to {}".format(toggle.mention))
