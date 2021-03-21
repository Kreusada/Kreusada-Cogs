.. _minifier:

========
Minifier
========

This is the cog guide for the minifier cog. You will
find detailed docs about usage and commands.

``[p]`` is considered as your prefix.

.. note:: To use this cog, load it by typing this::

        [p]load minifier

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

    import io,discord,python_minifier as minifier
    from redbot.core import commands
    from redbot.core.utils.predicates import MessagePredicate
    class Minifier(commands.Cog):
        'Minify your code!'
        def __init__(A,bot):A.bot=bot
        async def red_delete_data_for_user(A,**B):'Nothing to delete';return
        @commands.has_permissions(attach_files=True)
        @commands.command(usage='<file>')
        async def minify(self,ctx):
            "Minify a python file.\n\n        You need to attach a file to this command, and it's extension needs to be `.py`.\n        ";A=ctx;await A.trigger_typing()
            if not A.message.attachments:return await A.send_help()
            B=A.message.attachments[0]
            if not B.filename.lower().endswith('.py'):return await A.send('Must be a python file.')
            C=io.BytesIO(minifier.minify(await B.read()).encode());D='Please see the attached file below, with your minimized code.';await A.send(content=D,file=discord.File(C,filename=B.filename.lower()))

Looks quite cool, right? See how it makes it very hard to read the code.
I recommend only using the minifier when you are absolutely certain your code is fully
functional, otherwise it could be a real headache trying to work with this type of code.

We also have my :ref:`Vinfo <vinfo>` cog, exampled below:

