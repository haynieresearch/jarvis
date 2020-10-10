#!/bin/bash
#**********************************************************
#* CATEGORY    APPLICATIONS
#* GROUP       HOME AUTOMATION
#* AUTHOR      LANCE HAYNIE <LHAYNIE@HAYNIEMAIL.COM>
#* DATE        2017-08-09
#* PURPOSE     INSTALLER SCRIPT
#**********************************************************
#* MODIFICATIONS
#* 2017-08-09 - LHAYNIE - INITIAL VERSION
#* 2017-08-18 - LHAYNIE - UPDATED EXAMPLE CONFIG
#* 2017-08-22 - LHAYNIE - REMOVED SUBVERSION
#* 2017-08-22 - LHAYNIE - UPDATED CONFIG COPY PROCESS
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

echo "Installing System Requirements"
sudo apt-get install python-pip python3-dev python3-pip mpg123 python-dev \
bison libasound2-dev libportaudio-dev python-pyaudio xorg chromium-browser \
nginx php-fpm php-apcu pianobar net-tools nmap npm php-curl unclutter \
iptables-persistent dnsutils python-pyalsa python3-pyalsa jackd2 --yes

echo "Installing Python3 Requirements"
sudo pip3 install homeassistant
sudo pip3 install sqlalchemy
sudo pip3 install appdaemon
sudo pip3 install boto3
sudo pip3 install awscli
sudo pip3 install slugify
sudo pip3 install mad
sudo pip3 install pyalsaaudio
sudo pip3 install apiai

echo "Installing Python2 Requirements"
sudo pip2 install boto3
sudo pip2 install awscli
sudo pip2 install slugify
sudo pip2 install mad
sudo pip2 install pyalsa
sudo pip2 install pyalsaaudio
sudo pip2 install apiai
sudo pip2 install requests

echo "Installing System Services"
sudo cp -fR /opt/jarvis/resources/jarvis-* /etc/systemd/system/
sudo systemctl enable /etc/systemd/system/jarvis-*.service
sudo systemctl daemon-reload

echo "Installing Composer"
sudo curl -sS https://getcomposer.org/installer | sudo php -- --install-dir=/usr/local/bin --filename=composer

echo "Setting Up Twilio SDK"
cd /opt/jarvis/web/webapi/sms
composer require twilio/sdk
cd /opt/jarvis

echo "Setting up nginx web server"
sudo /etc/init.d/nginx stop
sudo rm -fR /var/www/html
sudo ln -s /opt/jarvis/web/ /var/www/html
sudo /etc/init.d/nginx start

echo "Setting up User Config"
cp -fR /opt/jarvis/resources/user-config /home/pi/.config

echo "Setting up sound profile"
cp -fR /opt/jarvis/resources/asoundrc /home/pi/.asoundrc

echo "Setting up Configuration Files"
cd /opt/jarvis
cp secrets.yaml.example secrets.yaml
cd /opt/jarvis/stt/config
cp config.yaml.example config.yaml
cd /opt/jarvis/web/webapi/sms
cp config.php.example config.php
cd /opt/jarvis
