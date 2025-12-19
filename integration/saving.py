from datetime import datetime, timezone
from .sessions_store import append_session
from .data_block import VoiceSession

def save_voice_session(category, subcategory, start_time):
	session = VoiceSession(
		category=category,
		subcategory=subcategory,
		start_time=start_time,
		end_time=datetime.now(timezone.utc),
	)
	append_session(session)
