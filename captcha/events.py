# Discord/Red related
import logging

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
                    f"Guild Name & ID: {challenge.guild.name} | {challenge.guild.id}"
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

    # @commands.command(name="testing")
    # @commands.is_owner()
    # async def challenge(self, ctx: commands.Context, member: discord.Member):
    #     """Challenge manually an user.
    #
    #     User will be asked to answer captcha.
    #     If he fail, he won't get reinvited by the bot.
    #     """
    #     try:
    #         await self.challenger(member)
    #     except NonEnabledError:
    #         await ctx.send(error("You must enable Captcha before."))
    #
    # @commands.command()
    # @commands.is_owner()
    # async def cancelcap(self, ctx: commands.Context):
    #     await self.temp(ctx.author)
    #     await ctx.tick()
    #
    # async def challenger(self, member: discord.Member):
    #     self.user_challenge_class[str(member.id)] = challenge = Challenge(member)
    #     await challenge.initialize(self.bot)
    #     initied = await challenge.start_challenge()
    #     if not initied:
    #         return
    #     status = await challenge.looper()
    #     if status:
    #         await challenge.handle_role()
    #     await challenge.cleanup()
    #     del self.user_challenge_class[str(member.id)]
    #
    # async def do_possible_cleanup(self, member: discord.Member):
    #     if str(member.id) in self.user_challenge_class:
    #         class_captcha = self.user_challenge_class[str(member.id)]
    #         await class_captcha.cleanup()
    #
    # async def temp(self, member: discord.Member):
    #     if str(member.id) in self.user_challenge_class:
    #         class_captcha = self.user_challenge_class[str(member.id)]
    #         await class_captcha.cancel_tasks()
