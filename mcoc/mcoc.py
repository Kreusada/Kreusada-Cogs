from redbot.core import commands, checks, Config
import discord
import random
from .mdtembed import Embed

class Mcoc(commands.Cog):
  """Mcoc"""
  
  def __init__(self):
    self.config = Config.get_conf(self, 200730042020, force_registration=True)
    
  @commands.group()
  async def crystal(self, ctx):
    """Chooses a random champion from MCOC."""
    CHAMPS = [
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_abomination.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_aegon.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_agent_venom.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_airwalker.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_angela.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_annihilus.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_antman.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_apocalypse.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_archangel.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_beast_allnew.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_bishop.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_black_bolt.png',
    ]
    
    await ctx.send(random.choice(CHAMPS))
      
