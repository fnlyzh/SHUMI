import json
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime, date
import pytz
from typing import Dict, List


@dataclass(frozen=True)
class DataConfig:
	merge_gap_minutes: int
	min_duration_minutes: int

	@staticmethod
	def from_json(path: Path) -> "DataConfig":
		"""
		Load config from a JSON file
		"""
		if not path.exists():
			raise FileNotFoundError(f"Data config JSON not found at {path}")
		
		data = json.loads(path.read_text(encoding="UTF-8"))

		return DataConfig(
			merge_gap_minutes=data["merge_gap_minutes"],
			min_duration_minutes=data["min_duration_minutes"],
		)


@dataclass(frozen=True)
class CalendarConfig:
	calendars: Dict[str, str]
	recurrence_color_id: str
	term_start_monday: date
	term_weeks: int
	break_weeks: List[int]
	timezone: str
	tz: pytz.BaseTzInfo

	@staticmethod
	def from_json(path: Path) -> "CalendarConfig":
		"""
		Load config from a JSON file
		"""
		if not path.exists():
			raise FileNotFoundError(f"Calendar config JSON not found at {path}")
		
		data = json.loads(path.read_text(encoding="UTF-8"))

		return CalendarConfig(
			calendars=data["calendars"],
			recurrence_color_id=data["recurrence_color_id"],
			term_start_monday=datetime.strptime(data["term_start_monday"], "%Y-%m-%d").date(),
			term_weeks=data["term_weeks"],
			break_weeks=data["break_weeks"],
			timezone=data["timezone"],
			tz=pytz.timezone(data["timezone"]),
		)


@dataclass(frozen=True)
class TasksConfig:
	tasklists: Dict[str, str]
	rate_limit: Dict[str, int]

	@staticmethod
	def from_json(path: Path) -> "TasksConfig":
		"""
		Load config from a JSON file
		"""
		if not path.exists():
			raise FileNotFoundError(f"Tasks config JSON not found at {path}")
		
		data = json.loads(path.read_text(encoding="UTF-8"))

		return TasksConfig(
			tasklists=data["tasklists"],
			rate_limit=data.get("rate_limit", {"batch_size": 3, "sleep_seconds": 3})
		)


@dataclass(frozen=True)
class DiscordConfig:
	channels: Dict[str, Dict[str, int]]
	study_role_id: int
	timezone: str
	tz: pytz.BaseTzInfo

	@staticmethod
	def from_json(path: Path) -> "DiscordConfig":
		"""
		Load config from a JSON file
		"""
		if not path.exists():
			raise FileNotFoundError(f"Data config JSON not found at {path}")
		
		data = json.loads(path.read_text(encoding="UTF-8"))

		return DiscordConfig(
			channels=data["voice_channels"],
			study_role_id=data["study_role_id"],
			timezone=data["timezone"],
			tz=pytz.timezone(data["timezone"]),
		)
