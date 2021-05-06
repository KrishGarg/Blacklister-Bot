import discord
from discord.ext import commands
import DiscordUtils

class HelpCommand(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def help(self, ctx):
    blacklist_embed = discord.Embed(title="↓ BlackList Commands ↓",color=0xffff00)
    blacklist_embed.add_field(name='Adding words/phrases to the blacklist:',value='''
```fix
>>add <word/phrase>
or
>>addword <word/phrase>
```
    ''',inline=False)
    blacklist_embed.add_field(name='Removing words/phrases from the blacklist:',value='''
```fix
>>del <word/phrase>
or
>>delete <word/phrase>
or
>>deleteword <word/phrase>
```
    ''',inline=False)
    blacklist_embed.add_field(name='Viewing all the blacklisted words:',value='''
```fix
>>list
or
>>blacklist
```
    ''',inline=False)
    blacklist_embed.add_field(name='Important Points:',value='''
**<> = Required Arguments**
**Administrator permission to run any above command.**
    ''')

    other_embed = discord.Embed(title='↓ Miscellaneous Commands ↓',color=0xffff00)
    other_embed.add_field(name='Ping Command:',value='''
```fix
>>ping
```
    ''',inline=False)
    other_embed.add_field(name='Invite Command:',value='''
```fix
>>invite
```
    ''',inline=False)

    paginator = DiscordUtils.Pagination.AutoEmbedPaginator(ctx)
    embeds = [blacklist_embed, other_embed]
    await paginator.run(embeds)

def setup(bot):
  bot.add_cog(HelpCommand(bot))