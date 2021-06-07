import discord
from discord.ext import commands
import sqlite3
import random

replies = [
  "You said a no-no word!",
  "The message sent consisted of a blacklisted word.",
  "Man! Check your message. It contained a blacklisted word!"
]

'''
  More replies will be added s00n™
'''

db = sqlite3.connect('main.db')
c = db.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS blacklist (
      guild_id INTEGER,
      words TEXT
    )
  """)

db.commit()
db.close()

class BlackListing(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  async def if_blacklisted_word_in_message_logic(self, msgObj):
    if msgObj.author.bot:
      return

    if isinstance(msgObj.author, discord.User):
      return

    if msgObj.author.guild_permissions.administrator:
      return

    db = sqlite3.connect('main.db')
    c = db.cursor()
    c.execute("SELECT prefix FROM prefixes WHERE guild_id = ?", (msgObj.guild.id,))
    pref = c.fetchone()
    pref = pref[0]

    if (msgObj.content.startswith(f"{pref}addword") or msgObj.content.startswith(f"{pref}deleteword") or msgObj.content.startswith(f"{pref}add") or msgObj.content.startswith(f"{pref}delete")) and msgObj.author.guild_permissions.administrator:
      db.close()
      return
    
    c.execute("SELECT words FROM blacklist WHERE guild_id = ?",(msgObj.guild.id,))

    data = c.fetchall()
    db.close()

    if not data:
      return

    else:
      words_in_one_str = data[0][0]

      words_arr = words_in_one_str.split(",")
      words_arr.pop(len(words_arr)-1)

      msg = msgObj.content.lower()

      if '*' in msg:
        msg = msg.replace('*','')

      if '_' in msg:
        msg = msg.replace('_','')

      # The invisible character
      if '​' in msg:
        msg = msg.replace('​','')

      if ' ' in msg:
        msg = msg.replace(' ','')

      if any(word.lower() in msg for word in words_arr):
        await msgObj.delete()
        await msgObj.channel.send(random.choice(replies),delete_after=3)
        return

      return

  @commands.Cog.listener()
  async def on_message(self, message):
    await self.if_blacklisted_word_in_message_logic(message)

  @commands.Cog.listener()
  async def on_message_edit(self, before, after):
    await self.if_blacklisted_word_in_message_logic(after)
    try:
      if (before.pinned and not after.pinned) or (not before.pinned and after.pinned):
          return
      await self.bot.process_commands(after)
    except:
        pass

  @commands.command(aliases=['blacklist','list'])
  @commands.has_permissions(administrator=True)
  async def _blacklist(self, ctx):
    try:
      db = sqlite3.connect('main.db')
      c = db.cursor()

      c.execute('SELECT words FROM blacklist WHERE guild_id = ?', (ctx.guild.id,))
      data = c.fetchall()

      db.close()

      if not data:
        await ctx.send("There are no words set for this server.")
        return

      else:
        datatosend = str(data[0][0])
        dts = datatosend.split(',')
        d = "||"
        for x in dts:
          if not x == "":
            d += f"**{x}**\n" 
        d += "||"
        await ctx.send(f"All the words set as blacklisted for this server are as follows:- \n{d}")
    except Exception as ex:
      print(ex)

  @commands.command(aliases=['addword','add'])
  @commands.has_permissions(administrator=True)
  async def _addword(self, ctx, *, word):
    db = sqlite3.connect('main.db')
    c = db.cursor()

    c.execute("SELECT * FROM blacklist WHERE guild_id = ?", (ctx.guild.id,))
    data = c.fetchall()

    if not data:
      c.execute("INSERT INTO blacklist VALUES (?,?)", (ctx.guild.id,word+','))
      db.commit()

    else:
      oldwords = data[0][1]
      newwords = oldwords + word + ','
      c.execute("UPDATE blacklist SET words = ? WHERE guild_id = ?", (newwords, ctx.guild.id))
      db.commit()

    db.close()

    await ctx.send(f"Added ||{word}|| to the blacklist!")
    return

  @commands.command(aliases=['deleteword','delete','del'])
  @commands.has_permissions(administrator=True)
  async def _deleteword(self, ctx,*, word):
    db = sqlite3.connect('main.db')
    c = db.cursor()

    c.execute("SELECT * FROM blacklist WHERE guild_id = ?", (ctx.guild.id,))
    data = c.fetchall()

    if not data:
      await ctx.send("There are no words set for this guild!")
      db.close()
      return

    else:
      oldwords = data[0][1]
      oldwords_list = oldwords.split(",")
      oldwords_list.pop(len(oldwords_list)-1)

      if not word in oldwords_list:
        await ctx.send("Ayo I don't see the word in the blacklist! Did you mess up the capitalizations? Check the `>>blacklist` to recheck the capitalizations!")
        db.close()
        return

      if len(oldwords_list) == 1:
        c.execute("DELETE FROM blacklist WHERE guild_id = ?", (ctx.guild.id,))
        db.commit()
        
      else:
        for words in oldwords_list[:]:
          if word == words:
            oldwords_list.remove(words)

        newwords = oldwords_list[:]
        newwords_str = ','.join(newwords)+','

        c.execute("UPDATE blacklist SET words = ? WHERE guild_id = ?", (newwords_str, ctx.guild.id))
        db.commit()

      await ctx.send(f"Done! Removed `{word}` from the blacklist! Run `>>blacklist` to check.")

    db.close()
    return

  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    if isinstance(error, commands.CommandNotFound):
      await ctx.send("I don't think thats a valid command. Check again!")
      return

    if isinstance(error, commands.MissingPermissions):
      await ctx.send("You ain't got enough permissions!")
      return

    if isinstance(error, commands.MissingRequiredArgument):
      await ctx.send("Yo check the syntax of the command again. I think you missed some arguments!")
      return

    if isinstance(error, commands.BadArgument):
      await ctx.send("I think the argument you sent me was/were wrong!")
      return

    if isinstance(error, commands.CommandError):
      await ctx.send("Some error happened! Try again later!")
      return

def setup(bot):
  bot.add_cog(BlackListing(bot))