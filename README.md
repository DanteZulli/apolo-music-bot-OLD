<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Unlicense License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/DanteZulli/apolo-music-bot">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Apolo Music Bot</h3>

  <p align="center">
     A self-hosted, feature-rich music bot for Discord, built with Python. Stream your favorite tunes seamlessly!
    <br />
    <a href="https://github.com/DanteZulli/apolo-music-bot"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/DanteZulli/apolo-music-bot/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/DanteZulli/apolo-music-bot/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

## Requirements

- Python 3.8 or higher
- FFmpeg installed on your system (if not using Docker)
- Discord Bot Token
- Privileged Intents enabled in the Discord Developer Portal

## Bot Setup on Discord Developer Portal

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application and configure the bot
   > **Note:** Feel free to customize your bot's name, avatar, and description to match your preferences!
3. In the "Bot" section, enable the following **Privileged Gateway Intents**:
   - Presence Intent
   - Server Members Intent
   - Message Content Intent
4. In the "OAuth2" section, generate an invite URL with the following permissions:
   - **Scopes**: `bot`, `applications.commands`
   - **Bot Permissions**:
     - View Channels
     - Send Messages
     - Connect
     - Speak
     - Use Voice Activity
5. Use the generated URL to invite the bot to your server

## Project Setup

1. Install the dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the root of the project to store your environment variables. Add your Discord bot token as follows:
```env
DISCORD_TOKEN=your_discord_token_here
```

3. Run the bot:
```bash
python main.py
```

## Running with Docker

### Using Docker Compose (Recommended)

1. Ensure Docker and Docker Compose are installed.
2. Create a `.env` file in the root of the project to store your environment variables. Add your Discord bot token as follows:
```env
DISCORD_TOKEN=your_discord_token_here
```
3. Run the bot with Docker Compose::
```bash
docker-compose up -d
```

### Using Docker Directly

1. Build the Docker image:
```bash
docker build -t apolo-music-bot .
```

2. Run the container:
```bash
docker run -d \
  --name apolo-music-bot \
  -e DISCORD_TOKEN=your_token_here \
  -e COMMAND_PREFIX=! \
  apolo-music-bot
```

## Usage

- `!join`: Connects the bot to your voice channel.
- `!leave`: Disconnects the bot from the voice channel.
- `!play [url]`:  Plays a song from YouTube or adds it to the queue.
- `!pause`: Pauses the current playback.
- `!resume`: Resumes the paused playback.
- `!stop`: Stops the playback and clears the queue.
- `!skip`: Skips the current song and moves to the next one in the queue.
- `!queue`: Displays the current song queue.
- `!help`: Displays a list of available commands and their usage.

## Roadmap

For a detailed list of planned features and improvements, please see our [TODO.md](TODO.md) file.

## Acknowledgments

* [discord.py](https://discordpy.readthedocs.io/en/stable/) - The Python library for Discord API
* [Discord Developer Portal](https://discord.com/developers/applications) - For bot creation and management
* [MIT License](https://opensource.org/licenses/MIT) - For licensing information

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.


<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/DanteZulli/apolo-music-bot?style=for-the-badge
[contributors-url]: https://github.com/DanteZulli/apolo-music-bot/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/DanteZulli/apolo-music-bot?style=for-the-badge
[forks-url]: https://github.com/DanteZulli/apolo-music-bot/network/members
[stars-shield]: https://img.shields.io/github/stars/DanteZulli/apolo-music-bot?style=for-the-badge
[stars-url]: https://github.com/DanteZulli/apolo-music-bot/stargazers
[issues-shield]: https://img.shields.io/github/issues/DanteZulli/apolo-music-bot.svg?style=for-the-badge
[issues-url]: https://github.com/DanteZulli/apolo-music-bot/issues
[license-shield]: https://img.shields.io/github/license/DanteZulli/apolo-music-bot.svg?style=for-the-badge
[license-url]: https://github.com/DanteZulli/apolo-music-bot/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/dante-zulli/
