import asyncio
import contextlib
import random
import time

import discord
from redbot.core import Config, commands, i18n
from redbot.core.utils.chat_formatting import bold, box


class TimesTables(commands.Cog):
    """
    Learn your times tables with a quick, simple game!

    Includes various ways to customize the difficulty,
    including an 'against the time' challenge.
    """

    __author__ = ["Kreusada"]
    __version__ = "1.1.3"

    def __init__(self, bot):
        self.bot = bot
        self.correct = "\N{WHITE HEAVY CHECK MARK}"
        self.incorrect = "\N{CROSS MARK}"
        self.session_quotes = [
            "Great work",
            "Amazing",
            "Awesome work",
            "Nice stuff",
        ]
        self.how_to_exit_early = (
            "Remember, you can type `exit()` or `stop()` at any time to quit the session."
        )
        self.config = Config.get_conf(self, 2345987543534, force_registration=True)
        self.config.register_guild(tt_inactive=3, tt_timeout=10, tt_sleep=2, tt_time_taken=True)
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("timestables", lambda x: self)

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    def cog_unload(self):
        with contextlib.suppress(Exception):
            self.bot.remove_dev_env_value("timestables")

    async def tt_build_stats(
        self, ctx, correct, incorrect, inactive, average_time, exited_early: bool
    ):
        if not exited_early:
            msg = f"{random.choice(self.session_quotes)} {ctx.author.name}! The session has ended."
        else:
            msg = f"You exited early, {ctx.author.name}."

        if average_time:
            timing = (
                f"\n\nAverage time per question: {self.average(average_time)}s\n"
                f"Total time spent answering: {self.total(average_time)}s"
            )
        else:
            timing = ""

        return await ctx.send(
            box(
                text=(
                    f"{msg}\n\nCorrect: {str(correct)}\n"
                    f"Incorrect: {str(incorrect)}\n"
                    f"Unanswered: {str(inactive)}"
                    f"{timing}"
                ),
                lang="yml",
            )
        )

    @staticmethod
    def time():
        return time.perf_counter()

    @staticmethod
    def total(times):
        return round(sum(times), 2)

    @staticmethod
    def average(times):
        try:
            return round(sum(times) / len(times), 2)
        except ZeroDivisionError:
            return 0

    @commands.group()
    async def tt(self, ctx):
        """Commands for times tables."""
        pass

    @tt.command()
    @commands.guild_only()
    @commands.mod_or_permissions(administrator=True)
    async def inactive(self, ctx, questions: int):
        """
        Set the number of questions unanswered before the session is closed.
        """
        if questions <= 2:
            return await ctx.send("Must be more than 2.")
        elif questions >= 10:
            return await ctx.send("Must be less than 10.")
        await self.config.guild(ctx.guild).tt_inactive.set(questions)
        await ctx.tick()

    @tt.command()
    @commands.guild_only()
    @commands.mod_or_permissions(administrator=True)
    async def timeout(self, ctx, seconds: int):
        """
        Set the number of seconds before a question times out.
        """
        if seconds <= 3:
            return await ctx.send("Must be more than 3.")
        elif seconds >= 50:
            return await ctx.send("Must be less than 50.")
        await self.config.guild(ctx.guild).tt_timeout.set(seconds)
        await ctx.tick()

    @tt.command()
    @commands.guild_only()
    @commands.mod_or_permissions(administrator=True)
    async def sleep(self, ctx, seconds: int):
        """
        Set the number of seconds between each question.
        """
        if seconds >= 8:
            return await ctx.send("Must be less than 8.")
        elif seconds <= 0:
            return await ctx.send("Must be a positive number.")
        await self.config.guild(ctx.guild).tt_timeout.set(seconds)
        await ctx.tick()

    @tt.command()
    @commands.guild_only()
    async def settings(self, ctx):
        """
        Shows the current settings for times tables.
        """
        settings = await self.config.guild(ctx.guild).all()
        time = settings["tt_time_taken"]
        inactive = settings["tt_inactive"]
        timeout = settings["tt_timeout"]
        sleep = settings["tt_sleep"]
        text = (
            f"Time toggled: {'Yes' if time else 'No'}\n"
            f"Inactive count: {inactive} questions\n"
            f"Timeout per question: {timeout}s\n"
            f"Time between questions: {sleep}s"
        )
        if await ctx.embed_requested():
            embed = discord.Embed(
                title=f"Settings for {ctx.guild.name}",
                description=text,
                color=await ctx.embed_colour(),
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(text)

    @tt.command(name="time")
    @commands.guild_only()
    @commands.mod_or_permissions(administrator=True)
    async def _time(self, ctx):
        """
        Toggle whether the command displays the time taken.
        Defaults to False.
        """
        time = await self.config.guild(ctx.guild).tt_time_taken()
        await self.config.guild(ctx.guild).tt_time_taken.set(not time)
        verb = "enabled" if not time else "disabled"
        await ctx.send(f"Time has been {verb}.")

    @tt.command()
    @commands.guild_only()
    async def start(self, ctx, number_of_questions: int):
        """Start a timestables session."""

        settings = await self.config.guild(ctx.guild).all()
        time_taken = settings["tt_time_taken"]
        inactive = settings["tt_inactive"]
        timeout = settings["tt_timeout"]
        sleep = settings["tt_sleep"]

        if number_of_questions > 20:
            return await ctx.send("Sorry, you cannot have more than 20 questions.")
        if number_of_questions < 1:
            return await ctx.send("Sorry, you cannot have less than 1 question.")
        await ctx.send(
            f"Starting timestable session with {number_of_questions} questions...\n{self.how_to_exit_early}"
        )
        await asyncio.sleep(3)

        def check(x):
            return x.author == ctx.author and x.channel == ctx.channel

        correct_answers = 0
        incorrect_answers = 0
        inactive_counter = 0
        average_time = []

        for i in range(number_of_questions):
            F = random.randint(1, 12)
            S = random.randint(1, 12)
            await ctx.send(f"{bold(f'{F} x {S}')}?")

            try:
                if time_taken:
                    time_start = self.time()
                answer = await self.bot.wait_for("message", timeout=timeout, check=check)
            except asyncio.TimeoutError:
                inactive_counter += 1
                if inactive_counter == inactive:
                    return await ctx.send("Session ended due to inactivity.")
                await ctx.send(
                    f"You took too long! Not to worry - the answer was {bold(str(F*S))}."
                )
            else:
                if answer.content == str(F * S):
                    time_end = self.time()
                    await answer.add_reaction(self.correct)
                    if time_taken:
                        await ctx.send(
                            f"{random.choice(self.session_quotes)}! This question took you {round(time_end - time_start,2)} seconds."
                        )
                    correct_answers += 1
                    if time_taken:
                        average_time.append(round(time_end - time_start, 2))
                elif answer.content.lower() in {"exit()", "stop()"}:
                    await ctx.send("Session ended.")
                    return await self.tt_build_stats(
                        ctx,
                        correct_answers,
                        incorrect_answers,
                        inactive_counter,
                        average_time if time_taken else None,
                        True,
                    )
                else:
                    await answer.add_reaction(self.incorrect)
                    await ctx.send(f"Not quite! The answer was {bold(str(F*S))}.")
                    incorrect_answers += 1
                await ctx.trigger_typing()
                await asyncio.sleep(sleep)

        await self.tt_build_stats(
            ctx,
            correct_answers,
            incorrect_answers,
            inactive_counter,
            average_time if time_taken else None,
            False,
        )
