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

require __DIR__ . '/vendor/autoload.php';
use Twilio\Rest\Client;

function tts($varCommand)
	{
		global $command;
		global $url;
		global $host;
		global $passwordUrl;
		global $password;
		global $json_data;
		global $data;
		global $reply;
		global $restUrl;
		global $options;
		global $context;
		global $result;

		$restUrl = $host . "services/shell_command/tts";
		$options = array(
			'http' => array(
			'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
			'method'  => 'POST',
			'content' => '{"message": "' . substr($varCommand, 4) . '"}'
		),
		);

		$context  = stream_context_create($options);
		$result = file_get_contents($restUrl, false, $context);
	}

function massmsg($varCommand)
	{
		global $command;
		global $url;
		global $host;
		global $passwordUrl;
		global $password;
		global $json_data;
		global $data;
		global $reply;
		global $restUrl;
		global $options;
		global $context;
		global $result;
		global $validNumbers;
    global $twilio_sid;
    global $twilio_token;
    global $fromNumber;

    $sid = $twilio_sid;
		$token = $twilio_token;
		$client = new Client($sid, $token);

		foreach ($validNumbers as $number) {
		$client->messages->create(
			$number,
			array(
					'from' => '$fromNumber',
					'body' => "Mass Message:" . substr($varCommand, 8)
			)
		);
		}

		$reply = "Mass Message Sent:" . substr($varCommand, 8);
	}

function send_tts($varCommand)
	{
		global $command;
		global $url;
		global $host;
		global $passwordUrl;
		global $password;
		global $json_data;
		global $data;
		global $reply;
		global $restUrl;
		global $options;
		global $context;
		global $result;
    global $twilio_sid;
    global $twilio_token;
    global $fromNumber;
		global $nwsRelayNumbers;

		function cleaner($url) {
		  $U = explode(' ',$url);

		  $W =array();
		  foreach ($U as $k => $u) {
		    if (stristr($u,'http') || (count(explode('.',$u)) > 1)) {
		      unset($U[$k]);
		      return cleaner( implode(' ',$U));
		    }
		  }
		  return implode(' ',$U);
		}

		$restUrl = $host . "services/shell_command/alarm_sound";
		$options = array(
			'http' => array(
			'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
			'method'  => 'POST'
		),
		);

		$context  = stream_context_create($options);
		$result = file_get_contents($restUrl, false, $context);

		sleep(1);

		$restUrl = $host . "services/shell_command/alarm_sound";
		$options = array(
			'http' => array(
			'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
			'method'  => 'POST'
		),
		);

		$context  = stream_context_create($options);
		$result = file_get_contents($restUrl, false, $context);

		$restUrl = $host . "services/shell_command/tts";
		$options = array(
			'http' => array(
			'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
			'method'  => 'POST',
			'content' => '{"message": "Weather Alert, Weather Alert. ' . cleaner($varCommand) . '"}'
		),
		);

		$context  = stream_context_create($options);
		$result = file_get_contents($restUrl, false, $context);

		sleep(1);

		$sid = $twilio_sid;
		$token = $twilio_token;
		$client = new Client($sid, $token);

		foreach ($nwsRelayNumbers as $number) {
		$client->messages->create(
			$number,
			array(
					'from' => '$fromNumber',
					'body' => "Weather Alert: $varCommand"
			)
		);
  	}
	}

