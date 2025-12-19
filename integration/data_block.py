from dataclasses import dataclass
from datetime import datetime

@dataclass
class VoiceSession:
	category: str
	subcategory: str  # voice channel name
	start_time: datetime
	end_time: datetime

	def to_dict(self):
		return {
			"category": self.category,
			"subcategory": self.subcategory,
			"start_time": self.start_time.isoformat(),
			"end_time": self.end_time.isoformat()
		}
	
	@staticmethod
	def from_dict(d):
		return VoiceSession(
			category=d["category"],
			subcategory=d["subcategory"],
			start_time=datetime.fromisoformat(d["start_time"]),
			end_time=datetime.fromisoformat(d["end_time"])
		)