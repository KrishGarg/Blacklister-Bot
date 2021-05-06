from discord.ext import commands
import sqlite3

db = sqlite3.connect('main.db')
c = db.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS prefixes (
    guild_id INTEGER,
    prefix TEXT
)''')
db.commit()
db.close()


def get_prefix(client, message):
    db = sqlite3.connect('main.db')
    c = db.cursor()
    c.execute('SELECT * FROM prefixes WHERE guild_id = ?', (message.guild.id,))
    prefixdata = c.fetchone()

    if not prefixdata:
        c.execute('INSERT INTO prefixes VALUES (?, ?)', (message.guild.id, '>>'))
        db.commit()
        db.close()
        return '>>'

    else:
        db.close()
        return prefixdata[1]


class ServerPrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        db = sqlite3.connect('main.db')
        c = db.cursor()
        c.execute('INSERT INTO prefixes VALUES (?, ?)', (guild.id, '>>'))
        db.commit()
        db.close()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        db = sqlite3.connect('main.db')
        c = db.cursor()
        c.execute('DELETE FROM prefixes WHERE guild_id = ?', (guild.id, ))
        db.commit()
        db.close()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, new_prefix=None):
        db = sqlite3.connect('main.db')
        c = db.cursor()
        c.execute('SELECT prefix FROM prefixes WHERE guild_id = ?', (ctx.guild.id, ))
        old_prefix = c.fetchone()
        if new_prefix is None:
            await ctx.send(f'The prefix for this server is `{old_prefix[0]}`.')
        else:
            c.execute('UPDATE prefixes SET prefix = ? WHERE guild_id = ?', (new_prefix, ctx.guild.id))
            db.commit()
            db.close()
            await ctx.send(f"The prefix for this server has been changed from `{old_prefix[0]}` to `{new_prefix}`.")

def setup(bot):
    bot.add_cog(ServerPrefix(bot))
