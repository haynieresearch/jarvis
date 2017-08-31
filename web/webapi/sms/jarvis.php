<?php
#**********************************************************
#* CATEGORY    SMS AUTOMATION
#* GROUP       HOME AUTOMATION
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

$number = $_GET['From'];
$body = $_GET['Body'];

include 'config.php';
include 'functions.php';

if (in_array($number, $nwsNumbers))
	{
		wx_alert($body);
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
