import discord
from discord.ext import commands
import youtube_dl

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='play', help='Play music from YouTube')
async def play(ctx, url):
    channel = ctx.message.author.voice.channel
    voice_channel = await channel.connect()

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        voice_channel.play(discord.FFmpegPCMAudio(url2), after=lambda e: print('done', e))

    await ctx.send(f'**Now playing:** {info["title"]}')

@bot.command(name='stop', help='Stop playing music and disconnect')
async def stop(ctx):
    voice_channel = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_channel.is_playing():
        voice_channel.stop()
    await voice_channel.disconnect()

bot.run('YOUR_BOT_TOKEN')
