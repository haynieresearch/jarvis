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
sudo apt-get install subversion python-pip python3-dev python3-pip mpg123 python-dev \
bison libasound2-dev libportaudio-dev python-pyaudio xorg chromium-browser \
nginx php5-fpm php-apc pianobar net-tools nmap --yes

echo "Installing Python2 Requirements"
sudo pip2 install boto3 awscli slugify mad pyalsa pyalsaaudio apiai

echo "Installing Python3 Requirements"
sudo pip3 install homeassistant sqlalchemy

echo "Installing System Services"
sudo cp -fR /opt/jarvis/resources/jarvis-* /etc/systemd/system/
sudo systemctl enable /etc/systemd/system/jarvis-*.service
sudo systemctl daemon-reload

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
mv secrets.yaml.example secrets.yaml
cd /opt/jarvis/stt/config/
mv config.yaml.example
cd /opt/jarvis
