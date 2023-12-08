import discord
from discord.ext import commands
import youtube_dl
import os

bot = commands.Bot(command_prefix='!')

def run_command(command):
    try:
        os.system(command)
    except Exception as e:
        print(f"Error running command: {e}")

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

@bot.command(name='run', help='Run a command in the terminal')
async def run(ctx, *, command):
    run_command(command)
    await ctx.send(f'Command executed: `{command}`')

bot.run('YOUR_BOT_TOKEN')
