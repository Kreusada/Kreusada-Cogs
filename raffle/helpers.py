import discord
import yaml

from typing import Union
from yaml.parser import MarkedYAMLError

from redbot.core.commands import Context, BadArgument
from redbot.core.utils.chat_formatting import box

from .safety import RaffleSafeMember


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


def raffle_safe_member_scanner(ctx: Context, content: str) -> None:
    """We need this to check if the values are formatted properly."""
    try:
        # This can raise BadArgument, that's fine
        content.format(winner=RaffleSafeMember(discord.Member), raffle=r"{raffle}")
    except KeyError as e:
        raise BadArgument(f"{e} was an unexpected argument in your new end message")