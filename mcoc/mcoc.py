from redbot.core import commands, checks, Config
import discord
import random
# from .mdtembed import Embed

class Mcoc(commands.Cog):
  """Mcoc"""
  
  def __init__(self):
    self.config = Config.get_conf(self, 200730042020, force_registration=True)
    
  @commands.group(invoke_without_command=True)
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
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_black_panther.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_black_panther_cw.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_black_widow.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_black_widow_timely.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_black_widow_movie.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_blade.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_cable.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_captain_america.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_captainamerica_infinitywar.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_capamerica_wwii.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_captain_marvel_movie.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_captain_marvel.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_carnage.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_civilwarrior.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_colossus.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_corvusglaive.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_ghost_rider_cosmic.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_crossbones.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_cullobsidian.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_cyclops_90s.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_cyclops.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_daredevil_netflix.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_daredevil.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_darkhawk.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_deadpool.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_deadpool_xforce.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_diablo.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_doctordoom.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_doc_ock.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_doctor_strange.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_brother_voodoo.png',
      'https://auntm.ai/resources/ui/uigacha/featured/gachachaseprize_256x256_domino.png'
      
    ]
    
    await ctx.send(random.choice(CHAMPS))
      