function sendCommand($varCommand)
	{
		global $command;
		global $url;
		global $host;
		global $passwordUrl;
		global $password;
		global $json_data;
		global $data;
		global $reply;
		global $restUrl;
		global $options;
		global $context;
		global $result;

		if (strtolower($varCommand) == "commands")
			{
				$reply = "Available Commands: Alarm status / Fire status / Lights on / Disarm / Arm away / Arm home / Cancel fire / Cancel carbon / Panic / Fire call / Fire call cancel / Outside bright / Outside blue / Outside off / tts: / massmsg: / katiemsg / sounds";
			}

		elseif (strtolower($varCommand) == "sounds")
				{
					$reply = "Available Sounds: fart / air raid / ghost / zombie / foghorn / gunshot / siren";
				}

		elseif (strtolower($varCommand) == "katiemsg")
				{
					$reply = "Available Katie Messages: Katie call mom / Katie call mom home / Katie call mom cell / Katie call dad / Katie call dad home / Katie call dad cell";
				}

		elseif (strtolower($varCommand) == "panic")
			{
				$restUrl = $host . "services/homeassistant/turn_on";
				$options = array(
					'http' => array(
					'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
					'method'  => 'POST',
					'content' => '{"entity_id": "input_boolean.panic"}'
				),
				);

				$context  = stream_context_create($options);
				$result = file_get_contents($restUrl, false, $context);

				$reply = "Panic Alarm Activated";
			}

		elseif (strtolower($varCommand) == "alarm status")
			{
				$command = "states/alarm_control_panel.home_alarm";
				$url = $host . $command . $passwordUrl;
				$json_data = file_get_contents($url, false);
				$data = json_decode($json_data, true);
				$reply = "Alarm Status: " . $data['state'];
			}

		elseif ($varCommand == "fire status")
			{
				$command = "states/input_boolean.firealarm";
				$url = $host . $command . $passwordUrl;
				$json_data = file_get_contents($url, false);
				$data = json_decode($json_data, true);
				$reply = "Fire Alarm Status: " . $data['state'];
			}

		elseif (strtolower($varCommand) == "lights on")
			{
				$restUrl = $host . "services/homeassistant/turn_on";
				$options = array(
					'http' => array(
					'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
					'method'  => 'POST',
					'content' => '{"entity_id": "group.alllights"}'
				),
				);

				$context  = stream_context_create($options);
				$result = file_get_contents($restUrl, false, $context);

				$reply = "All Lights Turned On";

				$restUrl = $host . "services/shell_command/tts";
				$options = array(
					'http' => array(
					'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
					'method'  => 'POST',
					'content' => '{"message": "I have received a request to turn on all lights via SMS messaging"}'
				),
				);

				$context  = stream_context_create($options);
				$result = file_get_contents($restUrl, false, $context);
			}

		elseif (strtolower($varCommand) == "disarm")
			{
				$restUrl = $host . "services/alarm_control_panel/alarm_disarm";
				$options = array(
					'http' => array(
					'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
					'method'  => 'POST',
					'content' => '{"entity_id": "alarm_control_panel.home_alarm", "code": "1986"}'
				),
				);

				$context  = stream_context_create($options);
				$result = file_get_contents($restUrl, false, $context);

				$reply = "Alarm has been disarmed";

				sleep(10);

				$restUrl = $host . "services/shell_command/tts";
				$options = array(
					'http' => array(
					'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
					'method'  => 'POST',
					'content' => '{"message": "The alarm has been disarmed via SMS messaging."}'
				),
				);

				$context  = stream_context_create($options);
				$result = file_get_contents($restUrl, false, $context);
			}

		elseif (strtolower($varCommand) == "arm away")
			{
				$restUrl = $host . "services/alarm_control_panel/alarm_arm_away";
				$options = array(
					'http' => array(
					'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
					'method'  => 'POST',
					'content' => '{"entity_id": "alarm_control_panel.home_alarm", "code": "1986"}'
				),
				);

				$context  = stream_context_create($options);
				$result = file_get_contents($restUrl, false, $context);

				$reply = "Alarm has been armed";

				sleep(10);

				$restUrl = $host . "services/shell_command/tts";
				$options = array(
					'http' => array(
					'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
					'method'  => 'POST',
					'content' => '{"message": "The alarm has been armed via SMS messaging"}'
				),
				);

				$context  = stream_context_create($options);
				$result = file_get_contents($restUrl, false, $context);
			}

		elseif (strtolower($varCommand) == "arm home")
			{
				$restUrl = $host . "services/alarm_control_panel/alarm_arm_home";
				$options = array(
					'http' => array(
					'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
					'method'  => 'POST',
					'content' => '{"entity_id": "alarm_control_panel.home_alarm", "code": "1986"}'
				),
				);

				$context  = stream_context_create($options);
				$result = file_get_contents($restUrl, false, $context);

				$reply = "Alarm has been armed";

				sleep(10);

				$restUrl = $host . "services/shell_command/tts";
				$options = array(
					'http' => array(
					'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
					'method'  => 'POST',
					'content' => '{"message": "The alarm has been armed via SMS messaging"}'
				),
				);

				$context  = stream_context_create($options);
				$result = file_get_contents($restUrl, false, $context);
			}

		elseif (strtolower($varCommand) == "cancel Fire")
			{
				$restUrl = $host . "services/script/turn_off";
				$options = array(
					'http' => array(
					'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
					'method'  => 'POST',
					'content' => '{"entity_id": "script.sos_alarm"}'
				),
				);

				$context  = stream_context_create($options);
				$result = file_get_contents($restUrl, false, $context);

				$restUrl = $host . "services/script/turn_off";
				$options = array(
					'http' => array(
					'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
					'method'  => 'POST',
					'content' => '{"entity_id": "script.sos_alarm_loop"}'
				),
				);

				$context  = stream_context_create($options);
				$result = file_get_contents($restUrl, false, $context);

				$restUrl = $host . "services/homeassistant/turn_off";
				$options = array(
					'http' => array(
					'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
					'method'  => 'POST',
					'content' => '{"entity_id": "switch.vibratone"}'
				),
				);

				$context  = stream_context_create($options);
				$result = file_get_contents($restUrl, false, $context);

				$restUrl = $host . "services/homeassistant/turn_off";
				$options = array(
					'http' => array(
					'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
					'method'  => 'POST',
					'content' => '{"entity_id": "input_boolean.firealarm"}'
				),
				);

				$context  = stream_context_create($options);
				$result = file_get_contents($restUrl, false, $context);

				$reply = "Fire alarm has been cancelled";

				sleep(10);

				$restUrl = $host . "services/shell_command/tts";
				$options = array(
					'http' => array(
					'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
					'method'  => 'POST',
					'content' => '{"message": "The fire alarm has been cancelled via SMS messaging"}'
				),
				);

				$context  = stream_context_create($options);
				$result = file_get_contents($restUrl, false, $context);
			}

		elseif (strtolower($varCommand) == "cancel carbon")
			{
				$restUrl = $host . "services/script/turn_off";
				$options = array(
					'http' => array(
					'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
					'method'  => 'POST',
					'content' => '{"entity_id": "script.sos_alarm"}'
				),
				);

				$context  = stream_context_create($options);
				$result = file_get_contents($restUrl, false, $context);

				$restUrl = $host . "services/script/turn_off";
				$options = array(
					'http' => array(
					'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
					'method'  => 'POST',
					'content' => '{"entity_id": "script.sos_alarm_loop"}'
				),
				);

				$context  = stream_context_create($options);
				$result = file_get_contents($restUrl, false, $context);

				$restUrl = $host . "services/homeassistant/turn_off";
				$options = array(
					'http' => array(
					'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
					'method'  => 'POST',
					'content' => '{"entity_id": "switch.vibratone"}'
				),
				);

				$context  = stream_context_create($options);
				$result = file_get_contents($restUrl, false, $context);

				$restUrl = $host . "services/homeassistant/turn_off";
				$options = array(
					'http' => array(
					'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
					'method'  => 'POST',
					'content' => '{"entity_id": "input_boolean.coalarm"}'
				),
				);

				$context  = stream_context_create($options);
				$result = file_get_contents($restUrl, false, $context);

				$reply = "Carbon monoxide alarm has been cancelled";

				sleep(10);

				$restUrl = $host . "services/shell_command/tts";
				$options = array(
					'http' => array(
					'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
					'method'  => 'POST',
					'content' => '{"message": "The carbon monoxide alarm has been cancelled via SMS messaging"}'
				),
				);

				$context  = stream_context_create($options);
				$result = file_get_contents($restUrl, false, $context);
			}

		elseif (strtolower($varCommand) == "fire call")
			{
				$restUrl = $host . "services/homeassistant/turn_on";
				$options = array(
					'http' => array(
					'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
					'method'  => 'POST',
					'content' => '{"entity_id": "input_boolean.lancefirecall"}'
				),
				);

				$context  = stream_context_create($options);
				$result = file_get_contents($restUrl, false, $context);

				$reply = "Fire call status set to on; reply fire call cancel when returning";
			}

		elseif (strtolower($varCommand) == "fire call cancel")
			{
				$restUrl = $host . "services/homeassistant/turn_off";
				$options = array(
					'http' => array(
					'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
					'method'  => 'POST',
					'content' => '{"entity_id": "input_boolean.lancefirecall"}'
				),
				);

				$context  = stream_context_create($options);
				$result = file_get_contents($restUrl, false, $context);

				$reply = "Fire call status set to off";
			}

		elseif (strtolower($varCommand) == "outside bright")
			{
				$restUrl = $host . "services/homeassistant/turn_on";
				$options = array(
					'http' => array(
					'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
					'method'  => 'POST',
					'content' => '{"entity_id": "scene.outside_bright"}'
				),
				);

				$context  = stream_context_create($options);
				$result = file_get_contents($restUrl, false, $context);

				$reply = "Outside bright turned on";

				sleep(10);

				$restUrl = $host . "services/shell_command/tts";
				$options = array(
					'http' => array(
					'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
					'method'  => 'POST',
					'content' => '{"message": "I have received a request to turn on all outside lights via SMS messaging"}'
				),
				);

				$context  = stream_context_create($options);
				$result = file_get_contents($restUrl, false, $context);
			}

		elseif (strtolower($varCommand) == "outside blue")
			{
				$restUrl = $host . "services/homeassistant/turn_on";
				$options = array(
					'http' => array(
					'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
					'method'  => 'POST',
					'content' => '{"entity_id": "scene.outside_blue"}'
				),
				);

				$context  = stream_context_create($options);
				$result = file_get_contents($restUrl, false, $context);

				$reply = "Outside blue turned on";
			}

		elseif (strtolower($varCommand) == "outside off")
			{
				$restUrl = $host . "services/homeassistant/turn_off";
				$options = array(
					'http' => array(
					'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
					'method'  => 'POST',
					'content' => '{"entity_id": "group.outsidelights"}'
				),
				);

				$context  = stream_context_create($options);
				$result = file_get_contents($restUrl, false, $context);

				$reply = "Outside lights turned off";

				sleep(10);

				$restUrl = $host . "services/shell_command/tts";
				$options = array(
					'http' => array(
					'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
					'method'  => 'POST',
					'content' => '{"message": "I have received a request to turn off all outside lights via SMS messaging"}'
				),
				);

				$context  = stream_context_create($options);
				$result = file_get_contents($restUrl, false, $context);
			}

			elseif (strtolower($varCommand) == "katie call mom")
				{

					$restUrl = $host . "services/shell_command/alarm_sound";
					$options = array(
						'http' => array(
						'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
						'method'  => 'POST'
					),
					);

					$context  = stream_context_create($options);
					$result = file_get_contents($restUrl, false, $context);

					sleep(1);

					$restUrl = $host . "services/shell_command/alarm_sound";
					$options = array(
						'http' => array(
						'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
						'method'  => 'POST'
					),
					);

					$context  = stream_context_create($options);
					$result = file_get_contents($restUrl, false, $context);

					$restUrl = $host . "services/shell_command/tts";
					$options = array(
						'http' => array(
						'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
						'method'  => 'POST',
						'content' => '{"message": "Attention Katie. Attention Katie. Your mom is trying to get a hold of you and you are not responding to calls and or texts. Please call her as soon as possible. Attention Katie. Attention Katie. Call your mom as soon as possible."}'
					),
					);

					$context  = stream_context_create($options);
					$result = file_get_contents($restUrl, false, $context);

					$reply = "Message to Katie has been played.";
				}

				elseif (strtolower($varCommand) == "katie call mom home")
					{

						$restUrl = $host . "services/shell_command/alarm_sound";
						$options = array(
							'http' => array(
							'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
							'method'  => 'POST'
						),
						);

						$context  = stream_context_create($options);
						$result = file_get_contents($restUrl, false, $context);

						sleep(1);

						$restUrl = $host . "services/shell_command/alarm_sound";
						$options = array(
							'http' => array(
							'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
							'method'  => 'POST'
						),
						);

						$context  = stream_context_create($options);
						$result = file_get_contents($restUrl, false, $context);

						$restUrl = $host . "services/shell_command/tts";
						$options = array(
							'http' => array(
							'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
							'method'  => 'POST',
							'content' => '{"message": "Attention Katie. Attention Katie. Your mom is trying to get a hold of you and you are not responding to calls and or texts. Please call her on the home phone as soon as possible. Attention Katie. Attention Katie. Call your mom on the home phone as soon as possible."}'
						),
						);

						$context  = stream_context_create($options);
						$result = file_get_contents($restUrl, false, $context);

						$reply = "Message to Katie has been played.";
					}

					elseif (strtolower($varCommand) == "katie call mom cell")
						{

							$restUrl = $host . "services/shell_command/alarm_sound";
							$options = array(
								'http' => array(
								'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
								'method'  => 'POST'
							),
							);

							$context  = stream_context_create($options);
							$result = file_get_contents($restUrl, false, $context);

							sleep(1);

							$restUrl = $host . "services/shell_command/alarm_sound";
							$options = array(
								'http' => array(
								'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
								'method'  => 'POST'
							),
							);

							$context  = stream_context_create($options);
							$result = file_get_contents($restUrl, false, $context);

							$restUrl = $host . "services/shell_command/tts";
							$options = array(
								'http' => array(
								'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
								'method'  => 'POST',
								'content' => '{"message": "Attention Katie. Attention Katie. Your mom is trying to get a hold of you and you are not responding to calls and or texts. Please call her on her cell phone as soon as possible. Attention Katie. Attention Katie. Call your mom on her cell phone as soon as possible."}'
							),
							);

							$context  = stream_context_create($options);
							$result = file_get_contents($restUrl, false, $context);

							$reply = "Message to Katie has been played.";
						}

				elseif (strtolower($varCommand) == "katie call dad")
					{

						$restUrl = $host . "services/shell_command/alarm_sound";
						$options = array(
							'http' => array(
							'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
							'method'  => 'POST'
						),
						);

						$context  = stream_context_create($options);
						$result = file_get_contents($restUrl, false, $context);

						sleep(1);

						$restUrl = $host . "services/shell_command/alarm_sound";
						$options = array(
							'http' => array(
							'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
							'method'  => 'POST'
						),
						);

						$context  = stream_context_create($options);
						$result = file_get_contents($restUrl, false, $context);

						$restUrl = $host . "services/shell_command/tts";
						$options = array(
							'http' => array(
							'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
							'method'  => 'POST',
							'content' => '{"message": "Attention Katie. Attention Katie. Your dad is trying to get a hold of you and you are not responding to calls and or texts. Please call him as soon as possible. Attention Katie. Attention Katie. Call your mom as soon as possible."}'
						),
						);

						$context  = stream_context_create($options);
						$result = file_get_contents($restUrl, false, $context);

						$reply = "Message to Katie has been played.";
					}

					elseif (strtolower($varCommand) == "katie call dad home")
						{

							$restUrl = $host . "services/shell_command/alarm_sound";
							$options = array(
								'http' => array(
								'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
								'method'  => 'POST'
							),
							);

							$context  = stream_context_create($options);
							$result = file_get_contents($restUrl, false, $context);

							sleep(1);

							$restUrl = $host . "services/shell_command/alarm_sound";
							$options = array(
								'http' => array(
								'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
								'method'  => 'POST'
							),
							);

							$context  = stream_context_create($options);
							$result = file_get_contents($restUrl, false, $context);

							$restUrl = $host . "services/shell_command/tts";
							$options = array(
								'http' => array(
								'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
								'method'  => 'POST',
								'content' => '{"message": "Attention Katie. Attention Katie. Your dad is trying to get a hold of you and you are not responding to calls and or texts. Please call him on the home phone as soon as possible. Attention Katie. Attention Katie. Call your dad on the home phone as soon as possible."}'
							),
							);

							$context  = stream_context_create($options);
							$result = file_get_contents($restUrl, false, $context);

							$reply = "Message to Katie has been played.";
						}

						elseif (strtolower($varCommand) == "katie call dad cell")
							{

								$restUrl = $host . "services/shell_command/alarm_sound";
								$options = array(
									'http' => array(
									'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
									'method'  => 'POST'
								),
								);

								$context  = stream_context_create($options);
								$result = file_get_contents($restUrl, false, $context);

								sleep(1);

								$restUrl = $host . "services/shell_command/alarm_sound";
								$options = array(
									'http' => array(
									'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
									'method'  => 'POST'
								),
								);

								$context  = stream_context_create($options);
								$result = file_get_contents($restUrl, false, $context);

								$restUrl = $host . "services/shell_command/tts";
								$options = array(
									'http' => array(
									'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
									'method'  => 'POST',
									'content' => '{"message": "Attention Katie. Attention Katie. Your dad is trying to get a hold of you and you are not responding to calls and or texts. Please call him on her cell phone as soon as possible. Attention Katie. Attention Katie. Call your dad on his cell phone as soon as possible."}'
								),
								);

								$context  = stream_context_create($options);
								$result = file_get_contents($restUrl, false, $context);

								$reply = "Message to Katie has been played.";
							}

						elseif (strtolower($varCommand) == "fart")
							{
							$restUrl = $host . "services/shell_command/fart_sound";
							$options = array(
								'http' => array(
								'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
								'method'  => 'POST'
							),
							);

							$context  = stream_context_create($options);
							$result = file_get_contents($restUrl, false, $context);

							sleep(1);

							$restUrl = $host . "services/shell_command/tts";
							$options = array(
								'http' => array(
								'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
								'method'  => 'POST',
								'content' => '{"message": "Pardon, but who just died? It smells like a rotting corpse in here!"}'
							),
							);

							$context  = stream_context_create($options);
							$result = file_get_contents($restUrl, false, $context);
						}

						elseif (strtolower($varCommand) == "barela")
							{
							$restUrl = $host . "services/shell_command/fart_sound";
							$options = array(
								'http' => array(
								'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
								'method'  => 'POST'
							),
							);

							$context  = stream_context_create($options);
							$result = file_get_contents($restUrl, false, $context);

							sleep(1);

							$restUrl = $host . "services/shell_command/tts";
							$options = array(
								'http' => array(
								'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
								'method'  => 'POST',
								'content' => '{"message": "Pardon, but who just died? It smells like a rotting corpse in here. Oh hi Chris, I did not see you come in at first. That explains the smell."}'
							),
							);

							$context  = stream_context_create($options);
							$result = file_get_contents($restUrl, false, $context);
						}

						elseif (strtolower($varCommand) == "air raid")
							{
							$restUrl = $host . "services/shell_command/air_raid_sound";
							$options = array(
								'http' => array(
								'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
								'method'  => 'POST'
							),
							);

							$context  = stream_context_create($options);
							$result = file_get_contents($restUrl, false, $context);
						}

						elseif (strtolower($varCommand) == "zombie")
							{
							$restUrl = $host . "services/shell_command/zombie_sound";
							$options = array(
								'http' => array(
								'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
								'method'  => 'POST'
							),
							);

							$context  = stream_context_create($options);
							$result = file_get_contents($restUrl, false, $context);
						}

						elseif (strtolower($varCommand) == "ghost")
							{
							$restUrl = $host . "services/shell_command/ghost_sound";
							$options = array(
								'http' => array(
								'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
								'method'  => 'POST'
							),
							);

							$context  = stream_context_create($options);
							$result = file_get_contents($restUrl, false, $context);
						}

						elseif (strtolower($varCommand) == "foghorn")
							{
							$restUrl = $host . "services/shell_command/foghorn";
							$options = array(
								'http' => array(
								'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
								'method'  => 'POST'
							),
							);

							$context  = stream_context_create($options);
							$result = file_get_contents($restUrl, false, $context);
						}

						elseif (strtolower($varCommand) == "gunshot")
							{
							$restUrl = $host . "services/shell_command/gunshot";
							$options = array(
								'http' => array(
								'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
								'method'  => 'POST'
							),
							);

							$context  = stream_context_create($options);
							$result = file_get_contents($restUrl, false, $context);
						}

						elseif (strtolower($varCommand) == "siren")
							{
							$restUrl = $host . "services/shell_command/siren";
							$options = array(
								'http' => array(
								'header'  => "Content-Type: application/json\r\nx-ha-access: " . $password . "\r\n ",
								'method'  => 'POST'
							),
							);

							$context  = stream_context_create($options);
							$result = file_get_contents($restUrl, false, $context);
						}

		else
			$reply = "Error: unknown command. Reply commands to get a list of availble commands.";
	}
?>
