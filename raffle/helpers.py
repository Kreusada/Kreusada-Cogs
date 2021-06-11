import asyncio
import discord
import yaml

from typing import Union
from yaml.parser import MarkedYAMLError

from redbot.core.bot import Red as RedBot
from redbot.core.commands import Context, BadArgument
from redbot.core.utils.chat_formatting import box

from .safety import RaffleSafeMember
from .enums import RaffleEMC
from .formatting import curl, formatenum


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


def raffle_safe_member_scanner(content: str) -> None:
    """We need this to check if the values are formatted properly."""
    try:
        # This can raise BadArgument, that's fine
        content.format(winner=RaffleSafeMember(discord.Member), raffle=r"{raffle}")
    except KeyError as e:
        raise BadArgument(f"{e} was an unexpected argument in your new end message")

async def start_interactive_end_message_session(ctx: Context, bot: RedBot, message: discord.Message):
    guide = (
        "Start adding some messages to add to the list of end messages.\n"
        "When a user is drawn, one of these messages will be randomly selected.\n"
        "When you have finished adding messages, **type stop() to discontinue the interactive session.**\n\n"
        "See below for a list of available variables:"
    )
    b = lambda x: box(x, lang="yaml")
    guide += b("\n".join(f"{curl(formatenum(u.name))}: {u.value}" for u in sorted(RaffleEMC, key=lambda x: len(x.name))))
    try:
        await message.edit(content=guide)
        await message.clear_reactions()
    except discord.HTTPException:
        await ctx.send(guide)
    
    messages = []

    check = lambda x: x.channel == ctx.channel and x.author == ctx.author

    while True:
        if not messages:
            await ctx.send("Add your first response:")
        elif len(messages) > 20:
            await ctx.send("That's enough messages!")
            return messages
        else:
            await ctx.send("Add another random response:")
        try:
            message = await bot.wait_for("message", check=check, timeout=40)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to continue, aborted session.")
            return False
        if message.content.lower() == "stop()":
            if messages:
                break
            return False 
        try:
            raffle_safe_member_scanner(message.content)
        except BadArgument:
            await ctx.send("That message's variables were not formatted correctly, skipping...")
            continue
        messages.append(message.content)
    return messages
