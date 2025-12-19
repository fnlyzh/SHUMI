import json
import os
import pytz
from dataclasses import dataclass
import dotenv

from typing import Dict

@dataclass(frozen=True)
class DiscordConfig:
	channels: Dict[str, Dict[str, int]]
	study_role_id: int
	timezone: str
	tz: pytz.BaseTzInfo

	@staticmethod
	def from_json(path: str) -> "DiscordConfig":
		"""
		Load config from a JSON file
		"""
		if not os.path.exists(path):
			raise FileNotFoundError(f"Personal config JSON not found at {path}")

		with open(path, "r", encoding="utf-8") as f:
			data = json.load(f)

		return DiscordConfig(
			channels=data["voice_channels"],
			study_role_id=data["study_role_id"],
			timezone=data["timezone"],
			tz=pytz.timezone(data["timezone"]),
		)

def load_discord_config() -> DiscordConfig:
	dotenv.load_dotenv()
	cfg_path = os.getenv("DISCORD_CONFIG_PATH")
	if cfg_path is None:
		raise RuntimeError("DISCORD_CONFIG_PATH is not set in .env")
	return DiscordConfig.from_json(cfg_path)