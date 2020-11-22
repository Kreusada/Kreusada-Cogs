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
        self.dadjoke_images = ['https://cdn.discordapp.com/attachments/758775890954944572/767820109128400937/demaratusfull.png']

    @commands.command(pass_context=True, aliases=('joke', 'dadjokes', 'jokes',))
    async def dadjoke(self, ctx):
        """Gets a random dad joke."""
        author = ctx.message.author
        joke = await self.get_joke()
        data = Embed.create(self, ctx, title='Demaratus Dad Jokes :joy:',
                            description=joke)
        image = (f"https://media.discordapp.net/attachments/745608075670585344/770068453502877716/DADJOKES.png?width=1442&height=481")
        data.set_author
        data.set_image(url=image)
        await ctx.send(embed=data)

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
    
    @commands.command()
    async def bubblewrap(self, ctx):
        """Pop some bubble wrap!"""
        data = Embed.create(
            self, ctx, title="Bubblewrap!",
            description=(
                "||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||\n"
                "||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||\n"
                "||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||\n"
                "||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||\n"
                "||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||\n"
                "||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||\n"
            )
        )
        await ctx.send(embed=data)
