from .votesystem import VoteSystem

def setup(bot):
  _ = VoteSystem
  bot.add_cog(_(bot))