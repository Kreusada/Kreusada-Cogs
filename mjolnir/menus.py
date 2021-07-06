# Most of this code belongs to Jojo, which was authored under the MIT license.
# This cog was transferred to Kreusada (12/04/2021)
# https://github.com/Just-Jojo/JojoCogs

import discord
from redbot.vendored.discord.ext import menus


class MjolnirPages(menus.ListPageSource):
    _source: menus.ListPageSource

    def __init__(self, data):
        super().__init__(data, per_page=1)  # Use pagify

    def is_paginating(self):
        return True

    async def format_page(self, menu, page):
        bot = menu.bot
        ctx = menu.ctx
        if ctx.channel.permissions_for(ctx.me).embed_links:
            embed = discord.Embed(
                title=f"{bot.user.name} Menu",
                description=page,
                colour=await ctx.embed_colour(),
            )
            embed.set_footer(text=f"Page {menu.current_page + 1}/{self.get_max_pages()}")
            return embed
        else:
            return page


class MjolnirMenu(menus.MenuPages, inherit_buttons=False):
    def __init__(self, source: menus.ListPageSource, page_start: int = 0, **kwargs):
        self.page_start = page_start
        super().__init__(source=source, **kwargs)

    async def send_initial_message(self, ctx, channel):
        self.current_page = self.page_start
        page = await self._source.get_page(self.page_start)
        kwargs = await self._get_kwargs_from_page(page)
        await channel.send(**kwargs)

    async def show_checked_page(self, page_number: int):
        max_pages = self._source.get_max_pages()
        if max_pages is None or max_pages > page_number >= 0:
            await self.show_page(page_number)
        elif page_number > max_pages:
            await self.show_page(0)
        elif page_number < 0:
            await self.show_page(max_pages - 1)

    def _skip_single_arrows(self):
        max_pages = self._source.get_max_pages()
        if max_pages is None:
            return True
        return max_pages == 1

    def _skip_double_triangle_buttons(self):
        max_pages = self._source.get_max_pages()
        if max_pages is None:
            return True
        return max_pages <= 4

    @menus.button(
        "\N{BLACK LEFT-POINTING DOUBLE TRIANGLE}",
        position=menus.First(0),
        skip_if=_skip_double_triangle_buttons,
    )
    async def go_to_first_page(self, payload):
        await self.show_checked_page(0)

    @menus.button(
        "\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE}",
        position=menus.Last(1),
        skip_if=_skip_double_triangle_buttons,
    )
    async def go_to_last_page(self, payload):
        await self.show_checked_page(self._source.get_max_pages() - 1)

    @menus.button(
        "\N{LEFTWARDS BLACK ARROW}",
        position=menus.First(1),
        skip_if=_skip_single_arrows,
    )
    async def go_to_previous_page(self, payload):
        await self.show_checked_page(self.current_page - 1)

    @menus.button(
        "\N{BLACK RIGHTWARDS ARROW}",
        position=menus.Last(0),
        skip_if=_skip_single_arrows,
    )
    async def go_to_next_page(self, payload):
        await self.show_checked_page(self.current_page + 1)

    @menus.button("\N{CROSS MARK}")
    async def stop_pages(self, payload):
        self.stop()
        await self.message.delete()
