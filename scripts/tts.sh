#!/bin/bash
#**********************************************************
#* CATEGORY    JARVIS HOME AUTOMTION
#* GROUP       TEXT TO SPEECH - SPEAK
#* AUTHOR      LANCE HAYNIE <LANCE@HAYNIEMAIL.COM>
#**********************************************************
#Jarvis Home Automation
#Copyright 2020 Haynie IPHC, LLC
#Developed by Haynie Research & Development, LLC
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.#
#You may obtain a copy of the License at
#http://www.apache.org/licenses/LICENSE-2.0
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

pid=$$
pidfile=/opt/jarvis/run/tts.pid
server=$(ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1')
port=8000
voice=Brian

echo "TTS Process started @ $(date)" >> /opt/jarvis/logs/tts.log

trap "rm -f -- '$pidfile'" EXIT
echo $pid > "$pidfile"

for pidcheck in $(pidof -x tts.sh); do
	if [ $pidcheck != $$ ]; then
		echo "TTS process is currently running, waiting for message to finish." >> /opt/jarvis/logs/tts.log
		sleep 10
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
    mpg123 -a hw:0,0 -q "http://$server:$port/read?voiceId=$voice&text=$NEXTURL&outputFormat=mp3"
		echo "TTS Message: $INPUT" >> /opt/jarvis/logs/tts.log
done
exit 0
