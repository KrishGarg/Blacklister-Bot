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
    embed1.add_field(name="↓ Bot's Invite Link ↓",value='''
[Click me to open
the invite link in
your browser!](https://discord.com/oauth2/authorize?client_id=796422925502775378&scope=bot&permissions=355400)
''',inline=True)
    embed1.add_field(name='↓ Support Server Invite Link ↓',value='''
[Click me to join
the server!](https://discord.gg/258wAYANQz)
    ''',inline=True)
    await ctx.send(embed=embed1)

def setup(bot):
  bot.add_cog(Misc(bot))