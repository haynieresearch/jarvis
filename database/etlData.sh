#!/bin/bash
source passwords.cfg

/usr/bin/sqlite3 -column /opt/jarvis/database/jarvis.db < /opt/jarvis/database/states.sql > /opt/jarvis/database/JARVIS.DATA.STATES
/usr/bin/sqlite3 -column /opt/jarvis/database/jarvis.db < /opt/jarvis/database/events.sql > /opt/jarvis/database/JARVIS.DATA.EVENTS
/usr/bin/todos /opt/jarvis/database/JARVIS.DATA.STATES
/usr/bin/todos /opt/jarvis/database/JARVIS.DATA.EVENTS

#Add JARVIS data to GDG
ftp -n -v $HOST << EOT
ascii
user $USER $PASSWD
prompt
site NOWRAP
site SBSENDEOL=CRLF
site CYL pri=500 sec=100
cd "'JARVIS'"
site LRECL=200 RECFM=F
put JARVIS.DATA.STATES DATA.STATES(+1)
site LRECL=2000 RECFM=F
put JARVIS.DATA.EVENTS DATA.EVENTS(+1)
bye
EOT
