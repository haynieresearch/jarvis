#**********************************************************
#* CATEGORY    APPLICATIONS
#* GROUP       HOME AUTOMATION
#* AUTHOR      LANCE HAYNIE <LHAYNIE@HAYNIEMAIL.COM>
#* DATE        2017-08-09
#* PURPOSE     JARVIS HOME AUTOMATION README
#**********************************************************
#* MODIFICATIONS
#* 2017-08-09 - LHAYNIE - INITIAL VERSION
#* 2018-08-17 - LHAYNIE - UPDATES FOR MODIFIED SMS COMMANDS
#* 2018-08-17 - LHAYNIE - UPDATES FOR FLOORPLAN
#**********************************************************
Jarvis is a Home Assistant (https://home-assistant.io/) implementation with wake word detection, SMS commands,
and a lot of automation control. While the Conversation component does it's job, it's currently a bit limited
and without wake word detection it was almost useless to me. I also have tried the AlexaPi implementation as
well as using Amazon Alexa products. However, creating custom intents was not as straight forward as I would
have liked for quick and easy creation. Between wake word and API.AI for speech handling, it appears to work
rather well. I have also decoupled the TTS services to make it easier to use that functionality elsewhere.

Note: SMS commands will require a basic level of experience with PHP.

P.S.: This system is far from perfect, if you make some enhancements or have any ideas please
feel free to share them. If you find any bugs you would like to report, you can do so via
the following link: https://sourceforge.net/p/jarvis-home-automation/tickets/?source=navbar
Keep in mind, generally any Home Assistant related issues should be raised on their side. If you are having a
configuration problem, I would be glad to help.

You will need to read this section completely before using this software to ensure that everything
works as designed. There is no other documentation other than this README file. Please note: this software
comes with no guaranteed support. Furthermore, this software is licensed under the MIT license.
License text is provided in the LICENSE file.

#**********************************************************
# DEVICES
#**********************************************************
Apple AirPort Extreme
Too Many iOS Devices
Raspberry Pi 3 - The Brain
Raspberry Pi LCD 7" Touchscreen - Touchscreen Interface
Honeywell Wi-Fi Thermostat
Wink Relay - Smart Switches + Touchscreen Interface
Wink Hub
Lutron Wireless Dimmer
Leviton Z-Wave Switch
Schlage Deadbolt
Phillips Hue Starter Pack
Phillips Hue Light Strip
Phillips Hue Soft White Blub
Phillips Hue Color Bulb
Phillips Hue Color Flood Light Bulb
Logitech Harmony Ultimate
iHome Smart Plug
Kiddie Z-Wave Smoke/Carbon Monoxide Alarm

#**********************************************************
# ASSUMPTIONS
#**********************************************************
This software makes a couple of assumptions, I will list them below and you can either update/install
what is needed on your system or make the required changes. Even though the software is open source,
some services currently are utilizing paid services. The main service is Microsoft Bing Speech.
While there are free alternatives for speech-to-text services. I have found them to be less than desirable.
Luckily, most have a free tier available to use.

For everything to work, you will need the following API keys:
API.AI - https://api.ai/
Microsoft Azure Bing Speech - https://docs.microsoft.com/en-us/azure/cognitive-services/speech/home
Microsoft Azure Face - https://docs.microsoft.com/en-us/azure/cognitive-services/face/overview
Dark Sky - https://darksky.net/dev/
Weather Underground - https://www.wunderground.com/weather/api/
Twilio - https://twilio.com

If you want SSL you can purchase and install a certificate. However, I find it much easier to sign
up for a free Cloud Flare (https://www.cloudflare.com) plan and encrypt your external site that way.

Note: I am going to include my current configuration and layout as an example. The systemd services
are included in the resources folder if you wish to edit them. The installer will take care of setting
this up for you.

#**********************************************************
# CONFIGURATION FILES
#**********************************************************
/opt/jarvis/configuration.yaml
/opt/jarvis/secrets.yaml
/opt/jarvis/stt/config/config.yaml

#**********************************************************
# SETUP
#**********************************************************
 1. Download the Raspian Lite image, and burn to an SD card for your Raspberry Pi.
 2. Boot your Raspberry Pi and set the initial system configuration.
    2.1. Login with the default user pi and password raspberry.
    2.2. Change the password with the command "passwd" and change to something other than the default.
    2.3. Run the program "sudo raspi-config" to initially setup your Pi.
         2.3.1. Hostname menu, set the hostname you wish to have your Pi appear as on the network.
         2.3.2. Interfacing Options menu, enable at a minimum SSH for remote access.
         2.3.3. Advanced Settings, set the memory split to 16 and audio to force 3.5mm.
         2.3.4. Reboot your Pi.
 3. Navigate to /opt "cd /opt" on your Raspberry Pi.
 4. Checkout the latest Jarvis program: sudo svn checkout svn://svn.code.sf.net/p/jarvis-home-automation/code/trunk/ jarvis
 5. Update permissions: sudo chown -fR pi:pi jarvis
 6. Navigate to /opt/jarvis "cd /opt/jarvis" and run InstallJarvis.sh
 7. Configure AWS CLI for Amazon Polly TTS: aws configure --profile adminuser
    7.1. You will need to obtain your AWS Access Key, and Secret Key before you begin
    7.2. Default Region Name: us-east-1
    7.3. Default Output Format: text
 8. Edit the configuration options in /opt/jarvis/secrets.yaml
    8.1. Set the Latitude and Longitude
    8.2. Set the HTTP Password
    8.3. Set the alarm code if you are going to use the alarm system
    8.4. Set the base URL to the Raspberry Pi's local address with 8123 as the port
    8.5. If you use Wink Products, update the wink_email and wink_password, otherwise delete
    8.6. Update applicable API keys
    8.7. Update Twilio SID and Token if you are going to use SMS and Call notification
    8.8. Update Honeywell user and pass if you use Honeywell Thermostats, else delete
 9. Setup API Access
    9.1. API.AI
         9.1.1. Navigate to https://console.api.ai/
         9.1.2. Create a new a new Agent
         9.1.3. Go to the Agent Settings, make note of your Client Access Token
         9.1.4. Navigate to Export and Import, and RESTORE FROM ZIP: /opt/jarvis/resources/apiai.zip
    9.2. Amazon AWS
        9.2.1. http://docs.aws.amazon.com/general/latest/gr/managing-aws-access-keys.html
    9.3. Microsoft Azure Bing Speech
         9.3.1. https://azure.microsoft.com/en-us/try/cognitive-services/?api=speech-api
10. Edit the configuration options in /opt/jarvis/stt/config/config.yaml
    10.1. Change the keyword to whatever you want to wake up Jarvis
    10.2. Update the HA (Home Assistant) host (Raspberry Pi IP address) and API password
    10.3. Update the apiai and bing_speech API keys
11. Update /opt/jarvis/configuration.yaml
    11.1. Update the options in homeassistant:
    11.2. Update the trusted_networks to include the IP of the Raspberry Pi
    11.3. Update any logbook exclusions/inclusions
    11.4. Do the same thing to history
    11.5. Update the ACCOUNTS section for applicable account connections
    11.6. Update the MISC CONFIG section
12. Update SMS Commands
    12.1. Edit the PHP file /opt/jarvis/web/webapi/sms/config.php
    12.2. Update the commands you wish to execute
13. Update Pianobar (Pandora) configuration
    13.1. Edit /home/pi/.config/pianobar/config and update email/password for Pandora to work
14. Update the floorplans, refer to https://github.com/pkozul/ha-floorplan
15. Reboot your Raspberry Pi


If all is well, your system will be 100% ready to go. If you have an attached screen/touch screen the main
panel will appear after all systems boot. If not, navigate to http://<raspberry pi IP>:8123.

#**********************************************************
# NOTES
#**********************************************************
Once installed you can use the following system services to restart/control the entire system.

Restart Everything:
sudo service jarvis* restart

Restart Home Assistant:
sudo service jarvis-base restart

Restart Speech to Text:
sudo service jarvis-stt restart

Restart Text to Speech:
sudo service jarvis-tts restart

Restart Kiosk:
sudo service jarvis-web restart

If you get a TLS fingerprint mismatch error with Pianobar/Pandora run this command to get the updated one:
openssl s_client -connect tuner.pandora.com:443 < /dev/null 2> /dev/null | \
    openssl x509 -noout -fingerprint | tr -d ':' | cut -d'=' -f2