.. code-block:: python

    """
    MIT License
    Copyright (c) 2021 Kreusada
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
    """

    import pip
    import sys
    import redbot
    import discord
    import logging
    import lavalink

    from distutils import sysconfig

    from redbot.core import commands
    from redbot.core.utils.chat_formatting import box, bold

    log = logging.getLogger("red.kreusada.vinfo")

    base = "{}: {}\n{}: {}.{}.{}\n{}: {}\n\n{}: {}\n{}: {}"

    RETURN_TYPE_1 = box(
        "- Could not find a version for `{}`.",
        lang="diff"
    )
    RETURN_TYPE_2 = box(
        "- You do not have an installed module named `{}`.", 
        lang="diff"
    )
    RETURN_TYPE_3 = box(
        "Builtin Red cogs do not have version attributes by default. Perhaps you're looking for your Red version, which would be {}.",
        lang="yaml"
    )

    REDBOT_CORE_COGS = [
        "Admin",
        "Alias",
        "Audio",
        "Bank",
        "Cleanup",
        "CustomCom",
        "Downloader",
        "Economy",
        "Filter",
        "General",
        "Image",
        "Mod",
        "ModLog",
        "Mutes",
        "Permissions",
        "Reports",
        "Streams",
        "Trivia",
        "Warnings",
    ]


    class Vinfo(commands.Cog):
        """
        Get versions of 3rd party cogs, and modules.
        """

        __author__ = [
            "Kreusada",
        ]
        __version__ = "1.0.1"

        def __init__(self, bot):
            self.bot = bot

        def format_help_for_context(self, ctx: commands.Context) -> str:
            context = super().format_help_for_context(ctx)
            authors = ", ".join(self.__author__)
            return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

        async def red_delete_data_for_user(self, **kwargs):
            """Nothing to delete"""
            return

        @staticmethod
        def modvinfo_format(mods):
            formatter = (
                bold("Red"),
                redbot.version_info,
                bold("Python (Sys)"),
                *sys.version_info[:3],
                bold("discord.py"),
                discord.__version__,
                bold("PIP"),
                pip.__version__,
                bold("Lavalink"),
                lavalink.__version__,
            )
            description = mods.format(*formatter)
            return discord.Embed(
                title="Common Modules",
                description=description,
            )

        # Commands

        @commands.is_owner()
        @commands.group(aliases=["versioninfo"])
        async def vinfo(self, ctx):
            """Get versions of 3rd party cogs, and modules."""

        @vinfo.command()
        async def cog(self, ctx, cog: str):
            """
            Get the version information for a Red cog.
            The cog must be loaded, and provided in the correct casing.
            """
            await ctx.trigger_typing()
            
            if cog not in self.bot.cogs:
                return await ctx.send(box(f"- Could not find a cog matching `{cog}`.", lang='diff'))

            Cog = self.bot.get_cog(cog)

            # Note that cogs won't have a `version_info` attr unlike some modules, so
            # we'll skip finding that attr because it will return False 99% of the time.

            if hasattr(Cog, "__version__"):
                return await ctx.send(box(f"{cog} version: {getattr(Cog, '__version__')}", lang='yaml'))
            elif cog in REDBOT_CORE_COGS:
                return await ctx.send(RETURN_TYPE_3.format(redbot.version_info))
            else:
                await ctx.send(box(f"- Could not find a version for {cog}.", lang='diff'))

        @vinfo.command(aliases=["module", "dep", "dependency"], usage="<module or dependency>")
        @commands.bot_has_permissions(embed_links=True)
        async def mod(self, ctx, module: str = None):
            """Get module versions."""
            
            if not module:
                embed = self.modvinfo_format(base)
                embed.color = await ctx.embed_colour()
                embed.set_footer(
                    text="Find a specific module version by adding the module argument."
                )
                await ctx.send(embed=embed)
                return await ctx.send_help()

            # If `version_info` is defined, we should refer to this first.
            version_info = "version_info"
            versionattr = "__version__"
            shortversionattr = '_version_'
            version = 'version'

            pypath = str(sysconfig.get_python_lib(standard_lib=True))
            await ctx.trigger_typing()

            try:
                MOD = __import__(module)
            except ModuleNotFoundError:
                return await ctx.send(RETURN_TYPE_2.format(module))

            if hasattr(MOD, version_info):
                vinfo = [getattr(MOD, version_info), "." + version_info]

            elif hasattr(MOD, versionattr):
                vinfo = [getattr(MOD, versionattr), "." + versionattr]

            elif hasattr(MOD, shortversionattr):
                vinfo = [getattr(MOD, shortversionattr), "." + shortversionattr]

            elif hasattr(MOD, version):
                vinfo = [getattr(MOD, version), "." + version]

            elif (
                (
                    hasattr(MOD, '__file__') 
                    and MOD.__file__.lower().startswith(pypath.lower())
                )
                or 
                (
                    hasattr(MOD, '__spec__')
                    and MOD.__spec__.origin.lower().startswith(pypath.lower())
                    or MOD.__spec__.origin.lower() == "built-in"
                    or not MOD.__spec__.origin
                )
            ):
                vinfo = [(sys.version_info[:3]), "[Core/Builtin Python]"]

            else:
                return await ctx.send(
                    RETURN_TYPE_1.format(MOD.__name__)
                )

            if isinstance(vinfo[0], tuple) and vinfo[1].endswith("[Core/Builtin Python]"):
                value = ("{}." * len(vinfo[0])).strip('.').format(*vinfo[0])
                attr = f"None {vinfo[1]}"
            
            elif isinstance(vinfo[0], tuple):
                value = ("{}." * len(vinfo[0])).strip('.').format(*vinfo[0])
                attr = f"`{MOD.__name__}{vinfo[1]}`"

            elif isinstance(vinfo[0], list):
                value = ("{}." * len(vinfo[0])).strip('.').format(*vinfo[0])
                attr = f"`{MOD.__name__}{vinfo[1]}`"

            else:
                value = vinfo[0]
                attr = f"`{MOD.__name__}{vinfo[1]}`"


            await ctx.send(
                box(
                    f"Attribute: {attr}\nFound version info for [{module}]: {value}",
                    lang="yaml",
                )
            )

To this...

