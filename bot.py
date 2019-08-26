from config import bot_token
import discord
from discord.ext import commands
import os

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, filename):
        if not discord.opus.is_loaded():
            discord.opus.load_opus("opuslib")

        ffmpeg = r"C:\Program Files (x86)\ffmpeg-20190813-8cd96e1-win64-static\bin\ffmpeg.exe"
        filepath = "VoiceFiles/{}.mp3".format(filename)
        if not os.path.isfile(filepath):
            return await ctx.send('file not found')
        try:
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filepath, executable=ffmpeg))
        except discord.errors.ClientException as e:
            # this catches  ffmpeg file not being found
            return await ctx.send(e)

        try:
            ctx.voice_client.play(source)
        except AttributeError:
            return await ctx.send('Voice channel not found')


        await ctx.send('Now playing: {}'.format(filename))

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Relatively simple music bot example')

@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')

bot.add_cog(Music(bot))
bot.run(bot_token)