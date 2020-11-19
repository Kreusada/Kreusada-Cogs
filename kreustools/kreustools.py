from redbot.core import commands, checks, Config
import discord
import random
import json
import os
from .deembed import Embed
from discord.utils import get

class Kreustools(commands.Cog):
  """Tools from Kreusada and Others."""

  def __init__(self, bot):
    self.bot = bot
    self.config = Config.get_conf(
      self, identifier=153607829, force_registration=True)
    self.config.register_guild(
      channel=None
    )
        
  @commands.command(pass_context=True, no_pm=True)
  async def showtopic(self, ctx, channel: discord.TextChannel = None):
    """Show the Channel Topic in a chat channel."""
    if channel is None:
      channel = ctx.message.channel
      topic = channel.topic
      if topic is not None and topic != '':
        embed = Embed.create(self, ctx, title=f"Channel Topic Tool :tools:",
                            description=f"\n\n**Channel: {channel.mention}**\n**Topic:** {topic}\n\nChannel ID: **{channel.id}**\nRequested by: **{ctx.author.name}**.")
        await ctx.send(embed=embed)
