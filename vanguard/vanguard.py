import discord
import random
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
        "**Rule 1**\nDO NOT share bot tokens anywhere. If you're showing code which includes the token, please replace it with placeholding text.\n\n"
        "**Rule 2**\nKeep to the correct channels, we'll be strict on this. If you don't know where you're going, ask in <#758775858222727168>. Additionally, keep discussion relevant to the channel topic.\n\n" 
        "**Rule 3**\nWe will not offer support for coding which involves illegally mitigating APIs and websites, or that breaks terms of service for discord or the targeted environment, or for other actions which may be considered malicious from intent.\n\n"
      ),
      color=0x59e1ac,
      footer_text=""
    )
    embed2 = Embed.create(
      self, ctx, description=(
        "**Rule 4**\nListen to and respect staff members and their instructions. Do not be rude or vulgar to those who voluntarily give up their time to help you.\n\n"
        "**Rule 5**\nDo not spam. Do not advertise content; this includes discord servers, or media that you are looking to promote. We don't do that here.\n\n"
        "**Rule 6**\nUsernames that involve unicode, slurs or invisibility will be changed.\n\n"
        "**Quick Links:**\n[Invite Demaratus](https://discord.com/oauth2/authorize?client_id=766580519000473640&scope=bot&permissions=8)"
        " | [Main Community Server](https://discord.gg/h5mUyEG) | [Demaratus Documentation](https://kreusadacogs.readthedocs.io/en/latest/)"
        " | [Vanguard Patreon](https://patreon.com/vanguards)"
      ),
      color=0x59e1ac
    )
    await ctx.send(embed=embed)
    await ctx.send(embed=embed2)
    
  @rule.command(name="1", aliases=["r1"])
  async def one(self, ctx):
    embed = Embed.create(
      self, ctx, title="<:alert:777928824670388254> Rule Number One",
      description="DO NOT share bot tokens anywhere. If you're showing code which includes the token, please replace it with placeholding text."
    )
    await ctx.send(embed=embed)

  @rule.command(name="2", aliases=["r2"])
  async def two(self, ctx):
    embed = Embed.create(
      self, ctx, title="<:alert:777928824670388254> Rule Number Two",
      description="Keep to the correct channels, we'll be strict on this. If you don't know where you're going, ask in <#758775858222727168>. Additionally, keep discussion relevant to the channel topic."
    )
    await ctx.send(embed=embed)

  @rule.command(name="3", aliases=["r3"])
  async def three(self, ctx):
    embed = Embed.create(
      self, ctx, title="<:alert:777928824670388254> Rule Number Three",
      description="We will not offer support for coding which involves illegally mitigating APIs and websites, or that breaks terms of service for discord or the targeted environment, or for other actions which may be considered malicious from intent."
    )
    await ctx.send(embed=embed)
      
  @rule.command(name="4", aliases=["r4"])
  async def four(self, ctx):
    embed = Embed.create(
      self, ctx, title="<:alert:777928824670388254> Rule Number Four",
      description="Listen to and respect staff members and their instructions. Do not be rude or vulgar to those who voluntarily give up their time to help you."
    )
    await ctx.send(embed=embed)

  @rule.command(name="5", aliases=["r5"])
  async def five(self, ctx):
    embed = Embed.create(
      self, ctx, title="<:alert:777928824670388254> Rule Number Five",
      description="Do not spam. Do not advertise content; this includes discord servers, or media that you are looking to promote. We don't do that here."
    )
    await ctx.send(embed=embed)

  @rule.command(name="6", aliases=["r6"])
  async def six(self, ctx):
    embed = Embed.create(
      self, ctx, title="<:alert:777928824670388254> Rule Number Six",
      description="Usernames that involve unicode, slurs or invisibility will be changed."
    )
    await ctx.send(embed=embed)
      
  @commands.command(aliases=["quicklink"])
  async def quicklinks(self, ctx):
    embed = Embed.create(
      self, ctx, title="<:alert:777928824670388254> Quicklinks",
      description=(
        "[Invite Demaratus](https://discord.com/oauth2/authorize?client_id=766580519000473640&scope=bot&permissions=8)"
        " | [Main Community Server](https://discord.gg/h5mUyEG) | [Demaratus Documentation](https://kreusadacogs.readthedocs.io/en/latest/)"
        " | [Vanguard Patreon](https://patreon.com/vanguards)"
      )
    )
    await ctx.send(embed=embed)
    
  @commands.command(aliases=["codeblocks"])
  async def codeblock(self, ctx):
    embed = Embed.create(
      self, ctx, title="Codeblocks!",
      description=(
        "Code blocks are used in Discord to represent code and data, supporting a range of coding languages. "
        "They are vital for showing people your code, otherwise things look real messy! "
        "Remember to use these code blocks when visiting our coding channels.\n\n"
        "**Small Code Blocks | **Syntax:** [`]\n\n**"
        "Represented using one backtick eitherside of the text. \n"
        "For example: `here is an example!`.\n"
        "Small code blocks are designed for mentioning small instances of code such as snippits, modules or command examples.\n\n"
        "**Large Code Blocks | **Syntax:** [```]\n\n**"
        "Represented using three backticks eitherside of the text."
        "It is important to include the file extension at the start of the code block. For example:"
        " ```py\n"
        "@main.command()\n"
        "async def command(self, ctx):\n"
        " await ctx.send()```\n"
        "**Using file extensions**"
      ),
      image="https://media.discordapp.net/attachments/763066391107862550/778398035675840532/codeblock_example.png"
    )
    await ctx.send(embed=embed)

  def check_dem_supportsquad(self, ctx, user=None):
    """Support Squad Checks"""
    role = discord.utils.get(self.vg.roles, id=745600714910335016)
    print('Support Squad member identified.')
    if user is None:
        user = ctx.message.author
        print('Message.author is user.')
    checkuser = discord.utils.get(self.vg.members, id=user.id)
    if checkuser is None:
        print('User not found in The Vanguards.')
        return False
    else:
        print('User found in The Vanguards.')
        if role in checkuser.roles:
            print('Support Squad Authenticated.')
            return True
        elif self.check_collectordevteam(ctx, user) is True:
            print('Support Squad Authenticated')
            return True
        else:
            print('User is not in the Support Squad.')
            return False
              
  def check_dem_devsquad(self, ctx, user=None):
    """Dev Squad Checks"""
    role = discord.utils.get(self.vg.roles, id=777606882256093214)
    if user is None:
        user = ctx.message.author
        checkuser = discord.utils.get(self.vg.members, id=user.id)
        if role in checkuser.roles:
            return True
        else:
            return False
    
  @commands.command(pass_context=True, name="demaratustips", aliases=["dt",])
  async def demaratus_tips(self, ctx, channel: discord.TextChannel, *, content):
      authorized = self.check_dem_supportsquad(ctx)
      if authorized is not True:
          return
      else:
          pages = []
          if len(ctx.message.attachments) > 0:
              image = ctx.message.attachments[0]
              imgurl = image.url
          else:
              imagelist = "https://media.discordapp.net/attachments/758775890954944572/779118744155979787/demaratusfull.png?width=907&height=641"
              imgurl = random.choice(imagelist)
          thumbnail = "https://media.discordapp.net/attachments/758775890954944572/779118859651252254/vanguardskeindem1.png?width=641&height=641"
          embed = Embed.create(
            self, ctx, title='Demaratus Tips', description=content,
            image=imgurl
          )
          embed.set_author(name="{} from the Demaratus Support Squad".format(
              ctx.message.author.display_name), icon_url=ctx.message.author.avatar_url)
#            data.add_field(name="Alliance Template",
#                           value="[Make an Alliance Guild](https://discord.new/gtzuXHq2kCg4)\nRoles, Channels & Permissions pre-defined", inline=False)
          embed.add_field(
              name="Add Demaratus", value="[Invite](https://discord.com/oauth2/authorize?client_id=766580519000473640&scope=bot&permissions=8)", inline=False)
          embed.add_field(
              name="Get Support", value="[The Vanguards](https://discord.gg/JmCFyq7)", inline=False)
          await channel.send(embed=embed)
        
    
