from dotenv import load_dotenv
load_dotenv()

from datetime import datetime, timedelta

from .data_block import VoiceSession
from .merge import merge_sessions

# from ..google_calendar.config import load_calendar_config
# from ..discord_bot.config import load_discord_config
from .config import load_integration_config

sessions = [
    VoiceSession("academic", "COMP1234", datetime(2025, 12, 19, 9, 0), datetime(2025, 12, 19, 10, 0)),
    VoiceSession("academic", "COMP1234", datetime(2025, 12, 19, 10, 2), datetime(2025, 12, 19, 11, 0)),  # 2-min gap -> merge
    VoiceSession("academic", "COMP1234", datetime(2025, 12, 19, 11, 10), datetime(2025, 12, 19, 11, 12)), # 12-min gap -> separate but too short -> removed
    VoiceSession("academic", "COMP5678", datetime(2025, 12, 19, 12, 0), datetime(2025, 12, 19, 13, 0)), # different subcategory -> separate
]

int_cfg = load_integration_config()

merged = merge_sessions(sessions, int_cfg.merge_gap_minutes, int_cfg.min_duration_minutes)
for s in merged:
    print(s)
