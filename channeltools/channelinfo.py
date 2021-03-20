import discord

from redbot.core import commands
from redbot.core.utils.chat_formatting import bold

from .abc import MixinMeta

def indent(text):
    if isinstance(text, (list, tuple)):
        return ["  {}".format(t) for t in text]
    return "  {}".format(text)

class ChannelInfo(MixinMeta):
    pass

    @commands.command()
    async def channelinfo(self, ctx, channel: discord.TextChannel = None):
        """Get information about a channel."""
        if not channel:
            channel = ctx.channel
        c = channel

        compose = (
            f"{bold('Channel name:')} {c.name}\n"
            f"{bold('Channel ID:')} {c.id}\n\n"
            f"{bold('Category name:')} {c.category}\n"
            f"{bold('Category ID:')} {c.category.id}\n"
            f"{bold('Creation date:')} {c.created_at.strftime('%d %B %Y, at %H:%M')}\n\n"
            f"{bold('Pins:')} {len(await c.pins())}\n"
            f"{bold('Members:')} {len(c.members)}\n"
            f"{bold('NSFW:')} {c.is_nsfw()}\n"
            f"{bold('News:')} {c.is_news()}\n"
        )

        embed = await self.embed_builder(
            ctx,
            title=f"Channel information for #{channel.name}",
            description=compose
        )

        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.set_image(url=ctx.guild.banner_url)

        await ctx.send(embed=embed)