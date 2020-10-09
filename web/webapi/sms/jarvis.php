<?php
#**********************************************************
#* CATEGORY    SMS AUTOMATION
#* GROUP       HOME AUTOMATION
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

$number = $_GET['From'];
$body = $_GET['Body'];

include 'config.php';
include 'functions.php';

if (in_array($number, $nwsNumbers))
	{
		wx_alert($body);
	}
elseif (in_array($number, $blockedNumbers))
	{
		$reply = "Error: You have been blocked by Jarvis for abuse of the system.";
	}
elseif (in_array($number, $validNumbers) && strtolower(substr($body,0,4)) == "tts:")
	{
		tts($body);
	}
elseif (in_array($number, $validNumbers) && strtolower(substr($body,0,8)) == "massmsg:")
	{
		massmsg($body);
	}
elseif (in_array($number, $validNumbers))
	{
		sendCommand($body);
	}
else
	{
		$reply = "Error: You are not authorized to send commands.";
	}

if (empty($reply))
	{
		$reply = "Command Received";
	}

header('Content-Type: text/xml');
?>
<Response>
    <Message>
    	<?php echo $reply; ?>
    </Message>
</Response>
