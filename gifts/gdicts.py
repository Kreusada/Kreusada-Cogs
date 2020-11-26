import discord
import requests
from validator_collection import validators

class Embed:
    def __init__(self, bot):
        self.bot = bot

    def create(self, ctx, color=discord.Color.red(), title='', description='', image=None,
               thumbnail=None, url=None, footer_text=None, footer_url=None, author_text=None):
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
            footer_text = "Gifts"
        data.set_footer(text=footer_text)
        return data

COLLS = [
  "Wow, look at all these beautiful gifts!",
  "Consider yourself lucky!"
  "These are your gifts? May I have some? :pleading_face:"
]

COLLN = [
  "Oh no! No gifts?! This is a tragedy.",
  "Get yourself some free gifts!"
  "This is not a nice vibe. Where are those gifts!"
]

GIFTS = {
  "a sock": "https://lh3.googleusercontent.com/proxy/LE92TgJSMnQoLad6P0q20KGR0hZf9Ouo6VCOGwNPn5OkJdWQESBe943oRsQzVBUs-C-l34wJLkSBFfzZmlI3s2POJN8U7B3CnE3DXSAikGWKihuKEi5d",
  "a cookie": "https://assets.stickpng.com/images/580b57fbd9996e24bc43c0fc.png"
}
