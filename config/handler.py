from pathlib import Path
import os
import json
import dotenv
from .models import DataConfig, DiscordConfig, CalendarConfig, TasksConfig

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


def load_tasks_config() -> TasksConfig:
	cfg_path = _get_env("TASKS_CONFIG_PATH")
	return TasksConfig.from_json(cfg_path)

def save_tasks_config(tasklist_name: str, tasklist_id: str) -> TasksConfig:
	cfg_path = _get_env("TASKS_CONFIG_PATH")

	raw = json.loads(cfg_path.read_text(encoding="utf-8"))

	raw.setdefault("tasklists", {})
	raw["tasklists"][tasklist_name] = tasklist_id

	cfg_path.write_text(json.dumps(raw, indent=4))

	return TasksConfig.from_json(cfg_path)


def load_discord_config() -> DiscordConfig:
	cfg_path = _get_env("DISCORD_CONFIG_PATH")
	return DiscordConfig.from_json(cfg_path)
