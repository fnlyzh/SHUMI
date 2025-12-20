from pathlib import Path
import os
import dotenv
from .models import DataConfig, DiscordConfig, CalendarConfig

dotenv.load_dotenv()

def _get_env(key: str) -> Path:
	path_str = os.getenv(key)
	if path_str is None:
		raise RuntimeError(f"{key} is not set in .env")
	return Path(path_str)

def load_integration_config() -> DataConfig:
	cfg_path = _get_env("DATA_CONFIG_PATH")
	return DataConfig.from_json(cfg_path)


def load_data_path() -> Path:
	data_path = _get_env("DATA_PATH")
	return data_path


def load_calendar_config() -> CalendarConfig:
	cfg_path = _get_env("CALENDAR_CONFIG_PATH")
	return CalendarConfig.from_json(cfg_path)


def load_discord_config() -> DiscordConfig:
	cfg_path = _get_env("DISCORD_CONFIG_PATH")
	return DiscordConfig.from_json(cfg_path)
