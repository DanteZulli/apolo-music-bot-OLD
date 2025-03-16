# Apolo Music Bot

Un bot de música para Discord desarrollado en Python.

## Requisitos

- Python 3.8 o superior
- FFmpeg instalado en el sistema
- Token de Discord Bot

## Configuración

1. Instala las dependencias:
```bash
pip install -r requirements.txt
```

2. Crea un archivo `.env` en la raíz del proyecto y añade tu token de Discord:
```
DISCORD_TOKEN=tu_token_aqui
```

3. Ejecuta el bot:
```bash
python main.py
```

## Comandos

- `!join`: Conecta el bot al canal de voz
- `!leave`: Desconecta el bot del canal de voz
- `!play [url]`: Reproduce una canción de YouTube
- `!pause`: Pausa la reproducción
- `!resume`: Reanuda la reproducción
- `!stop`: Detiene la reproducción

## Notas

- Asegúrate de tener FFmpeg instalado en tu sistema
- El bot necesita permisos de voz en el servidor de Discord
- Usa el prefijo '!' para todos los comandos