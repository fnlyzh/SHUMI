from .calendar.events import create_event
from storage.utils import load_sessions #, clear_sessions
from storage.processing import merge_sessions
from config.handler import load_integration_config

def flush_sessions_to_calendar(service, discord_cfg, calendar_cfg):
	sessions = load_sessions()
	if not sessions:
		return
	
	int_cfg = load_integration_config()
	
	merged = merge_sessions(
		sessions,
		merge_gap_minutes=int_cfg.merge_gap_minutes,
		min_duration_minutes=int_cfg.min_duration_minutes,
	)

	for session in merged:
		try:
			try:
				calendar_id = discord_cfg.channels[session.category]["calendar_id"]
			except IndexError:
				raise IndexError(f"calendar ID for category '{session.category}' not found in Discord cfg")

			create_event(
				service, calendar_cfg, calendar_id,
				title=session.subcategory,  # voice channel name
				start_datetime=session.start_time,
				end_datetime=session.end_time,
				subcategory=session.subcategory,
			)
		except Exception as err:
			print(f"[error] failed to create event: {err}")
			continue

	# clear_sessions()