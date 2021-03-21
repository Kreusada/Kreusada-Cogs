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

    X=True
    W=tuple
    M='__version__'
    L='yaml'
    K=len
    J=isinstance
    G='diff'
    F=getattr
    B=hasattr
    import pip,sys as D,redbot as H,discord as I,logging as N,lavalink as O
    from distutils import sysconfig as P
    from redbot.core import commands as E
    from redbot.core.utils.chat_formatting import box as A,bold as C
    Q=N.getLogger('red.kreusada.vinfo')
    R='{}: {}\n{}: {}.{}.{}\n{}: {}\n\n{}: {}\n{}: {}'
    S=A('- Could not find a version for `{}`.',lang=G)
    T=A('- You do not have an installed module named `{}`.',lang=G)
    U=A("Builtin Red cogs do not have version attributes by default. Perhaps you're looking for your Red version, which would be {}.",lang=L)
    V=['Admin','Alias','Audio','Bank','Cleanup','CustomCom','Downloader','Economy','Filter','General','Image','Mod','ModLog','Mutes','Permissions','Reports','Streams','Trivia','Warnings']
    class Y(E.Cog):
        __author__=['Kreusada'];__version__='1.0.1'
        def __init__(self,bot):self.bot=bot
        @staticmethod
        def modvinfo_format(mods):formatter=C('Red'),H.version_info,C('Python (Sys)'),*D.version_info[:3],C('discord.py'),I.__version__,C('PIP'),pip.__version__,C('Lavalink'),O.__version__;description=mods.format(*formatter);return I.Embed(title='Common Modules',description=description)
        def format_help_for_context(self,ctx):context=super().format_help_for_context(ctx);authors=', '.join(self.__author__);return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"
        @E.is_owner()
        @E.group(aliases=['versioninfo'])
        async def vinfo(self,ctx):0
        @vinfo.command()
        async def cog(self,ctx,cog):
            await ctx.trigger_typing()
            if cog not in self.bot.cogs:return await ctx.send(A(f"- Could not find a cog matching `{cog}`.",lang=G))
            Cog=self.bot.get_cog(cog)
            if B(Cog,M):return await ctx.send(A(f"{cog} version: {F(Cog,M)}",lang=L))
            elif cog in V:return await ctx.send(U.format(H.version_info))
            else:await ctx.send(A(f"- Could not find a version for {cog}.",lang=G))
        @vinfo.command(aliases=['module','dep','dependency'],usage='<module or dependency>')
        @E.bot_has_permissions(embed_links=X)
        async def mod(self,ctx,module=None):
            G='{}.';E='[Core/Builtin Python]';C='.'
            if not module:embed=self.modvinfo_format(R);embed.color=await ctx.embed_colour();embed.set_footer(text='Find a specific module version by adding the module argument.');await ctx.send(embed=embed);return await ctx.send_help()
            version_info='version_info';versionattr=M;shortversionattr='_version_';version='version';pypath=str(P.get_python_lib(standard_lib=X));await ctx.trigger_typing()
            try:MOD=__import__(module)
            except ModuleNotFoundError as mnfe:return await ctx.send(T.format(module))
            if B(MOD,version_info):vinfo=[F(MOD,version_info),C+version_info]
            elif B(MOD,versionattr):vinfo=[F(MOD,versionattr),C+versionattr]
            elif B(MOD,shortversionattr):vinfo=[F(MOD,shortversionattr),C+shortversionattr]
            elif B(MOD,version):vinfo=[F(MOD,version),C+version]
            elif B(MOD,'__file__'):
                if MOD.__file__.lower().startswith(pypath.lower()):vinfo=[D.version_info[:3],E]
            elif B(MOD,'__spec__'):
                if not MOD.__spec__.origin:vinfo=[D.version_info[:3],E]
                spec=MOD.__spec__.origin.lower()
                if spec.startswith(pypath.lower())or spec=='built-in':vinfo=[D.version_info[:3],E]
            else:Q.info(f"[From {ctx.channel.id}] {module} path: {MOD.__file__}");return await ctx.send(S.format(MOD.__name__))
            if J(vinfo[0],W)and vinfo[1].endswith(E):value=(G*K(vinfo[0])).strip(C).format(*vinfo[0]);attr=f"None {vinfo[1]}"
            elif J(vinfo[0],W):value=(G*K(vinfo[0])).strip(C).format(*vinfo[0]);attr=f"`{MOD.__name__}{vinfo[1]}`"
            elif J(vinfo[0],list):value=(G*K(vinfo[0])).strip(C).format(*vinfo[0]);attr=f"`{MOD.__name__}{vinfo[1]}`"
            else:value=vinfo[0];attr=f"`{MOD.__name__}{vinfo[1]}`"
            await ctx.send(A(f"Attribute: {attr}\nFound version info for [{module}]: {value}",lang=L))


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