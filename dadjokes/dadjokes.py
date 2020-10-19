import random
from .mdtembed import Embed
import json
import aiohttp
import discord
from redbot.core import commands, checks
from redbot.core.config import Config


class DadJokes(commands.Cog):
    """Random dad jokes from icanhazdadjoke.com"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=949000000949,
            force_registration=True,
        )
        self.channel = self.bot.get_channel('725065939460030575')
        # self.diagnostics = DIAGNOSTICS(self.bot)
        self.dadjoke_images = [
            'https://cdn.discordapp.com/attachments/758775890954944572/767818906151813130/demaratusfull.png`]

    @commands.command(pass_context=True, aliases=('joke', 'dadjokes', 'jokes',))
    async def dadjoke(self, ctx):
        """Gets a random dad joke."""
        author = ctx.message.author
        joke = await self.get_joke()
        data = Embed.create(self, ctx, title='Demaratus Dad Jokes :sparkles:',
                            description=joke)
        data.set_author
        data.set_image(url=random.choice(self.dadjoke_images))
        # if self.channel is None:
        #     self.set_channel()
        # try:
        # await ctx.send(ctx.message.channel, embed=data)

        await ctx.send(embed=data)
        #     await self.diagnostics.log(ctx, self.channel)
        # except:
        #     await self.diagnostics.log(ctx, self.channel, msg=joke)

    async def get_joke(self):
        api = 'https://icanhazdadjoke.com/slack'
        joke = None
        while joke is None:
            async with aiohttp.ClientSession() as session:
                async with session.get(api) as response:
                    result = await response.json()
                    attachments = result['attachments'][0]
                    joke = attachments['text']
        if joke is not None:
            return joke

    def set_channel(self):
        self.channel = self.bot.get_channel('725065939460030575')
        return


def setup(bot):
    n = DadJokes(bot)
    bot.add_cog(n)
