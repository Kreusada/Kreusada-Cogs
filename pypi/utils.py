import math
from typing import Dict

import discord
from discord.ui import Button, View


class JumpUrlView(View):
    def __init__(self, pypi_url: str, *, project_urls: Dict[str, str]):
        super().__init__()
        button = Button(label="Page on PyPi", url=pypi_url, row=1)
        self.add_item(button)
        for index, (name, url) in enumerate(project_urls.items()):
            self.add_item(Button(label=name, url=url, row=math.floor(index / 3 + 2)))
