from discord.ext import commands

class SupportServerStuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        to_be_publishing_channels = [839821581760331797, 839820997712674826]
        if message.channel.id in to_be_publishing_channels:
            await message.publish()

def setup(bot):
    bot.add_cog(SupportServerStuff(bot))