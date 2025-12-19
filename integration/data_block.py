from dataclasses import dataclass
from datetime import datetime

@dataclass
class VoiceSession:
	category: str
	subcategory: str  # voice channel name
	start_time: datetime
	end_time: datetime
