from discord.ext import commands

class Logging(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  '''
  Soon™
  '''

def setup(bot):
  bot.add_cog(Logging(bot))