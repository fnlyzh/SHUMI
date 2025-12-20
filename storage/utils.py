import json
from pathlib import Path

from core.models import VoiceSession
from config.handler import load_data_path

SESSIONS_FILE: Path = load_data_path()


def append_session(session):
	SESSIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
	with SESSIONS_FILE.open("a", encoding="UTF-8", newline="\n") as f:
		f.write(json.dumps(session.to_dict(), ensure_ascii=True) + "\n")


def load_sessions():
	if not SESSIONS_FILE.exists():
		return []

	sessions = []
	with SESSIONS_FILE.open("r", encoding="UTF-8") as f:
		for line in f:
			sessions.append(VoiceSession.from_dict(json.loads(line)))
	return sessions


def clear_sessions():
	if SESSIONS_FILE.exists:
		SESSIONS_FILE.unlink()
