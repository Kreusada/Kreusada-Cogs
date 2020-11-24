import discord
import requests
from validator_collection import validators

UNSUCRESP = [
SUCRESP = [


class Embed:
    def __init__(self, bot):
        self.bot = bot

    def create(self, ctx, color=discord.Color.red(), title='', description='', image=None,
               thumbnail=None, url=None, footer_text=None, footer_url=None, author_text=None):
        
        DEMARATUS = 'https://cdn.discordapp.com/attachments/769165401879478302/780802976205635634/vanguardskeindem1.png'
        if isinstance(ctx.message.channel, discord.abc.GuildChannel):
            color = ctx.message.author.color
        data = discord.Embed(color=color, title=title, url=url)
        if description is not None:
            if len(description) < 1500:
                data.description = description
        data.set_author(name=ctx.message.author.display_name,
                        icon_url=ctx.message.author.avatar_url)
        if image is not None:
            validators.url(image)
            code = requests.get(image).status_code
            if code == 200:
                data.set_image(url=image)
            else:
                print('Image URL Failure, code {}'.format(code))
                print('Attempted URL:\n{}'.format(image))
        if footer_text is None:
            footer_text = "Demaratus | Higher or Lower"
        if footer_url is None:
            footer_url = DEMARATUS
        data.set_footer(text=footer_text, icon_url=footer_url)
        return data
