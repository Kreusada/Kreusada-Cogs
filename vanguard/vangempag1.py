import discord
import requests


class Embedpag1:
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
#        if url is None:
#            url = PATREON
        data = discord.Embed(color=color, title=title, url=url)
        if description is not None:
            if len(description) < 1500:
                data.description = description
