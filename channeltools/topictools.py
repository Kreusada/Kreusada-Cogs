import discord

from redbot.core import commands
from redbot.core.utils.chat_formatting import box, italics

from .abc import MixinMeta


class TopicTools(MixinMeta):
    """
    Tools for editing, creating, and reviewing channel topics.
    """

    @commands.group()
    async def topic(self, ctx):
        """
        Tools for editing, creating, and reviewing channel topics.
        """
        pass

    @topic.command()
    async def edit(self, ctx, channel: discord.TextChannel, *, new_topic: str):
        """Edit the channel topic of a channel.
        
        WARNING: Do not overuse, or you could become ratelimited."""
        if not channel.permissions_for(ctx.me).manage_channels:
            return await ctx.send("I need to be able to edit channels.")
        if len(new_topic) > 1024:
            return await ctx.send("The text limit caps at 1024.")
        await self.bot.get_channel(channel.id).edit(topic=new_topic)
        await ctx.send(f"Topic for {channel.mention} successfully changed.")

    @topic.command()
    async def show(self, ctx, channel: discord.TextChannel = None):
        """Show the channel topic of a channel."""
        if not channel:
            channel = ctx.channel
        if not channel.topic:
            topic = italics("No topic was provided.")
        else:
            topic = channel.topic
        await ctx.send(
            embed=await self.embed_builder(
                ctx,
                title=f"#{channel.name} topic",
                description=topic,
            )
        )

    @topic.command()
    async def missing(self, ctx, channel: discord.TextChannel = None):
        """Get channels with missing channel topics."""
        missing_channel_mentions = "\n".join([f'-\t#{c.name}' for c in ctx.guild.text_channels if not c.topic])
        percentage = round((len([c for c in ctx.guild.text_channels if not c.topic])/len(ctx.guild.text_channels)) * 100)
        with_topics = len([c for c in ctx.guild.text_channels if c.topic])
        without_topics = len([c for c in ctx.guild.text_channels if not c.topic])
        pre_processed_stats = (
            f"Percentage of channels without topics: {percentage}%\n"
            f"Channels with topics: {with_topics}\n"
            f"Channels without topics: {without_topics}"
        )
        output = box(pre_processed_stats, lang="yaml") + box(missing_channel_mentions, lang="diff")
        await ctx.send(
            embed=await self.embed_builder(
                ctx,
                title=f"Missing Topic Information",
                description=output,
            )
        )