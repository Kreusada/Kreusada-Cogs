import discord
import random
from redbot.core import commands, checks, Config
from .mdtembed import Embed

class Find(commands.Cog):
  """Find"""
  
  def __init__(self):
    self.config = Config.get_conf(self, 200730042020, force_registration=True)
    
  @commands.group()
  @checks.admin()
  async def find(self, ctx):
    """The Matrix Development Team Index."""
    pass
  
  @find.group()
  async def matrixrepo(self, ctx):
    """Browse our Cog Creator's repositories."""
    
  @matrixrepo.group()
  async def kreusada(self, ctx):
    """Kreusada's Github Repository."""
    await ctx.send(f"https://github.com/KREUSADA/demaratus/")
    
  @matrixrepo.group()
  async def jojo(self, ctx):
    """Jojo's Github Repository."""
    await ctx.send(f"https://github.com/Just-Jojo/JojoCogs/")
    
  @matrixrepo.group()
  async def flyingkiller(self, ctx):
    """FlyingKiller147's Github Repository."""
    await ctx.send(f"https://github.com/FlyingKiller147/mybotfk/")
    
  @matrixrepo.group()
  async def adnayekken(self, ctx):
    """Adnayekken's Github Repository."""
    await ctx.send(f"Adnayekken's Github Repository is temporarily closed. :x:")
    
  @matrixrepo.group()
  async def otriux(self, ctx):
    """Otriux's Github Repository."""
    await ctx.send(f"Otriux's Github Repository has not yet been submitted!")
    
  @matrixrepo.group()
  async def titan(self, ctx):
    """The Mad Titan's Github Repository."""
    await ctx.send(f"Titan's Github Repository has not yet been submitted!")
    
  @matrixrepo.group()
  async def octavius(self, ctx):
    """Octavius' Github Repository."""
    await ctx.send(f"Octavius doesn't code anymore! :robot:")
    
  @matrixrepo.group()
  async def zagelfino(self, ctx):
    """Zagelfino's Github Repository."""
    await ctx.send(f"Zagelfino doesn't code anymore! :robot:")
    
  @find.group()
  async def matrixdocs(self, ctx):
    """Shows the documentation for some of our bots."""
    
  @matrixdocs.group()
  async def demaratus(self, ctx):
    """Demaratus' RTD Documentation."""
    await ctx.send(f"Demaratus Documentation: https://kreusadacogs.readthedocs.io/en/latest/\nThis documentation is scripted by Kreusada, and won't be completed until 2021 for sure.\nYou can contribute, let us know, or create a pull request on my github repo under /docs.")
  
  @matrixdocs.group()
  async def collector(self, ctx):
    """Collector Documentation."""
    await ctx.send(f"Unfortunately, Collector does not have a documentation at this time.\nHowever, JJW has made some video guides for the Collector.\nYou can watch them here: https://www.youtube.com/watch?v=wO5JFXJZBHE&list=PLrM7-aBPjDsRVEq1UpvV-u85K06Ds7suD")
  
  @find.group()
  async def awbadges(self, ctx):
    """The Alliance War badge index."""
    
  @awbadges.group()
  async def master(self, ctx):
    """Master Alliance War Badges."""
  
  @awbadges.group()
  async def platinum(self, ctx):
    """Platinum Alliance War Badges."""
    
  @awbadges.group()
  async def gold(self, ctx):
    """Gold Alliance War Badges."""
    
  @awbadges.group()
  async def silver(self, ctx):
    """Silver Alliance War Badges."""
    
  @awbadges.group()
  async def bronze(self, ctx):
    """Bronze Alliance War Badges."""
    
  @awbadges.group()
  async def stone(self, ctx):
    """Stone Alliance War Badges."""
    
  @awbadges.group()
  async def participation(self, ctx):
    """Participation Alliance War Badges."""
    
  @master.group(name="1", invoke_without_command=True)
  async def one(self, ctx):
    """Master Rank 1 Badge."""
    author = ctx.message.author
    data = Embed.create(self, ctx, title='Master Rank One Badge :trophy:')
    image = (f"https://media.discordapp.net/attachments/401476363707744257/738083791654092940/47EFB6D4D1380ABD2C40D2C7B0533A29245F7955.png")
    data.set_author(name=author)
    data.set_image(url=image)
    await ctx.send(embed=data)
    
  @master.group(name="2", invoke_without_command=True)
  async def two(self, ctx):
    """Master Rank 2 Badge."""
    author = ctx.message.author
    data = Embed.create(self, ctx, title='Master Rank Two Badge :trophy:')
    image = (f"https://media.discordapp.net/attachments/401476363707744257/738083791113027654/650E29ADB8C5C382FF5A358113B2C02B8EADA415.png")
    data.set_author(name=author)
    data.set_image(url=image)
    await ctx.send(embed=data)
    
  @master.group(name="3", invoke_without_command=True)
  async def three(self, ctx):
    """Master Rank 3 Badge."""
    author = ctx.message.author
    data = Embed.create(self, ctx, title='Master Rank Three Badge :trophy:')
    image = (f"https://media.discordapp.net/attachments/401476363707744257/738083791440052294/08BA0A081A9D56E35E60E3FD61FAB7ED9A10CD00.png")
    data.set_author(name=author)
    data.set_image(url=image)
    await ctx.send(embed=data)
    
  @master.group(name="20", invoke_without_command=True)
  async def four(self, ctx):
    """Master Top 20 Badge."""
    author = ctx.message.author
    data = Embed.create(self, ctx, title='Master Badge :trophy:')
    image = (f"https://media.discordapp.net/attachments/401476363707744257/738083791301509191/28A5CCCA9CA8294C76D8BE94CC0ADD2734B26570.png")
    data.set_author(name=author)
    data.set_image(url=image)
    await ctx.send(embed=data)
    
  @platinum.group(name="1", invoke_without_command=True)
  async def five(self, ctx):
    """Platinum 1 Badge."""
    author = ctx.message.author
    data = Embed.create(self, ctx, title='Platinum One Badge :trophy:')
    image = (f"https://media.discordapp.net/attachments/401476363707744257/738083790718631937/E78E2BAF9B0C9BA6C7FE45BE726FFB0B0B0CACFD.png")
    data.set_author(name=author)
    data.set_image(url=image)
    await ctx.send(embed=data)
    
  @platinum.group(name="2", invoke_without_command=True)
  async def six(self, ctx):
    """Platinum 2 Badge."""
    author = ctx.message.author
    data = Embed.create(self, ctx, title='Platinum Two Badge :trophy:')
    image = (f"https://media.discordapp.net/attachments/401476363707744257/738083790362116116/487EA26A1BA0F2C2848E7C87F10430BD218C2178.png")
    data.set_author(name=author)
    data.set_image(url=image)
    await ctx.send(embed=data)
    
  @platinum.group(name="3", invoke_without_command=True)
  async def seven(self, ctx):
    """Platinum 3 Badge."""
    author = ctx.message.author
    data = Embed.create(self, ctx, title='Platinum Three Badge :trophy:')
    image = (f"https://media.discordapp.net/attachments/401476363707744257/738083790559117352/0ED8BD10441C6D086AEB7BBA5271269F46E009D1.png")
    data.set_author(name=author)
    data.set_image(url=image)
    await ctx.send(embed=data)
    
  @platinum.group(name="4", invoke_without_command=True)
  async def eight(self, ctx):
    """Platinum 4 Badge."""
    author = ctx.message.author
    data = Embed.create(self, ctx, title='Platinum Four Badge :trophy:')
    image = (f"https://media.discordapp.net/attachments/401476363707744257/738083789934166046/71703F9C740FFDC3223A570CC1C252D8392534BC.png")
    data.set_author(name=author)
    data.set_image(url=image)
    await ctx.send(embed=data)
    
  @gold.group(name="1", invoke_without_command=True)
  async def nine(self, ctx):
    """Gold 1 Badge."""
    author = ctx.message.author
    data = Embed.create(self, ctx, title='Gold One Badge :trophy:')
    image = (f"https://media.discordapp.net/attachments/401476363707744257/738083790131298375/76BC21BF523A415866D19814BD8AF4BE16EF30A9.png")
    data.set_author(name=author)
    data.set_image(url=image)
    await ctx.send(embed=data)
    
  @gold.group(name="2", invoke_without_command=True)
  async def ten(self, ctx):
    """Gold 2 Badge."""
    author = ctx.message.author
    data = Embed.create(self, ctx, title='Gold Two Badge :trophy:')
    image = (f"https://media.discordapp.net/attachments/401476363707744257/738083998462509096/8CD52FEB7540016B6ABA1EC67B9F1777E3C29878.png")
    data.set_author(name=author)
    data.set_image(url=image)
    await ctx.send(embed=data)
    
  @gold.group(name="3", invoke_without_command=True)
  async def eleven(self, ctx):
    """Gold 3 Badge."""
    author = ctx.message.author
    data = Embed.create(self, ctx, title='Gold Three Badge:trophy:')
    image = (f"https://media.discordapp.net/attachments/401476363707744257/738084001926873098/3A9A8FDA006D0BE225242AAA5909021CD52BCFB3.png")
    data.set_author(name=author)
    data.set_image(url=image)
    await ctx.send(embed=data)
    
  @silver.group(name="1", invoke_without_command=True)
  async def twelve(self, ctx):
    """Silver 1 Badge."""
    author = ctx.message.author
    data = Embed.create(self, ctx, title='Silver One Badge :trophy:')
    image = (f"https://media.discordapp.net/attachments/401476363707744257/738084001465499789/4B389D377A94EDA747B38DF640C0B33A3A3F61AE.png")
    data.set_author(name=author)
    data.set_image(url=image)
    await ctx.send(embed=data)
    
  @silver.group(name="2", invoke_without_command=True)
  async def thirteen(self, ctx):
    """Silver 2 Badge."""
    author = ctx.message.author
    data = Embed.create(self, ctx, title='Silver Two Badge :trophy:')
    image = (f"https://media.discordapp.net/attachments/401476363707744257/738084001465499789/4B389D377A94EDA747B38DF640C0B33A3A3F61AE.png")
    data.set_author(name=author)
    data.set_image(url=image)
    await ctx.send(embed=data)
    
  @silver.group(name="3", invoke_without_command=True)
  async def fourteen(self, ctx):
    """Silver 3 Badge."""
    author = ctx.message.author
    data = Embed.create(self, ctx, title='Silver Three Badge :trophy:')
    image = (f"https://media.discordapp.net/attachments/401476363707744257/738083994612006914/5302FA8FA04735224847C8BBF82D1D54C8567B9C.png")
    data.set_author(name=author)
    data.set_image(url=image)
    await ctx.send(embed=data)
    
  @bronze.group(name="1", invoke_without_command=True)
  async def fifteen(self, ctx):
    """Bronze 1 Badge."""
    author = ctx.message.author
    data = Embed.create(self, ctx, title='Bronze One Badge :trophy:')
    image = (f"https://media.discordapp.net/attachments/401476363707744257/738083995211792404/719AC2C2AB5833D815C899DAF9ADB7CF11819CBA.png")
    data.set_author(name=author)
    data.set_image(url=image)
    await ctx.send(embed=data)
    
  @bronze.group(name="2", invoke_without_command=True)
  async def sixteen(self, ctx):
    """Bronze 2 Badge."""
    author = ctx.message.author
    data = Embed.create(self, ctx, title='Bronze Two Badge :trophy:')
    image = (f"https://media.discordapp.net/attachments/401476363707744257/738083993043337276/E636A90C3F0DFFDAED0176D972AA0C73F3E40FF8.png")
    data.set_author(name=author)
    data.set_image(url=image)
    await ctx.send(embed=data)
    
  @bronze.group(name="3", invoke_without_command=True)
  async def seventeen(self, ctx):
    """Bronze 3 Badge."""
    author = ctx.message.author
    data = Embed.create(self, ctx, title='Bronze Three Badge :trophy:')
    image = (f"https://media.discordapp.net/attachments/401476363707744257/738083997866786876/5B06D509847E0FA1405A50021486C1A5D8C6F9B2.png")
    data.set_author(name=author)
    data.set_image(url=image)
    await ctx.send(embed=data)

  @stone.group(name="1", invoke_without_command=True)
  async def eighteen(self, ctx):
    """Stone 1 Badge."""
    author = ctx.message.author
    data = Embed.create(self, ctx, title='Stone One Badge :trophy:')
    image = (f"https://media.discordapp.net/attachments/401476363707744257/738083996054978730/9AC92A2FDC2996C346125296356C664373147F2F.png")
    data.set_author(name=author)
    data.set_image(url=image)
    await ctx.send(embed=data)
    
  @stone.group(name="2", invoke_without_command=True)
  async def nineteen(self, ctx):
    """Stone 2 Badge."""
    author = ctx.message.author
    data = Embed.create(self, ctx, title='Stone Two Badge :trophy:')
    image = (f"https://media.discordapp.net/attachments/401476363707744257/738083993681002586/BF3D13EACC9F44216E754884AA183185761C84CF.png")
    data.set_author(name=author)
    data.set_image(url=image)
    await ctx.send(embed=data)
    
  @stone.group(name="3", invoke_without_command=True)
  async def twenty(self, ctx):
    """Stone 3 Badge."""
    author = ctx.message.author
    data = Embed.create(self, ctx, title='Stone Three Badge :trophy:')
    image = (f"https://media.discordapp.net/attachments/401476363707744257/738084098857238670/EA938C0B0C2AE3E6DB91514F5F8768C4F033D373.png")
    data.set_author(name=author)
    data.set_image(url=image)
    await ctx.send(embed=data)
    
  @participation.group(name="1", invoke_without_command=True, pass_context=True)
  async def twentyone(self, ctx):
    """Participation Badge."""
    author = ctx.message.author
    data = Embed.create(self, ctx, title='Participation Badge :trophy:')
    image = (f"https://media.discordapp.net/attachments/401476363707744257/738083790886535228/DA7D39277836A9CF1B39A68D37EAF99999B366C7.png")
    data.set_author(name=author)
    data.set_image(url=image)
    await ctx.send(embed=data)

 
