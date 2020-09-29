import discord
from discord import Embed, Color


class EmbedCreator:
    def __init__(self, client):
        self.client = client

    async def create(self, ctx, title="",
                     description="", color=Color.gold(),
                     footer=None, footer_image=None,
                     thumbnail=None, image=None):
        """Make an Embed as easy as 1, 2, 3
        Args:
            ctx: The context needed to set the author's name and url
            title (str, optional): The Title of the embed. Defaults to "".
            description (str, optional): The Description of the embed. Defaults to "".
            color (discord.Color, optional): Color/Colour of the embed (You need to use discord.Color. to set the color). Defaults to Color.blue().
            footer (optional): Set the footer of the Embed. Defaults to None.
            footer_image (optional): Set the footer icon. Defaults to None.
            thumbnail (optional): Set the thumbnail of the embed. Defaults to None.
            image (optional): Set the embed's image. Defaults to None.
        Returns:
            Embed: A Discord embed object
        """
        if isinstance(ctx.message.channel, discord.abc.GuildChannel):
            color = ctx.message.author.color
        data = Embed(title=title, color=color)
        if description is not None:
            data.description = description
        data.set_author(name=ctx.author.display_name,
                        icon_url=ctx.author.avatar_url)

        if footer is None:
            footer = ctx.author.display_name
        if footer_image is None:
            footer_image = ctx.author.avatar_url
        data.set_footer(text=footer, icon_url=footer_image)

        if image is not None:
            data.set_image(url=image)

        if thumbnail is not None:
            data.set_thumbnail(
                url=thumbnail
            )
        return data
