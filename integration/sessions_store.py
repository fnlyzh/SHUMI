import json
import os

from .data_block import VoiceSession

from .config import load_data_path
SESSIONS_FILE = load_data_path()

def append_session(session):
	os.makedirs(os.path.dirname(SESSIONS_FILE), exist_ok=True)
	with open(SESSIONS_FILE, "a") as f:
		f.write(json.dumps(session.to_dict()) + "\n")


def load_sessions():
	if not os.path.exists(SESSIONS_FILE):
		return []

	sessions = []
	with open(SESSIONS_FILE, "r") as f:
		for line in f:
			sessions.append(VoiceSession.from_dict(json.loads(line)))
	return sessions


def clear_sessions():
	if os.path.exists(SESSIONS_FILE):
		os.remove(SESSIONS_FILE)
