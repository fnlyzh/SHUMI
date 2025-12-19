# Folder Architecture
google_calendar/
├── main.py               # entry point; controller
├── auth.py               # OAuth + token handling
├── service.py            # Google Calendar service creation
│
├── calendar/
│   ├── __init__.py
│   ├── events.py         # CRUD operations for events
│   ├── queries.py        # list/search/filter helpers
│   └── utils.py          # helper utility functions
│
├── tasks/
│   ├── __init__.py
│   ├── tasks.py          # CRUD operations for tasks
│   ├── queries.py        # list/search/filter helpers
│   └── utils.py          # helper utility functions
│
├── automation/
│   ├── __init__.py
│   ├── rescheduler.py    # move events based on tasks/rules
│   └── rules.py          # logic for rescheduling
│
├── config.py             # scopes, paths, constants
├── credentials.json
└── token.json
