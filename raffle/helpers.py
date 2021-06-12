import asyncio
import discord
import yaml

from typing import Union, Literal
from yaml.parser import MarkedYAMLError

from redbot.core.bot import Red as RedBot
from redbot.core.commands import Context, BadArgument
from redbot.core.utils.chat_formatting import box

from .safety import RaffleSafeMember
from .enums import RaffleEMC, RaffleJMC
from .formatting import curl, formatenum, cross


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


def raffle_safe_member_scanner(content: str, cond: Literal["join_message", "end_message"]) -> None:
    """We need this to check if the values are formatted properly."""
    kwargs = {
        "raffle": r"{raffle}"
    }
    if cond == "join_message":
        kwargs["user"] = RaffleSafeMember(discord.Member)
        kwargs["entry_count"] = r"{entry_count}"
    else:
        kwargs["winner"] = RaffleSafeMember(discord.Member)
    try:
        # This can raise BadArgument, that's fine
        content.format(**kwargs)
    except KeyError as e:
        raise BadArgument(f"{e} was an unexpected argument in your new {cond.split('_')[0]} message")


async def start_interactive_message_session(
    ctx: Context, bot: RedBot, 
    sesstype: Literal["join_message", "end_message"], message: discord.Message
):
    if sesstype == "join_message":
        when_phrase = "When a user is drawn"
        ENUM = RaffleJMC
    else:
        when_phrase = "When a user enters the raffle"
        ENUM = RaffleEMC
    guide = (
        f"Start adding some messages to add to the list of {sesstype.split('_')[0]} messages.\n"
        f"{when_phrase}, one of these messages will be randomly selected.\n\n"
        "**Available variables:**"
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
    tostop = lambda x: f"{x}\n> Type **stop()** or **exit()** to discontinue gathering messages."
    bubble = lambda x: "{} {}".format("\N{RIGHT ANGER BUBBLE}\N{VARIATION SELECTOR-16}", x)
    while True:
        if not messages:
            await ctx.send(tostop(bubble("Add your first response.")))
        elif len(messages) > 20:
            await ctx.send(F"Sorry, 20 is the maximum limit for the number of {sesstype} messages.")
            break
        else:
            await ctx.send(tostop(bubble("Add another random response:")))
        try:
            message = await bot.wait_for("message", check=check, timeout=100)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to continue, aborted session.")
            return False
        if message.content.lower() in ("exit()", "stop()"):
            if messages:
                break
            return False 
        try:
            raffle_safe_member_scanner(message.content, sesstype)
        except BadArgument:
            await ctx.send(cross("That message's variables were not formatted correctly, skipping..."))
            continue
        messages.append(message.content)
    return messages
