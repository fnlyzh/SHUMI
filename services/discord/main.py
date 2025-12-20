import discord
from discord.ext import commands
import logging

from .api_setup.setup import load_token, setup_logging
from config.handler import load_discord_config
from .discord_modules.record_time import record_voice_time

def create_bot(cfg) -> commands.Bot:
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    # may need to enable more intents if I tick more in the discord developers page

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"{bot.user.name} is ready.")

    @bot.event
    async def on_voice_state_update(member, before, after):
        await record_voice_time(bot, cfg, member, before, after)

    return bot

def main():
    cfg = load_discord_config()
    token = load_token()
    
    handler = setup_logging()
    bot = create_bot(cfg)

    bot.run(token, log_handler=handler, log_level=logging.DEBUG)

if __name__ == "__main__":
    main()