import discord
import datetime
import collections

from typing import Union

from redbot.core import commands
from redbot.core.utils.chat_formatting import bold, box

from .abc import MixinMeta


channel_information = "Channel Name: **{0.name}**\nChannel ID: **{0.id}**"

category_information = "\nCategory Name: **{0.name}**\nCategory ID: **{0.id}**"

type_information = "News Channel: **{news}**\nNSFW Channel: **{nsfw}**"

other_information = "Number of pins: **{pins}**\nUsers with read access: **{members}**"

voice_channel_information = "VC Name: **{0.name}**\nVC ID: **{0.id}**"

voice_settings_information = "User Limit: **{limit}**\nBitrate: **{0.bitrate}**"

voice_user_information = (
    "\n\nMuted: **{0.self_mute}**\nDeafened: **{0.self_deaf}**\n" "Streaming: **{0.self_stream}**"
)

def two_digit_number(num):
    if len(str(num)) == 1:
        return '0{}'.format(num)
    return num


class Channel(MixinMeta):
    pass

    @commands.command()
    async def channelinfo(
        self, ctx, channel: Union[discord.TextChannel, discord.VoiceChannel] = None
    ):
        """Get information about a voice or text channel."""
        await ctx.trigger_typing()
        if not channel:
            if ctx.author.voice:
                return await self.get_voice_channel_information(ctx, ctx.author.voice.channel) 
            return await self.get_text_channel_information(ctx, ctx.channel) 
        if isinstance(channel, discord.TextChannel):
            await self.get_text_channel_information(ctx, channel)
        else:
            await self.get_voice_channel_information(ctx, channel)
    
    async def get_text_channel_information(self, ctx, channel):
        if not channel:
            channel = ctx.channel
        c = channel
        created_at = (datetime.datetime.now() - c.created_at).days
        if created_at == 1:
            created_at = f"Created {created_at} day ago."
        elif not created_at:
            created_at = "Created today."
        else:
            created_at = f"Created {created_at} days ago."
        embed = await self.embed_builder(
            ctx,
            title=f"Channel information for #{channel.name}",
            description=created_at,
        )
        value = channel_information.format(c)

        embed.add_field(
            name="Basic Info:",
            value=value,
            inline=False,
        )

        if c.category:
            embed.add_field(
                name="Category Info:",
                value=category_information.format(c.category),
                inline=True,
            )

        value = type_information.format(
            nsfw=c.is_nsfw(),
            news=c.is_news(),
        )

        embed.add_field(
            name="Type",
            value=value,
            inline=False,
        )

        value = other_information.format(pins=len(await c.pins()), members=len(c.members))

        embed.add_field(
            name="Misc:",
            value=value,
            inline=False,
        )
        check = await self._channel_info_chat_settings(ctx)
        if check:
            y = []
            async for x in c.history(limit=200):
                y.append(x.author.id)
            re_formatted = collections.Counter(y).most_common()[:5]
            print(re_formatted)
            value = ""
            if not re_formatted:
                value += "No users have talked here yet!"
            else:
                for x in re_formatted:
                    bot_get_user = self.bot.get_user(x[0])
                    messages = x[1]
                    if not bot_get_user:
                        if x[0] in [x.id for x in await ctx.guild.webhooks()]:
                            get_user = "Webhook"
                        else:
                            get_user = "Unknown"
                    else:
                        get_user = bot_get_user.display_name
                    value += "\n- [{}]({})".format(two_digit_number(messages), get_user)

            embed.add_field(
                name="Top Chatters (last 200):",
                value=box(value, lang='md'),
                inline=False,
            )

        embed.set_author(name=ctx.guild.name)
        embed.set_thumbnail(url=ctx.guild.icon_url)

        await ctx.send(embed=embed)

    async def get_voice_channel_information(self, ctx, voice_channel: discord.VoiceChannel):
        voice = voice_channel
        author = ctx.author
        if voice:
            created_at = (datetime.datetime.now() - voice.created_at).days
        else:
            created_at = (datetime.datetime.now() - author.voice.channel.created_at).days
        if created_at == 1:
            created_at = f"Created {created_at} day ago."
        elif not created_at:
            created_at = "Created today."
        else:
            created_at = f"Created {created_at} days ago."
        embed = await self.embed_builder(
            ctx,
            title="Voice Channel Information",
            description=created_at,
        )
        if not voice:
            value=voice_channel_information.format(author.voice.channel)
        else:
            value=voice_channel_information.format(voice)

        embed.add_field(
            name="Basic Info:",
            value=value,
        )

        value = voice_settings_information.format(
            voice,
            limit=voice.user_limit if voice.user_limit else "Unlimited",
        )

        embed.add_field(
            name="VC Settings:",
            value=value,
            inline=False,
        )

        if author.voice:
            embed.add_field(
                name="User Info:",
                value=voice_user_information.format(author.voice),
                inline=False,
            )
            embed.set_footer(icon_url=author.avatar_url, text=author)
        else:
            if voice.permissions_for(author).connect:
                embed.set_footer(text=f"Join {voice.name} for more info!")
        embed.set_author(name=ctx.guild.name)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)
