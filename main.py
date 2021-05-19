import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from cogs.ServerPrefix import get_prefix

load_dotenv()

bot = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all(), help_command=None, allowed_mentions=discord.AllowedMentions(everyone=False))
bot.owner_ids = {506093256501755904, 453875226757955585}

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('Prefix: >>'))
    print(f"Logged in as {bot.user.name}#{bot.user.discriminator}")


if __name__ == '__main__':
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f"Loaded {filename[:-3]}")

bot.run(os.getenv("TOKEN"))
