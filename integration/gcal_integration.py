from .data_block import VoiceSession
from ..google_calendar.calendar.events import create_event

def create_gcal_event(service, discord_cfg, calendar_cfg, session: VoiceSession):
	try:
		calendar_id = discord_cfg.categories[session.category]["calendar_id"]
	except IndexError:
		raise IndexError(f"calendar ID for category '{session.category}' not found in Discord cfg")

	create_event(
		service, calendar_cfg, calendar_id,
		title=session.category,  # voice channel name
		start_datetime=session.start_time,
		end_datetime=session.end_datetime,
		subcategory=session.subcategory,
	)
