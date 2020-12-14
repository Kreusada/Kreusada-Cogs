#Thanks Draper and Preda
import functools
from concurrent.futures._base import as_completed
from concurrent.futures.thread import ThreadPoolExecutor
from typing import List


def rgetattr(obj, attr, *args):
    def _getattr(obj2, attr2):
        return getattr(obj2, attr2, *args)

    return functools.reduce(_getattr, [obj] + attr.split("."))


def threadexec(func, *args) -> List:
    result = []
    with ThreadPoolExecutor(max_workers=1) as executor:
        for future in as_completed(
                [executor.submit(func, *args)]
        ):
            result = future.result()
    return result
