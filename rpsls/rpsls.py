# Made for TW on Discord
import contextlib
import enum
import json
import random
from pathlib import Path
from typing import Dict, List, Tuple

from redbot.core import commands
from redbot.core.commands import BadArgument, Context, Converter
from redbot.core.utils.chat_formatting import bold, humanize_list, italics


with open(Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


DIAGRAM = "https://static.wikia.nocookie.net/bigbangtheory/images/7/7d/RPSLS.png/revision/latest?cb=20120822205915"

class RPSLSEnum(enum.Enum):
    SCISSORS = "\N{BLACK SCISSORS}\N{VARIATION SELECTOR-16}"
    PAPER = "\N{PAGE FACING UP}"
    ROCK = "\N{MOYAI}"
    LIZARD = "\N{LIZARD}"
    SPOCK = "\N{RAISED HAND WITH PART BETWEEN MIDDLE AND RING FINGERS}"


class ValidChoiceConverter(Converter):
    async def convert(self, ctx: Context, argument: str):
        argument = argument.lower()
        if argument == "help":
            raise BadArgument(DIAGRAM)
        valid_args = [e.name.lower() for e in RPSLSEnum]
        if not argument in valid_args:
            raise BadArgument(
                "Choice must be one of {}. You can also use "
                "`{}rpsls help` for a help diagram.".format(
                    humanize_list(valid_args, style="or"), ctx.clean_prefix
                )
            )
        mapper = {v: c for c, v in enumerate(valid_args, start=1)}
        return argument, mapper[argument]


class _IntMapper(object):
    intmapper: Dict[int, List[int]] = {}

    def __getitem__(self, item):
        m = {}
        for i in range(1, 6):
            if i <= 2:
                m[i] = [i + 1, i + 3]
            elif 5 > i >= 3:
                m[i] = [i + 1, i - 2]
            else:
                m[i] = [i // i, i - 2]
        self.intmapper.update(m)
        return self.intmapper[item]


IntMapper = _IntMapper()
VS = "\N{SQUARED VS}"


def get_emoji_from_name(name) -> str:
    return {e.name.lower(): e.value for e in RPSLSEnum}[name]


def generate_bot_rpsls() -> Tuple[str, int]:
    ret = {v: c for c, v in enumerate([e.name.lower() for e in RPSLSEnum], 1)}
    return random.choice(list(ret.items()))


class RPSLS(commands.Cog):
    """Rock, paper, scizzors, lizard, spock."""

    __author__ = "Kreusada"
    __version__ = "2.1.1"

    def __init__(self, bot):
        self.bot = bot
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(RuntimeError, ValueError):
                self.bot.add_dev_env_value(self.__class__.__name__.lower(), lambda x: self)

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    def cog_unload(self):
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(KeyError):
                self.bot.remove_dev_env_value(self.__class__.__name__.lower())

    @commands.command()
    async def rpsls(self, ctx, choice: ValidChoiceConverter):
        """Play rock, paper, scizzors, lizard, spock.

        Use `[p]rpsls help` for a diagram.
        """
        human_choice, human_number = choice
        bot_choice, bot_number = generate_bot_rpsls()
        if bot_number == human_number:
            phrase = italics("It's a draw! We're fair and square.")
            bot_user = self.bot.user
            human_user = ctx.author
        elif bot_number in IntMapper[human_number]:
            phrase = italics("You won - nice job!")
            bot_user = self.bot.user
            human_user = bold(str(ctx.author))
        else:
            phrase = italics("Damn, better luck next time...")
            bot_user = bold(str(self.bot.user))
            human_user = ctx.author
        bot_emoji = get_emoji_from_name(bot_choice)
        human_emoji = get_emoji_from_name(human_choice)
        message = f"{human_user} {human_emoji} {VS} {bot_emoji} {bot_user}" f"\n> {phrase}"
        await ctx.maybe_send_embed(message)
