import asyncio
from typing import List, Literal, Union

import discord
import yaml
from redbot.core.bot import Red as RedBot
from redbot.core.commands import Context
from redbot.core.i18n import Translator
from redbot.core.utils.chat_formatting import box
from redbot.core.utils.menus import DEFAULT_CONTROLS, close_menu, menu
from yaml.parser import MarkedYAMLError

from .checks import now
from .enums import RaffleEndMessageComponents, RaffleJoinMessageComponents
from .exceptions import InvalidArgument, RaffleError
from .formatting import cross, curl, formatenum
from .safety import RaffleSafeMember

_ = Translator("Raffle", __file__)


listumerate = lambda *args: list(enumerate(*args))


def format_traceback(exc) -> str:
    boxit = lambda x, y: box(f"{x}: {y}", lang="yaml")
    return boxit(exc.__class__.__name__, exc)


def cleanup_code(content) -> str:
    # From redbot.core.dev_commands, thanks will :P
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:-1])
    return content.strip("` \n")


def validator(data) -> Union[bool, dict]:
    try:
        loader = yaml.full_load(data)
    except MarkedYAMLError:
        return False
    if not isinstance(loader, dict):
        return False
    return loader


def getstrftime(perc: str) -> Union[str, int]:
    return now.strftime(f"%{perc}")


def number_suffix(number: int) -> str:
    suffixes = {0: "th", 1: "st", 2: "nd", 3: "rd"}
    for i in range(4, 10):
        suffixes[i] = "th"
    return str(number) + suffixes[int(str(number)[-1])]


def yield_sectors(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


def has_badge(badge: str, author: discord.Member):
    badge_data = {k: v for k, v in list(author.public_flags)}
    return badge_data[badge]


def format_underscored_text(text: str):
    return text.replace("_", " ").title()


def revert_underscored_text(text: str):
    return text.replace(" ", "_").lower()


async def compose_menu(ctx, embed_pages: List[discord.Embed]):
    if len(embed_pages) == 1:
        control = {"\N{CROSS MARK}": close_menu}
    else:
        control = DEFAULT_CONTROLS
    return await menu(ctx, embed_pages, control)


def raffle_safe_member_scanner(content: str, cond: Literal["join_message", "end_message"]) -> None:
    """We need this to check if the values are formatted properly."""
    kwargs = {"raffle": r"{raffle}"}
    if cond == "join_message":
        kwargs["user"] = RaffleSafeMember(member=discord.Member, obj="user")
        kwargs["entry_count"] = r"{entry_count}"
    else:
        kwargs["winner"] = RaffleSafeMember(member=discord.Member, obj="winner")
    condition = cond.split("_")[0] + " message"
    try:
        content.format(**kwargs)
    except AttributeError:
        raise InvalidArgument(f"Please only use top level attributes in your {condition}")
    except TypeError:
        raise InvalidArgument(
            "Please define an attribute with {winner}, do not use it alone ({condition})".format(
                winner=r"{winner}", condition=condition
            )
        )
    except KeyError as e:
        raise InvalidArgument(
            "{e} was an unexpected argument in your new {cond} message".format(e=e, cond=condition)
        )


async def start_interactive_message_session(
    ctx: Context,
    bot: RedBot,
    sesstype: Literal["join_message", "end_message"],
    message: discord.Message,
):
    if sesstype == "join_message":
        when_phrase = _("When a user is drawn")
        ENUM = RaffleJoinMessageComponents
    else:
        when_phrase = _("When a user enters the raffle")
        ENUM = RaffleEndMessageComponents

    guide = _(
        "Start adding some messages to add to the list of {sesstype} messages.\n"
        "{when_phrase}, one of these messages will be randomly selected.\n\n"
        "**Available variables:**".format(sesstype=sesstype.split("_")[0], when_phrase=when_phrase)
    )

    b = lambda x: box(x, lang="yaml")
    guide += b(
        "\n".join(
            f"{curl(formatenum(u.name))}: {u.value}"
            for u in sorted(ENUM, key=lambda x: len(x.name))
        )
    )
    try:
        await message.edit(content=guide)
        await message.clear_reactions()
    except discord.HTTPException:
        await ctx.send(guide)

    messages = []

    check = lambda x: x.channel == ctx.channel and x.author == ctx.author
    tostop = lambda x: f"{x}\n> " + _(
        "Type {stop} or {exit} to discontinue gathering messages.".format(
            stop="**stop()**", exit="**exit()**"
        )
    )
    bubble = lambda x: "{} {}".format("\N{RIGHT ANGER BUBBLE}\N{VARIATION SELECTOR-16}", x)
    while True:
        if not messages:
            await ctx.send(tostop(bubble(_("Add your first response."))))
        elif len(messages) > 20:
            await ctx.send(
                _(
                    "Sorry, 20 is the maximum limit for the number of {sesstype} messages.".format(
                        sesstype=sesstype
                    )
                )
            )
            break
        else:
            await ctx.send(tostop(bubble(_("Add another random response:"))))
        try:
            message = await bot.wait_for("message", check=check, timeout=100)
        except asyncio.TimeoutError:
            await ctx.send(_("You took too long to continue, aborted session."))
            return False
        if message.content.lower() in ("exit()", "stop()"):
            if messages:
                break
            return False
        try:
            raffle_safe_member_scanner(message.content, sesstype)
        except InvalidArgument:
            await ctx.send(
                cross(_("That message's variables were not formatted correctly, skipping..."))
            )
            continue
        messages.append(message.content)
    return messages
