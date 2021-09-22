"""Private tool to generate docs for cogs."""

import inspect
import os
import pathlib

from redbot.core import commands
from redbot.core.commands import BadArgument, Cog, Command, Context, Converter
from redbot.core.utils.chat_formatting import box


class CogConverter(Converter):
    async def convert(self, ctx: Context, cog: str):
        if not (obj := ctx.bot.get_cog(cog)):
            raise BadArgument("No cog with the name '%s'" % cog)
        return obj


def header(text: str, style: str = "="):
    head = style * len(text)
    return head + "\n" + text + "\n" + head


def format_command(ctx: Context, command: Command):
    base = f"* ``[p]{command.qualified_name}"
    if command.signature:
        base += f" {command.signature}``"
    else:
        base += "``"
    return f"{base}\n {inspect.cleandoc(command.help)}"


class CogGuide(Cog):
    """Private tool to generate docs for cogs."""

    @commands.command()
    async def cogguide(self, ctx: Context, cog: CogConverter):
        cog: commands.Cog = cog
        cog_name = cog.qualified_name
        backslash = "\n"
        message = f"""
.. _{cog_name.lower()}:

{header(cog_name)}

This is the cog guide for the '{cog_name}' cog. This guide
contains the collection of commands which you can use in the cog.

Through this guide, ``[p]`` will always represent your prefix. Replace
``[p]`` with your own prefix when you use these commands in Discord.

.. note::

    This guide was last updated for version {cog.__version__}. Ensure
    that you are up to date by running ``[p]cog update {cog_name.lower()}``.

    If there is something missing, or something that needs improving
    in this documentation, feel free to create an issue `here <https://github.com/Kreusada/Kreusada-Cogs/issues>`_.

    This documentation is auto-generated everytime this cog receives an update.

{header("About this cog", "-")}

{inspect.getdoc(cog)}

{header("Commands", "-")}

Here are all the commands included in this cog ({len(set(cog.walk_commands()))}):

{backslash.join(format_command(ctx, x) for x in sorted(cog.walk_commands(), key=lambda x: x.qualified_name))}

{header("Installation", "-")}

If you haven't added my repo before, lets add it first. We'll call it
"kreusada-cogs" here.

.. code-block:: ini

    [p]repo add kreusada-cogs https://github.com/Kreusada/Kreusada-Cogs

Now, we can install {cog_name}.

.. code-block:: ini

    [p]cog install kreusada-cogs {cog_name.lower()}

Once it's installed, it is not loaded by default. Load it by running the following
command:

.. code-block:: ini

    [p]load {cog_name.lower()}

{header("Further Support", "-")}

For more support, head over to the `cog support server <https://discord.gg/GET4DVk>`_,
I have my own channel over there at #support_kreusada-cogs. Feel free to join my
`personal server <https://discord.gg/JmCFyq7>`_ whilst you're here.
""".lstrip()
        paths = [
            ("docs", f"cog_{cog_name.lower()}.rst"),
            (f"{cog_name.lower()}", "README.rst"),
        ]
        for path in paths:
            cogpath = os.path.join("Desktop", "Github", "Kreusada-Cogs")
            with open(os.path.join(os.environ["USERPROFILE"], cogpath, *path), "w") as fp:
                fp.write(message)
        await ctx.send(
            "Cog guide updated at the following locations:\n"
            + box(
                f"%userprofile%/Desktop/Github/Kreusada-Cogs/{cog_name.lower()}/README.rst\n"
                f"%userprofile%/Desktop/Github/Kreusada-Cogs/docs/cog_{cog_name.lower()}.rst\n",
                lang="autohotkey",
            )
        )


def setup(bot):
    bot.add_cog(CogGuide())
