import discord
from discord.ext import commands

class Misc(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def ping(self, ctx):
    await ctx.send(f'Pong! `{round(self.bot.latency * 1000)}ms` is the latency!')

  @commands.command()
  async def invite(self, ctx):
    embed1 = discord.Embed(title='Invite Me To Your Server!',color=0xffff00)
    embed1.add_field(name='↓ Invite Link ↓',value='''
[Click me to open
the invite link in
your browser!](https://discord.com/api/oauth2/authorize?client_id=796422925502775378&permissions=387136&scope=bot)
''',inline=True)
    await ctx.send(embed=embed1)

def setup(bot):
  bot.add_cog(Misc(bot))