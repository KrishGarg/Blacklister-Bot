from discord.ext import commands
import sqlite3

class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.mention_everyone:
            return
        if self.bot.user.mentioned_in(message):
            db = sqlite3.connect('main.db')
            c = db.cursor()
            c.execute("SELECT prefix FROM prefixes WHERE guild_id = ?", (message.guild.id, ))
            pref = c.fetchone()
            db.close()
            if not pref:
                await message.channel.send("There was some issue when looking at this server's prefix! You can fix it by running `>>prefix` and it that doesn't work, just re=invite the bot!")
                return
            await message.channel.send(f"My prefix for this server is `{pref[0]}`.")

def setup(bot):
    bot.add_cog(Other(bot))