.. code-block:: python

    '\nMIT License\n\nCopyright (c) 2021 Kreusada\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n'
    _C='__version__'
    _B='yaml'
    _A='diff'
    import pip,sys,redbot,discord,logging,lavalink
    from distutils import sysconfig
    from redbot.core import commands
    from redbot.core.utils.chat_formatting import box,bold
    log=logging.getLogger('red.kreusada.vinfo')
    base='{}: {}\n{}: {}.{}.{}\n{}: {}\n\n{}: {}\n{}: {}'
    RETURN_TYPE_1=box('- Could not find a version for `{}`.',lang=_A)
    RETURN_TYPE_2=box('- You do not have an installed module named `{}`.',lang=_A)
    RETURN_TYPE_3=box("Builtin Red cogs do not have version attributes by default. Perhaps you're looking for your Red version, which would be {}.",lang=_B)
    REDBOT_CORE_COGS=['Admin','Alias','Audio','Bank','Cleanup','CustomCom','Downloader','Economy','Filter','General','Image','Mod','ModLog','Mutes','Permissions','Reports','Streams','Trivia','Warnings']
    class Vinfo(commands.Cog):
        '\n    Get versions of 3rd party cogs, and modules.\n    ';__author__=['Kreusada'];__version__='1.0.1'
        def __init__(A,bot):A.bot=bot
        def format_help_for_context(A,ctx):B=super().format_help_for_context(ctx);C=', '.join(A.__author__);return f"{B}\n\nAuthor: {C}\nVersion: {A.__version__}"
        async def red_delete_data_for_user(A,**B):'Nothing to delete';return
        @staticmethod
        def modvinfo_format(mods):A=bold('Red'),redbot.version_info,bold('Python (Sys)'),*sys.version_info[:3],bold('discord.py'),discord.__version__,bold('PIP'),pip.__version__,bold('Lavalink'),lavalink.__version__;B=mods.format(*A);return discord.Embed(title='Common Modules',description=B)
        @commands.is_owner()
        @commands.group(aliases=['versioninfo'])
        async def vinfo(self,ctx):'Get versions of 3rd party cogs, and modules.'
        @vinfo.command()
        async def cog(self,ctx,cog):
            '\n        Get the version information for a Red cog.\n\n        The cog must be loaded, and provided in the correct casing.\n        ';B=ctx;A=cog;await B.trigger_typing()
            if A not in self.bot.cogs:return await B.send(box(f"- Could not find a cog matching `{A}`.",lang=_A))
            C=self.bot.get_cog(A)
            if hasattr(C,_C):return await B.send(box(f"{A} version: {getattr(C,_C)}",lang=_B))
            elif A in REDBOT_CORE_COGS:return await B.send(RETURN_TYPE_3.format(redbot.version_info))
            else:await B.send(box(f"- Could not find a version for {A}.",lang=_A))
        @vinfo.command(aliases=['module','dep','dependency'],usage='<module or dependency>')
        @commands.bot_has_permissions(embed_links=True)
        async def mod(self,ctx,module=None):
            'Get module versions.';O='[Core/Builtin Python]';N='{}.';E=module;D='.';C=ctx
            if not E:H=self.modvinfo_format(base);H.color=await C.embed_colour();H.set_footer(text='Find a specific module version by adding the module argument.');await C.send(embed=H);return await C.send_help()
            I='version_info';J=_C;K='_version_';L='version';M=str(sysconfig.get_python_lib(standard_lib=True));await C.trigger_typing()
            try:B=__import__(E)
            except ModuleNotFoundError:return await C.send(RETURN_TYPE_2.format(E))
            if hasattr(B,I):A=[getattr(B,I),D+I]
            elif hasattr(B,J):A=[getattr(B,J),D+J]
            elif hasattr(B,K):A=[getattr(B,K),D+K]
            elif hasattr(B,L):A=[getattr(B,L),D+L]
            elif hasattr(B,'__file__')and B.__file__.lower().startswith(M.lower())or(hasattr(B,'__spec__')and B.__spec__.origin.lower().startswith(M.lower())or B.__spec__.origin.lower()=='built-in'or not B.__spec__.origin):A=[sys.version_info[:3],O]
            else:return await C.send(RETURN_TYPE_1.format(B.__name__))
            if isinstance(A[0],tuple)and A[1].endswith(O):F=(N*len(A[0])).strip(D).format(*A[0]);G=f"None {A[1]}"
            elif isinstance(A[0],tuple):F=(N*len(A[0])).strip(D).format(*A[0]);G=f"`{B.__name__}{A[1]}`"
            elif isinstance(A[0],list):F=(N*len(A[0])).strip(D).format(*A[0]);G=f"`{B.__name__}{A[1]}`"
            else:F=A[0];G=f"`{B.__name__}{A[1]}`"
            await C.send(box(f"Attribute: {G}\nFound version info for [{E}]:


----------------------
Additional Information
----------------------

This cog has been vetted by the Red-DiscordBot QA team as approved.
For inquiries, see to the contact options below.

---------------
Receive Support
---------------

Feel free to ping me at the `Red Cog Support Server <https://discord.gg/GET4DVk>`_ in :code:`#support_othercogs`,
or you can head over to `my support server <https://discord.gg/JmCFyq7>`_ and ask your questions in :code:`#support-kreusadacogs`.