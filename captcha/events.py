# Discord/Red related
import logging, discord

# Local
from abc import ABCMeta
from traceback import format_exception

from discord import Member
from redbot.core import commands
from redbot.core.utils.chat_formatting import bold

from .abc import MixinMeta

log = logging.getLogger("red.predeactor.captcha")


class Listeners(MixinMeta, metaclass=ABCMeta):
    async def runner(self, member: Member):
        allowed = await self.basic_check(member)
        if allowed:
            challenge = await self.create_challenge_for(member)
            # noinspection PyBroadException
            try:
                await self.realize_challenge(challenge)
            except Exception as e:
                log.critical(
                    f"An unexpected error happened!\n"
                    f"Guild Name & ID: {challenge.guild.name} | {challenge.guild.id}\n"
                    f"Error: {format_exception(type(e), e, e.__traceback__)}"
                )
            finally:
                await self.delete_challenge_for(member)

    async def cleaner(self, member: Member):
        try:
            challenge = self.obtain_challenge(member)
        except KeyError:
            return
        try:
            await challenge.cleanup_messages()
            await self.send_or_update_log_message(
                challenge.guild,
                bold("User has left the server."),
                challenge.messages["logs"],
                member=challenge.member,
            )
        except Exception as e:
            log.critical(
                f"An unexpected error happened!\n"
                f"Guild Name & ID: {challenge.guild.name} | {challenge.guild.id}"
                f"Error: {format_exception(type(e), e, e.__traceback__)}"
            )
        finally:
            await self.delete_challenge_for(member)

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        await self.runner(member)

    @commands.Cog.listener()
    async def on_member_remove(self, member: Member):
        await self.cleaner(member)
        
    @commands.is_owner()
    @commands.command()
    async def captcha(self, ctx, *members: discord.Member):
        """Start a captcha challenge for the specified user"""
        await ctx.send("The challenge has been launched for all members of the server specified in the command.\n"+"```"+ctx.message.content+"```")
        time = await self.data.guild(ctx.guild).timeout()
        await self.data.guild(ctx.guild).timeout.set(20)
        for i in members:
            await self.runner(i)
        await self.data.guild(ctx.guild).timeout.set(time)
        await ctx.send("The challenge is over for all the users specified in the command. This does not mean that all users were not bots and therefore are still there.\n"+"```"+ctx.message.content+"```")
