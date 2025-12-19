import os
import logging
from ..config import DiscordConfig

from dotenv import load_dotenv
load_dotenv()

def load_token():
    token = os.getenv("DISCORD_TOKEN")
    if token is None:
        raise RuntimeWarning("DISCORD_TOKEN not set in .env")
    return token

def setup_logging(log_file="discord.log") -> logging.FileHandler:
    handler = logging.FileHandler(filename=log_file, encoding="utf-8", mode="w")
    return handler