from redbot.core import commands

from .abc import MixinMeta


class ConfigManager(MixinMeta):
    pass

    @commands.group()
    async def ctoolset(self, ctx):
        """Settings with channeltools."""

    @ctoolset.command()
    async def topchatters(self, ctx):
        """Toggle whether `[p]channelinfo` displays
        the most chatterful users.
        """
        config = await self._channel_info_chat_settings(ctx)
        if not config:
            await self.config.guild(ctx.guild).topchatters.set(True)
            await ctx.send("Enabled.")
        else:
            await self.config.guild(ctx.guild).topchatters.set(False)
            await ctx.send("Disabled.")
