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

    info_embed = discord.Embed(title='↓ Basic Information ↓', color=0xffff00, description='''
• **The bot will ignore the blacklisted words sent by members with Administrator permission.**
• **Code to the bot's repository:** [Click Me!](https://github.com/KrishGarg/Blacklister-Bot)
• **Link to the support server:** [Click Me!](https://discord.gg/258wAYANQz)
• **All the commands are on the following pages.**
''')

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
    other_embed.add_field(name='Prefix Changing Command:',value='''
```fix
{0}prefix <new prefix>
```
**Note: If the prefix command is ran without the new prefix, it will show the current server prefix.**
    '''.format(pref), inline=False)

    paginator = DiscordUtils.Pagination.AutoEmbedPaginator(ctx)
    embeds = [info_embed, blacklist_embed, other_embed]
    await paginator.run(embeds)

def setup(bot):
  bot.add_cog(HelpCommand(bot))