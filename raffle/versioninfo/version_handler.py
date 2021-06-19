import ast
import aiohttp
from typing import Union, Tuple

from .components import RAW_VERSION_PATH, RAW_VERSION_URL

class VersionHandler(object):
    """A raffle version information object used to
    check if the cog is outdated."""

    @classmethod
    def versiongetter(cls, asstr: bool = True) -> Union[str, Tuple[int, ...]]:
        with open(RAW_VERSION_PATH) as f:
            ret = ast.literal_eval(f.readlines()[0].rstrip())
        if asstr:
            return ".".join(str(i) for i in ret)
        return ret

    @classmethod
    async def rawversiongetter(cls, asstr: bool = True) -> Union[str, Tuple[int, ...]]:
        async with aiohttp.request("GET", RAW_VERSION_URL) as res:
            ret = await res.text()
        ret = ast.literal_eval(ret)
        if asstr:
            return ".".join(str(i) for i in ret)
        return ret

    @classmethod
    async def validate(cls) -> bool:
        return cls.versiongetter(int) <= await cls.rawversiongetter()





