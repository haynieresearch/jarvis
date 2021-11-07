#!/bin/bash
#**********************************************************
#* CATEGORY    APPLICATIONS
#* GROUP       HOME AUTOMATION
#* AUTHOR      LANCE HAYNIE
#* PURPOSE     UPDATE SCRIPT
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

echo "Setting Permissions"
cd /opt/
sudo chown -fR pi:pi jarvis
sudo chmod -fR 775 jarvis

echo "Updating System"
sudo apt-get update

echo "Upgrading System"
sudo apt-get upgrade --yes
sudo rpi-update

echo "Installing Python3 Requirements"
sudo pip3 install --upgrade homeassistant
sudo pip3 install --upgrade sqlalchemy
sudo pip3 install --upgrade appdaemon
sudo pip3 install --upgrade boto3
sudo pip3 install --upgrade awscli
sudo pip3 install --upgrade slugify
sudo pip3 install --upgrade mad
sudo pip3 install --upgrade pyalsaaudio
sudo pip3 install --upgrade apiai

echo "Installing Python2 Requirements"
sudo pip2 install --upgrade boto3
sudo pip2 install --upgrade awscli
sudo pip2 install --upgrade slugify
sudo pip2 install --upgrade mad
sudo pip2 install --upgrade pyalsa
sudo pip2 install --upgrade pyalsaaudio
sudo pip2 install --upgrade apiai
sudo pip2 install --upgrade requests
