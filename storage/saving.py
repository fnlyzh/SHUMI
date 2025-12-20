from datetime import datetime, timezone
from .utils import append_session
from core.models import VoiceSession

def save_voice_session(category, subcategory, start_time):
	session = VoiceSession(
		category=category,
		subcategory=subcategory,
		start_time=start_time,
		end_time=datetime.now(timezone.utc),
	)

	append_session(session)
