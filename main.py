import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from music_player import MusicPlayer
from discord import Embed, Color

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
            embed = Embed(description='🚫 ¡Necesitas estar en un canal de voz primero!', color=Color.red())
            await ctx.send(embed=embed)
            return
        
        channel = ctx.message.author.voice.channel
        if ctx.guild.voice_client not in self.bot.voice_clients:
            await channel.connect()
            embed = Embed(description=f'✅ Conectado a {channel}', color=Color.green())
            await ctx.send(embed=embed)

    @commands.command(name='leave', help='Desconecta el bot del canal de voz')
    async def leave(self, ctx):
        if ctx.guild.voice_client:
            await ctx.guild.voice_client.disconnect()
            embed = Embed(description='👋 ¡Hasta luego!', color=Color.blue())
            await ctx.send(embed=embed)

    @commands.command(name='play', help='Reproduce una canción de YouTube')
    async def play(self, ctx, *, url):
        if not ctx.message.author.voice:
            embed = Embed(description='🚫 ¡Necesitas estar en un canal de voz primero!', color=Color.red())
            await ctx.send(embed=embed)
            return

        if not ctx.guild.voice_client:
            await ctx.message.author.voice.channel.connect()

        audio_info = await self.music_player.get_audio_info(url)
        if audio_info:
            self.music_player.add_to_queue(audio_info)
            embed = Embed(title='🎵 Canción Añadida', color=Color.green())
            embed.add_field(name='Título', value=audio_info['title'], inline=False)
            embed.add_field(name='Duración', value=f"{int(audio_info['duration'] // 60)}:{int(audio_info['duration'] % 60):02d}", inline=True)
            await ctx.send(embed=embed)
            if not self.music_player.is_playing(ctx.guild.voice_client):
                await self.music_player.play_next(ctx.guild.voice_client)
        else:
            embed = Embed(description='❌ No se pudo reproducir la canción. Verifica la URL.', color=Color.red())
            await ctx.send(embed=embed)

    @commands.command(name='pause', help='Pausa la reproducción')
    async def pause(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            embed = Embed(description='⏸ Música pausada', color=Color.blue())
            await ctx.send(embed=embed)

    @commands.command(name='resume', help='Reanuda la reproducción')
    async def resume(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client and voice_client.is_paused():
            voice_client.resume()
            embed = Embed(description='▶ Reproducción reanudada', color=Color.green())
            await ctx.send(embed=embed)

    @commands.command(name='stop', help='Detiene la reproducción')
    async def stop(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client:
            voice_client.stop()
            self.music_player.clear_queue()
            embed = Embed(description='⏹ Reproducción detenida', color=Color.red())
            await ctx.send(embed=embed)

    @commands.command(name='skip', help='Salta a la siguiente canción')
    async def skip(self, ctx):
        if self.music_player.skip(ctx.guild.voice_client):
            embed = Embed(description='⏭ Saltando a la siguiente canción...', color=Color.blue())
            await ctx.send(embed=embed)
            await self.music_player.play_next(ctx.guild.voice_client)
        else:
            embed = Embed(description='❌ No hay ninguna canción reproduciéndose.', color=Color.red())
            await ctx.send(embed=embed)

    @commands.command(name='queue', help='Muestra la cola de reproducción')
    async def queue(self, ctx):
        queue = self.music_player.get_queue()
        if not queue:
            embed = Embed(description='📋 La cola está vacía.', color=Color.blue())
            await ctx.send(embed=embed)
            return

        embed = Embed(title='📋 Cola de Reproducción', color=Color.blue())
        for i, track in enumerate(queue, 1):
            duration = f"{int(track['duration'] // 60)}:{int(track['duration'] % 60):02d}"
            embed.add_field(name=f'{i}. {track["title"]}', value=f'⏱ Duración: {duration}', inline=False)
        await ctx.send(embed=embed)

@bot.event
async def on_ready():
    print(f'{bot.user} ha iniciado sesión!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'música | {COMMAND_PREFIX}help'))
    await bot.add_cog(Music(bot))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = Embed(description=f'❌ Comando no encontrado. Usa {COMMAND_PREFIX}help para ver los comandos disponibles.', color=Color.red())
        await ctx.send(embed=embed)

class CustomHelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = Embed(title='🎵 Comandos de Apolo Music Bot', 
                     description='¡Aquí tienes una lista de todos los comandos disponibles!',
                     color=Color.blue())
        
        for cog in mapping:
            if cog:
                filtered = await self.filter_commands(cog.get_commands())
                command_list = []
                for command in filtered:
                    command_list.append(f'`{COMMAND_PREFIX}{command.name}`: {command.help}')
                if command_list:
                    cog_name = cog.qualified_name
                    embed.add_field(name=f'🎮 {cog_name}',
                                  value='\n'.join(command_list),
                                  inline=False)
        
        embed.set_footer(text=f'Usa {COMMAND_PREFIX}help <comando> para más información sobre un comando específico')
        await self.get_destination().send(embed=embed)
    
    async def send_command_help(self, command):
        embed = Embed(title=f'ℹ️ Comando: {COMMAND_PREFIX}{command.name}',
                     description=command.help,
                     color=Color.blue())
        if command.aliases:
            embed.add_field(name='📝 Aliases', value=', '.join(command.aliases), inline=False)
        await self.get_destination().send(embed=embed)

bot.help_command = CustomHelpCommand()

def main():
    bot.run(TOKEN)

if __name__ == '__main__':
    main()