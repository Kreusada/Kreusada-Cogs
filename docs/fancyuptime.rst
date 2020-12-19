.. _fancyuptime:

====================
Cog: FancyUptime
====================

-------
Outline
-------

:code:`FancyUptime` is a cog that allows users to get their bot's uptime inside an embed, with some additional 'fancy' info!
This cog will remove the :code:`uptime` command from your redbot's core, instead replacing it with :code:`FancyUptime`'s :code:`uptime` command.

.. attention:: Not happy with the output from :code:`FancyUptime`? No problem, just unload the cog and you will have the original uptime command back from your redbot core.

------------
Installation
------------

Make sure you have :code:`Downloader` loaded!

:code:`[p]load Downloader`

Let's add Kreusada's repository firstly:

:code:`[p]repo add kreusadacogs https://github.com/kreus7/kreusadacogs`

Now, you can add the :code:`FancyUptime` cog into your system.

:code:`[p]cog install kreusadacogs fancyuptime`

-----
Usage
-----

- :code:`[p]uptime`

Shows your bot's uptime with additional information!

----
Code
----

Here is the code used for :code:`FancyUptime`.

.. code-block:: python

    import discord
    from redbot.core import commands
    
    import discord
    from redbot.core import commands, Config
    from redbot.core.utils import AsyncIter
    from datetime import datetime, timedelta
    from .delta_utils import humanize_timedelta

    class FancyUptime(commands.Cog):
      def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=59465034743, force_registration=True)
       
     def cog_unload(self):
        global _old_uptime
        if _old_uptime:
         try:
            self.bot.remove_command("uptime")
         except Exception as error:
           log.info(error)
          self.bot.add_command(_old_uptime)

      @commands.command()
      async def uptime(self, ctx: commands.Context):
         """Shows [botname]'s uptime."""
          since = ctx.bot.uptime.strftime("%A the %d of %B, %Y")
          delta = datetime.utcnow() - self.bot.uptime
          uptime_str = humanize_timedelta(timedelta=delta) or ("Less than one second")
          bot = ctx.bot.user
          botname = ctx.bot.user.name
          guild = ctx.guild
          users = len(self.bot.users)
          servers = str(len(self.bot.guilds))
          commandsavail = len(set(self.bot.walk_commands()))
          now = datetime.now()
          strftime = now.strftime("Today at %H:%M %p")
          e = discord.Embed(title=f":green_circle:  {botname}'s Uptime",
                            description=(
                             f"**{botname}** has been up since {since}. "
                             f"Therefore, it's been online for {uptime_str}."
                           ),
                            color=0x59e1ac)
          e.add_field(name="Instance name:", value=bot.name, inline=True)
          e.add_field(name="Current guild:", value=guild, inline=True)
          e.add_field(name="Number of guilds:", value=servers, inline=True)
          e.add_field(name="Unique users:", value=users, inline=True)
          e.add_field(name="Commands available:", value=commandsavail, inline=True)
          e.add_field(name="Uptime Invoker:", value=ctx.author.name, inline=True)
          e.set_thumbnail(url=bot.avatar_url)
          e.set_footer(text=f"{strftime}")
          await ctx.send(embed=e)

    async def setup(bot):
      fu = FancyUptime(bot)
      global _old_uptime
      _old_uptime = bot.get_command("uptime")
     if _old_uptime:
         bot.remove_command(_old_uptime.name)
      bot.add_cog(fu)

.. code-block:: python

    import datetime
    import discord
    from typing import Optional, SupportsInt

    def humanize_timedelta(
      *, timedelta: Optional[datetime.timedelta] = None, seconds: Optional[SupportsInt] = None
    ) -> str:

    try:
        obj = seconds if seconds is not None else timedelta.total_seconds()
    except AttributeError:
        raise ValueError("You must provide either a timedelta or a number of seconds")

    seconds = int(obj)
    periods = [
        (("year"), ("years"), 60 * 60 * 24 * 365),
        (("month"), ("months"), 60 * 60 * 24 * 30),
        (("day"), ("days"), 60 * 60 * 24),
        (("hour"), ("hours"), 60 * 60),
        (("minute"), ("minutes"), 60),
        (("second"), ("seconds"), 1),
    ]

    strings = []
    for period_name, plural_period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            if period_value == 0:
                continue
            unit = plural_period_name if period_value > 1 else period_name
            strings.append(f"{period_value} {unit}")

    return ", ".join(strings)

-------
Support
-------

As always, you can join my `support server <https://discord.gg/JmCFyq7>`_ if you need help!

- Kreusada
