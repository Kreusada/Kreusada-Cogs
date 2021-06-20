import asyncio
import discord
import yaml

from typing import Any, Dict, List, Literal, Union
from yaml.parser import MarkedYAMLError

from redbot.core.bot import Red as RedBot
from redbot.core.i18n import Translator
from redbot.core.commands import Context
from redbot.core.utils.chat_formatting import box
from redbot.core.utils.menus import menu, close_menu, DEFAULT_CONTROLS

from .checks import now
from .safety import RaffleSafeMember
from .enums import RaffleEMC, RaffleJMC
from .formatting import curl, formatenum, cross
from .exceptions import InvalidArgument

_ = Translator("Raffle", __file__)

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


def format_dashed_title(data: Dict[str, Any]) -> str:
    return "-" * len(min([f"{k}: {v}" for k, v in data.items()]))


async def compose_menu(ctx: commands.Context, embed_pages: List[discord.Embed]):
    if len(embed_pages) == 1:
        control = {"\N{CROSS MARK}": close_menu}
    else:
        control = DEFAULT_CONTROLS
    return await menu(ctx, embed_pages, control)


def raffle_safe_member_scanner(content: str, cond: Literal["join_message", "end_message"]) -> None:
    """We need this to check if the values are formatted properly."""
    kwargs = {
        "raffle": r"{raffle}"
    }
    if cond == "join_message":
        kwargs["user"] = RaffleSafeMember(member=discord.Member, obj="user")
        kwargs["entry_count"] = r"{entry_count}"
    else:
        kwargs["winner"] = RaffleSafeMember(member=discord.Member, obj="winner")
    try:
        content.format(**kwargs)
    except KeyError as e:
        raise InvalidArgument(
            _(
                "{e} was an unexpected argument in your new {cond} message".format(
                    e=e,
                    cond=cond.split("_")[0]
                )
            )
        )



async def start_interactive_message_session(
    ctx: Context, bot: RedBot, 
    sesstype: Literal["join_message", "end_message"], message: discord.Message
):
    if sesstype == "join_message":
        when_phrase = _("When a user is drawn")
        ENUM = RaffleJMC
    else:
        when_phrase = _("When a user enters the raffle")
        ENUM = RaffleEMC

    guide = _(
        "Start adding some messages to add to the list of {sesstype} messages.\n"
        "{when_phrase}, one of these messages will be randomly selected.\n\n"
        "**Available variables:**".format(
            sesstype=sesstype.split("_")[0],
            when_phrase=when_phrase
        )
    )

    b = lambda x: box(x, lang="yaml")
    guide += b("\n".join(f"{curl(formatenum(u.name))}: {u.value}" for u in sorted(ENUM, key=lambda x: len(x.name))))
    try:
        await message.edit(content=guide)
        await message.clear_reactions()
    except discord.HTTPException:
        await ctx.send(guide)
    
    messages = []

    check = lambda x: x.channel == ctx.channel and x.author == ctx.author
    tostop = lambda x: f"{x}\n> " + _("Type {stop} or {exit} to discontinue gathering messages.".format(stop="**stop()**", exit="**exit()**"))
    bubble = lambda x: "{} {}".format("\N{RIGHT ANGER BUBBLE}\N{VARIATION SELECTOR-16}", x)
    while True:
        if not messages:
            await ctx.send(tostop(bubble(_("Add your first response."))))
        elif len(messages) > 20:
            await ctx.send(_("Sorry, 20 is the maximum limit for the number of {sesstype} messages.".format(sesstype=sesstype)))
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
            await ctx.send(cross(_("That message's variables were not formatted correctly, skipping...")))
            continue
        messages.append(message.content)
    return messages
