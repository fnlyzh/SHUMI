import json
import os
import pytz
from dataclasses import dataclass
import dotenv
from datetime import datetime, date

from typing import Dict, List

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
	def from_json(path: str) -> "CalendarConfig":
		"""
		Load config from a JSON file
		"""
		if not os.path.exists(path):
			raise FileNotFoundError(f"Personal config JSON not found at {path}")

		with open(path, "r", encoding="utf-8") as f:
			data = json.load(f)

		return CalendarConfig(
			calendars=data["calendars"],
			recurrence_color_id=data["recurrence_color_id"],
			term_start_monday=datetime.strptime(data["term_start_monday"], "%Y-%m-%d").date(),
			term_weeks=data["term_weeks"],
			break_weeks=data["break_weeks"],
			timezone=data["timezone"],
			tz=pytz.timezone(data["timezone"]),
		)

def load_calendar_config():
	dotenv.load_dotenv()
	cfg_path = os.getenv("CALENDER_CONFIG_PATH")
	if cfg_path is None:
		raise RuntimeError("CALENDER_CONFIG_PATH is not set in .env")
	return CalendarConfig.from_json(cfg_path)