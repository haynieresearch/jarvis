#!/bin/bash
/usr/bin/sqlite3 -column /opt/jarvis/database/jarvis.db < /opt/jarvis/database/states.sql > /opt/jarvis/database/JARVIS.DATA.STATES
/usr/bin/sqlite3 -column /opt/jarvis/database/jarvis.db < /opt/jarvis/database/events.sql > /opt/jarvis/database/JARVIS.DATA.EVENTS
/usr/bin/todos /opt/jarvis/database/JARVIS.DATA.STATES
/usr/bin/todos /opt/jarvis/database/JARVIS.DATA.EVENTS
