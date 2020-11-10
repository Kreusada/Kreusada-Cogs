from redbot.core import commands, checks, Config
import discord
import random
import json
import os
from .deembed import Embed
from discord.utils import get

class Demevents(commands.Cog):
  """Events specifically for Demaratus."""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=153607829, force_registration=True)
        self.config.register_guild()
        
