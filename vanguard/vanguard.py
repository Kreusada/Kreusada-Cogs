import discord
from validator_collection import validators
from redbot.core import commands, checks, Config, modlog
from .vangem import Embed

class Vanguard(commands.Cog):
  """Vanguard Support Schema."""
  
  def __init__(self,bot):
      self.bot = bot
      self.vg = self.bot.get_guild(744572173137477692)
      self.config = Config.get_conf(
          self, 200730042020, force_registration=True)
      default_guild = {
          "role": None,
          "channel": None
      }
      self.config.register_guild(**default_guild)
      
  @commands.group()
  async def rule(self, ctx):
    """Vanguard Rule Index"""
    
  @commands.group()
  async def guide(self, ctx):
    """Vanguard Guide Index"""
    
  @rule.command()
  @checks.admin()
  async def full(self, ctx):
    embed = Embed.create(
      self, ctx, title="<:alert:777928824670388254> Vanguard Rules",
      description=(
        "\n\nHey there, welcome to the Vanguards. "
        "This server can help you to learn, implement and use **code**. "
        "We support multiple coding languages and are happy to help you. "
        "Additionally, this is the primary support server for <@766580519000473640>. "
        "We have some rules, which **must** be followed for the welfare of our members.\n\n"
        "**Rule 1**\n\nDO NOT share bot tokens anywhere. If you're showing code which includes the token, please replace it with placeholding text.\n\n"
        "**Rule 2**\n\nKeep to the correct channels, we'll be strict on this. If you don't know where you're going, ask in <#758775858222727168>. Additionally, keep discussion relevant to the channel topic.\n\n" 
        "**Rule 3**\n\nWe will not offer support for coding which involves illegally mitigating APIs and websites, or that breaks terms of service for discord or the targeted environment. Or for other actions which may be considered malicious from intent.\n\n"
        "**Rule 4**\n\nListen to and respect staff members and their instructions. Do not be rude or vulgar to those who voluntarily give up their time to help you.\n\n"
        "**Rule 5**\n\nDo not spam. Do not advertise content; this includes discord servers, or media that you are looking to promote. We don't do that here.\n\n"
        "**Rule 6**\n\nUsernames that involve unicode, slurs or invisibility will be changed.\n\n"
        "**Quick Links:**\n(Invite Demaratus)[https://discord.com/oauth2/authorize?client_id=766580519000473640&scope=bot&permissions=8],"
        " | (Main Community Server)[https://discord.gg/h5mUyEG] | (Demaratus Documentation)[https://kreusadacogs.readthedocs.io/en/latest/]"
      ),
      color=0x59e1ac
    )
    await ctx.send(embed=embed)
