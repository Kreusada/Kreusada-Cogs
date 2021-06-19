import ast
import aiohttp
import json

from pathlib import Path
from typing import Union, Tuple

RAW_VERSION_PATH = Path(__file__).parent.parent / "info.json"
RAW_VERSION_URL = "https://raw.githubusercontent.com/Kreusada/Kreusada-Cogs/master/raffle/info.json"


class VersionHandler(object):
    """A raffle version information object used to
    check if the cog is outdated."""

    with open(RAW_VERSION_PATH, "r") as f:
        __version__ = json.load(f)["version"]

    @classmethod
    def versiongetter(cls, asstr: bool = True) -> Union[str, Tuple[int, ...]]:
        if asstr:
            return ".".join(str(i) for i in cls.__version__)
        return cls.__version__

    @classmethod
    async def rawversiongetter(cls, asstr: bool = True) -> Union[str, Tuple[int, ...]]:
        async with aiohttp.request("GET", RAW_VERSION_URL) as res:
            ret = await res.text()
        ret = json.loads(ret)["version"]
        if asstr:
            return ".".join(str(i) for i in ret)
        return tuple(ret)

    @classmethod
    async def validate(cls) -> bool:
        return cls.versiongetter(int) <= await cls.rawversiongetter()





