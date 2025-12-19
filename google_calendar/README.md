# Folder Architecture
google_calendar/
├── main.py               # entry point; controller
├── auth.py               # OAuth + token handling
├── service.py            # Google Calendar service creation
│
├── calendar/
│   ├── __init__.py
│   ├── events.py         # CRUD operations for events
│   ├── recurrence.py     # weekly classes, RRULE helpers
│   └── queries.py        # list/search/filter helpers
│
├── automation/
│   ├── __init__.py
│   ├── rescheduler.py    # move events based on tasks/rules
│   └── rules.py          # logic for rescheduling
│
├── config.py             # scopes, paths, constants
├── credentials.json
└── token.json
