### Converted code from my Vinfo cog: https://github.com/Kreusada/Kreusada-Cogs/tree/master/vinfo

X=True
W=tuple
M='__version__'
L='yaml'
K=len
J=isinstance
G='diff'
F=getattr
B=hasattr
import logging as N
import sys as D
from distutils import sysconfig as P

import discord as I
import lavalink as O
import pip
import redbot as H
from redbot.core import commands as E
from redbot.core.utils.chat_formatting import bold as C
from redbot.core.utils.chat_formatting import box as A

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