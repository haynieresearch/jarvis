#!/bin/bash
#**********************************************************
#* CATEGORY    JARVIS HOME AUTOMTION
#* GROUP       TEXT TO SPEECH - SAVE FILE
#* AUTHOR      LANCE HAYNIE <LANCE@HAYNIEMAIL.COM>
#**********************************************************
#Jarvis Home Automation
#Copyright (C) 2017  Haynie Research & Development

#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License along
#with this program; if not, write to the Free Software Foundation, Inc.,
#51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

pid=$$
pidfile=/opt/jarvis/run/tts.pid
server=10.0.1.200
port=8000
voice=Brian

echo "TTS Process started @ $(date)" >> /opt/jarvis/logs/tts.log

trap "rm -f -- '$pidfile'" EXIT
echo $pid > "$pidfile"

for pidcheck in $(pidof -x tts.sh); do
	if [ $pidcheck != $$ ]; then
		echo "TTS process is currently running, waiting for message to finish." >> /opt/jarvis/logs/tts.log
		sleep 5
		exec bash "$0" $*
	fi
done

INPUT=$*
STRINGNUM=0

ary=($INPUT)
for key in "${!ary[@]}"
  do
    SHORTTMP[$STRINGNUM]="${SHORTTMP[$STRINGNUM]} ${ary[$key]}"
    LENGTH=$(echo ${#SHORTTMP[$STRINGNUM]})
    if [[ "$LENGTH" -lt "1500" ]]; then
      SHORT[$STRINGNUM]=${SHORTTMP[$STRINGNUM]}
    else
      STRINGNUM=$(($STRINGNUM+1))
      SHORTTMP[$STRINGNUM]="${ary[$key]}"
      SHORT[$STRINGNUM]="${ary[$key]}"
    fi
done

for key in "${!SHORT[@]}"
  do
    NEXTURL=$(echo ${SHORT[$key]} | xxd -plain | tr -d '\n' | sed 's/\(..\)/%\1/g')
    wget -O /opt/jarvis/tmp/tts.mp3 "http://$server:$port/read?voiceId=$voice&text=$NEXTURL&outputFormat=mp3"
		echo "TTS Message: $INPUT" >> /opt/jarvis/logs/tts.log
done
exit 0
