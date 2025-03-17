import asyncio
import yt_dlp
import discord

class MusicPlayer:
    def __init__(self):
        self.queue = []
        self.current = None
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'noplaylist': True
        }
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

    async def get_audio_info(self, url):
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if 'entries' in info:
                    info = info['entries'][0]
                return {
                    'url': info['url'],
                    'title': info['title'],
                    'duration': info['duration']
                }
        except Exception as e:
            print(f'Error extracting info: {str(e)}')
            return None

    async def play_next(self, voice_client):
        if not voice_client.is_playing() and self.queue:
            self.current = self.queue.pop(0)
            audio_source = discord.FFmpegPCMAudio(
                self.current['url'],
                **self.FFMPEG_OPTIONS
            )
            voice_client.play(
                audio_source,
                after=lambda e: asyncio.run_coroutine_threadsafe(
                    self.play_next(voice_client),
                    voice_client.loop
                )
            )
            return True
        return False

    def add_to_queue(self, track):
        self.queue.append(track)

    def clear_queue(self):
        self.queue.clear()
        self.current = None

    def get_queue(self):
        return self.queue

    def is_playing(self, voice_client):
        return voice_client and voice_client.is_playing()

    def skip(self, voice_client):
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            return True
        return False