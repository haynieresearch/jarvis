#/bin/bash
joke=$(curl -s "https://v2.jokeapi.dev/joke/Miscellaneous,Dark,Pun,Spooky,Christmas?blacklistFlags=nsfw,explicit&format=txt") >/dev/null 2>&1
/opt/jarvis/scripts/tts.sh "Do you want to hear a joke?"
sleep 1
/opt/jarvis/scripts/tts.sh $joke
