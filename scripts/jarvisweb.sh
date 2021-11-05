#!/bin/bash
#**********************************************************
#* CATEGORY    JARVIS HOME AUTOMTION
#* GROUP       START WEB FRONT END KIOSK MODE
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

sleep 15
export DISPLAY=:0
/usr/bin/xset -dpms
/usr/bin/xset s noblank
/usr/bin/xset s off

/usr/bin/unclutter &
/usr/bin/chromium-browser --kiosk --incognito --start-fullscreen --disable-session-crashed-bubble --enable-features=OverlayScrollbar --disable-infobars --noerrdialogs --no-first-run --fast --fast-start --enable-use-zoom-for-dsf http://10.10.0.11:8123/
