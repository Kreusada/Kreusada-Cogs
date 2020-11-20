import discord
import requests


class Embed:
    def __init__(self, bot):
        self.bot = bot

    def create(self, ctx, color=discord.Color.red(), title='', description='', image=None,
               thumbnail=None, url=None, footer_text=None, footer_url=None, author_text=None):
        '''Return a color styled embed with MDT footer, and optional title or description.
        user_id = user id string. If none provided, takes message author.
        color = manual override, otherwise takes gold for private channels, or author color for guild.
        title = String, sets title.
        description = String, sets description.
        image = String url.  Validator checks for valid url.
        thumbnail = String url. Validator checks for valid url.'''
        DEMARATUS = 'https://media.discordapp.net/attachments/758775890954944572/777496867109208094/vanguardskeindem1.png'

        if isinstance(ctx.message.channel, discord.abc.GuildChannel):
            color = ctx.message.author.color
        data = discord.Embed(color=color, title=title, url=url)
        if description is not None:
            if len(description) < 1500:
                data.description = description
        if image is not None:
            data.set_image(url=image)
        if thumbnail is not None:
            data.set_thumbnail(url=thumbnail)
        if footer_text is None:
            footer_text = "Demaratus | Hot Potato"
        if footer_url is None:
            footer_url = DEMARATUS
        data.set_footer(text=footer_text, icon_url=footer_url)
        return data
