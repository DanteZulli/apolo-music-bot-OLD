import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from music_player import MusicPlayer

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot setup with required intents
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

# Get command prefix from environment variables, default to '!' if not set
COMMAND_PREFIX = os.getenv('COMMAND_PREFIX', '!')
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.music_player = MusicPlayer()

    @commands.command(name='join', help='Conecta el bot al canal de voz')
    async def join(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send('¡Necesitas estar en un canal de voz primero!')
            return
        
        channel = ctx.message.author.voice.channel
        if ctx.guild.voice_client not in self.bot.voice_clients:
            await channel.connect()
            await ctx.send(f'Conectado a {channel}')

    @commands.command(name='leave', help='Desconecta el bot del canal de voz')
    async def leave(self, ctx):
        if ctx.guild.voice_client:
            await ctx.guild.voice_client.disconnect()
            await ctx.send('¡Hasta luego!')

    @commands.command(name='play', help='Reproduce una canción de YouTube')
    async def play(self, ctx, *, url):
        if not ctx.message.author.voice:
            await ctx.send('¡Necesitas estar en un canal de voz primero!')
            return

        if not ctx.guild.voice_client:
            await ctx.message.author.voice.channel.connect()

        audio_info = await self.music_player.get_audio_info(url)
        if audio_info:
            self.music_player.add_to_queue(audio_info)
            await ctx.send(f'🎵 Añadido a la cola: {audio_info["title"]}')
            if not self.music_player.is_playing(ctx.guild.voice_client):
                await self.music_player.play_next(ctx.guild.voice_client)
        else:
            await ctx.send('❌ No se pudo reproducir la canción. Verifica la URL.')

    @commands.command(name='pause', help='Pausa la reproducción')
    async def pause(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            await ctx.send('⏸ Música pausada')

    @commands.command(name='resume', help='Reanuda la reproducción')
    async def resume(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client and voice_client.is_paused():
            voice_client.resume()
            await ctx.send('▶ Reproducción reanudada')

    @commands.command(name='stop', help='Detiene la reproducción')
    async def stop(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client:
            voice_client.stop()
            self.music_player.clear_queue()
            await ctx.send('⏹ Reproducción detenida')

    @commands.command(name='skip', help='Salta a la siguiente canción')
    async def skip(self, ctx):
        if self.music_player.skip(ctx.guild.voice_client):
            await ctx.send('⏭ Saltando a la siguiente canción...')
            await self.music_player.play_next(ctx.guild.voice_client)
        else:
            await ctx.send('❌ No hay ninguna canción reproduciéndose.')

    @commands.command(name='queue', help='Muestra la cola de reproducción')
    async def queue(self, ctx):
        queue = self.music_player.get_queue()
        if not queue:
            await ctx.send('📋 La cola está vacía.')
            return

        queue_text = '📋 Cola de reproducción:\n'
        for i, track in enumerate(queue, 1):
            queue_text += f'{i}. {track["title"]}\n'
        await ctx.send(queue_text)

@bot.event
async def on_ready():
    print(f'{bot.user} ha iniciado sesión!')
    await bot.add_cog(Music(bot))

def main():
    bot.run(TOKEN)

if __name__ == '__main__':
    main()