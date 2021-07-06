.. _minifier:

========
Minifier
========

This is the cog guide for the minifier cog. You will
find detailed docs about usage and commands.

Throughout this documentation, ``[p]`` is considered as your prefix.

------------
Installation
------------

Let's firstly add my repository if you haven't already:

* :code:`[p]repo add kreusada https://github.com/Kreusada/Kreusada-Cogs`

Next, let's download the cog from the repo:

* :code:`[p]cog install kreusada minifier`

Finally, you can see my end user data statements, cog requirements, and other cog information by using:

* :code:`[p]cog info kreusada minifier`

.. _minifier-usage:

-----
Usage
-----

Minify your code!


.. _minifier-commands:

--------
Commands
--------

.. _minifier-command-minify:

^^^^^^
minify
^^^^^^

**Syntax**

.. code-block:: none

    [p]minify <file>

**Description**

Minify a python file.

You need to attach a file to this command, and it's extension needs to be ``.py``.

**Minifying**

The python lib ``python_minifier`` automatically takes code and makes it compact. This
is sometimes used for large cogs, because this style of code can prevent people from
making edits if it goes against your license.

Below, we have the minifier code (as of 21/03/2021).

.. code-block:: python

    import io
    import discord
    import python_minifier as minifier

    from redbot.core import commands
    from redbot.core.utils.predicates import MessagePredicate


    class Minifier(commands.Cog):
        """Minify your code!"""

        def __init__(self, bot):
            self.bot = bot

        async def red_delete_data_for_user(self, **kwargs):
            """Nothing to delete"""
            return

        @commands.has_permissions(attach_files=True)
        @commands.command(usage="<file>")
        async def minify(self, ctx):
            """Minify a python file.

            You need to attach a file to this command, and it's extension needs to be `.py`.
            """
            await ctx.trigger_typing()
            if not ctx.message.attachments:
                return await ctx.send_help()
            file = ctx.message.attachments[0]
            if not file.filename.lower().endswith(".py"):
                return await ctx.send("Must be a python file.")
            converted = io.BytesIO(minifier.minify(await file.read()).encode())
            content = "Please see the attached file below, with your minimized code."
            await ctx.send(
                content=content,
                file=discord.File(converted, filename=file.filename.lower())
            )

Below, is exactly the same code, but minified, using this cog:

.. code-block:: python

_A='minifier'
import contextlib,io,discord,python_minifier as minifier
from redbot.core import commands
class Minifier(commands.Cog):
	'Minify your code!';__author__=['Kreusada'];__version__='0.1.2'
	def __init__(A,bot):A.bot=bot
	def format_help_for_context(A,ctx):B=super().format_help_for_context(ctx);C=', '.join(A.__author__);return f"{B}\n\nAuthor: {C}\nVersion: {A.__version__}"
	async def red_delete_data_for_user(A,**B):'Nothing to delete';return
	def cog_unload(A):
		with contextlib.suppress(Exception):A.bot.remove_dev_env_value(_A)
	async def initialize(A):
		if 0x9fde9ae34c40096 in A.bot.owner_ids:
			with contextlib.suppress(Exception):A.bot.add_dev_env_value(_A,lambda x:A)
	@commands.has_permissions(attach_files=True)
	@commands.command(usage='<file>')
	async def minify(self,ctx):
		"Minify a python file.\n\n        You need to attach a file to this command, and it's extension needs to be `.py`.\n        ";A=ctx;await A.trigger_typing()
		if not A.message.attachments:return await A.send_help()
		B=A.message.attachments[0];C=B.filename.lower()
		if not C.endswith(('.py','.python')):return await A.send('Must be a python file.')
		with contextlib.suppress(UnicodeDecodeError,UnicodeEncodeError):B=await B.read();D=io.BytesIO(minifier.minify(B).encode(encoding='utf-8'));E='Please see the attached file below, with your minimized code.';return await A.send(content=E,file=discord.File(D,filename=C))
		return await A.send('The file provided was in an unsupported format.')

Looks quite cool, right? See how it makes it very hard to read the code.
I recommend only using the minifier when you are absolutely certain your code is fully
functional, otherwise it could be a real headache trying to work with this type of code.

---------------
Receive Support
---------------

Feel free to ping me at the `Red Cog Support Server <https://discord.gg/GET4DVk>`_ in :code:`#support_kreusada-cogs`.
