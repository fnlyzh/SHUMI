import json
import os
from dataclasses import dataclass
import dotenv

from typing import Dict, List

@dataclass(frozen=True)
class DataConfig:
	merge_gap_minutes: int
	min_duration_minutes: int

	@staticmethod
	def from_json(path: str) -> "DataConfig":
		"""
		Load config from a JSON file
		"""
		if not os.path.exists(path):
			raise FileNotFoundError(f"Personal config JSON not found at {path}")

		with open(path, "r", encoding="utf-8") as f:
			data = json.load(f)

		return DataConfig(
			merge_gap_minutes=data["merge_gap_minutes"],
			min_duration_minutes=data["min_duration_minutes"],
		)

def load_integration_config():
	dotenv.load_dotenv()
	cfg_path = os.getenv("DATA_CONFIG_PATH")
	if cfg_path is None:
		raise RuntimeError("DATA_CONFIG_PATH is not set in .env")
	return DataConfig.from_json(cfg_path)

def load_data_path() -> str:
	dotenv.load_dotenv()
	data_path = os.getenv("DATA_PATH")
	if data_path is None:
		raise RuntimeError("DATA_PATH is not set in .env")
	return data_path