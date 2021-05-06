import discord
from discord.ext import commands
import DiscordUtils
import sqlite3

class HelpCommand(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def help(self, ctx):
    db = sqlite3.connect('main.db')
    c = db.cursor()
    c.execute("SELECT prefix FROM prefixes WHERE guild_id = ?", (ctx.guild.id, ))
    pref = c.fetchone()
    pref = pref[0]
    db.close()

    blacklist_embed = discord.Embed(title="↓ BlackList Commands ↓",color=0xffff00)
    blacklist_embed.add_field(name='Adding words/phrases to the blacklist:',value='''
```fix
{0}add <word/phrase>
or
{0}addword <word/phrase>
```
    '''.format(pref), inline=False)
    blacklist_embed.add_field(name='Removing words/phrases from the blacklist:',value='''
```fix
{0}del <word/phrase>
or
{0}delete <word/phrase>
or
{0}deleteword <word/phrase>
```
    '''.format(pref), inline=False)
    blacklist_embed.add_field(name='Viewing all the blacklisted words:',value='''
```fix
{0}list
or
{0}blacklist
```
    '''.format(pref), inline=False)
    blacklist_embed.add_field(name='Important Points:',value='''
**<> = Required Arguments**
**Administrator permission to run any above command.**
    ''')

    other_embed = discord.Embed(title='↓ Miscellaneous Commands ↓',color=0xffff00)
    other_embed.add_field(name='Ping Command:',value='''
```fix
{0}ping
```
    '''.format(pref), inline=False)
    other_embed.add_field(name='Invite Command:',value='''
```fix
{0}invite
```
    '''.format(pref), inline=False)

    paginator = DiscordUtils.Pagination.AutoEmbedPaginator(ctx)
    embeds = [blacklist_embed, other_embed]
    await paginator.run(embeds)

def setup(bot):
  bot.add_cog(HelpCommand(bot))