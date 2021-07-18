import json
from pathlib import Path
from typing import Tuple

import aiohttp

RAW_VERSION_PATH = Path(__file__).parent / "info.json"
RAW_VERSION_URL = (
    "https://raw.githubusercontent.com/Kreusada/Kreusada-Cogs/master/raffle/info.json"
)

__all__ = ("VersionHandler",)


class VersionHandler(object):
    """A raffle version information object used to
    check if the cog is outdated."""

    with open(RAW_VERSION_PATH, "r") as f:
        __version__ = tuple(json.load(f)["version"])

    @classmethod
    async def request_raw_version(cls) -> Tuple[int]:
        async with aiohttp.request("GET", RAW_VERSION_URL) as res:
            ret = await res.text()
        return tuple(json.loads(ret)["version"])

    @classmethod
    async def validate(cls) -> bool:
        raw_version = await cls.request_raw_version()
        return cls.__version__ > raw_version

    @classmethod
    def tuple_to_str(cls, v) -> str:
        return ".".join(str(x) for x in v)
