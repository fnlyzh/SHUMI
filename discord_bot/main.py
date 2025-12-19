import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

from discord_modules.record_study import record_study_on_voice

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
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
    await record_study_on_voice(bot, member, before, after)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)