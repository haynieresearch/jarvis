<?php
require __DIR__ . '/vendor/autoload.php';
use Twilio\Rest\Client;

$number = $_GET['From'];
$body = $_GET['Body'];

$pageNumbers = array(
	"+14355251418", //WashCo Dispatch
	"+14356197079" //Chris
);

$responseNotifyNumbers = array(
	"+14355251418", //Lance
	"+17252448709", //Ryan
	"+14356197079" //Chris
);

$activeMembers = array(
	"+14355251418" => "Lance",
	"+17252448709" => "Ryan",
	"+14356197079" => "Chris"
);

//Key value check
if (array_key_exists("$number",$activeMembers))
  {
  	$validNumber = "TRUE";
  }
else
  {
  	$validNumber = "FALSE";
  }

//Main response processing
if (in_array($number, $pageNumbers) && strtolower(substr($body,0,7)) == "s: sanf")
	{
		send_page($body);
	}
elseif (in_array($number, $pageNumbers) && strtolower(substr($body,0,5)) == "page:")
	{
		manual_page($body);
	}
elseif ($validNumber == "TRUE")
	{
		processResponse($body);
	}
else
	{
		$reply = "Error: You are not authorized. Please contact Lance Haynie to have your information programmed.";
	}

function send_page($varCommand)
	{
		global $number;
		global $smsNumber;
		global $body;
		global $activeMembers;

		$sid = 'AC4bbd8542d05810f24efaf2c28adc5763';
		$token = 'df267e8a426269917a52650e4b122855';
		$client = new Client($sid, $token);

		foreach ($activeMembers as $smsNumber => $name) {
		$client->messages->create(
			$smsNumber,
			array(
					'from' => '+14352720192',
					'body' => "$name, Santa Clara Fire Department has been paged. Please indicate your response (number only) for incident tracking.\n\nReply With:\n1 - Responding Immediately\n2 - Responding Delayed (15+ Minutes)\n3 - Standing By\n4 - Unable to Respond"
			)
		);
		}
	}

	function manual_page($varCommand)
		{
			global $number;
			global $smsNumber;
			global $body;
			global $activeMembers;

			$sid = 'AC4bbd8542d05810f24efaf2c28adc5763';
			$token = 'df267e8a426269917a52650e4b122855';
			$client = new Client($sid, $token);

			foreach ($activeMembers as $smsNumber => $name) {
			$client->messages->create(
				$smsNumber,
				array(
						'from' => '+14352720192',
						'body' => "$name, Santa Clara Fire Department has been manually paged. Here is the information: " . substr($varCommand, 5) . "\nPlease indicate your response (number only) for incident tracking.\n\nReply With:\n1 - Responding Immediately\n2 - Responding Delayed (15+ Minutes)\n3 - Standing By\n4 - Unable to Respond"
				)
			);
			}
		}

	function processResponse($response)
		{
			global $number;
			global $smsNumber;
			global $body;
			global $activeMembers;
			global $reply;
			global $responseNotifyNumbers;

			$sid = 'AC4bbd8542d05810f24efaf2c28adc5763';
			$token = 'df267e8a426269917a52650e4b122855';
			$client = new Client($sid, $token);

			if ($response == "1")
				{
					$reply = "Response accepted: You are responding immediately.";

					foreach ($responseNotifyNumbers as $smsNumber) {
					$client->messages->create(
						$smsNumber,
						array(
								'from' => '+14352720192',
								'body' => $activeMembers[$number] . " is responding immediately."
						)
					);
					}
				}
			elseif ($response == "2")
				{
					$reply = "Response accepted: You are responding delayed.";

					foreach ($responseNotifyNumbers as $smsNumber) {
					$client->messages->create(
						$smsNumber,
						array(
								'from' => '+14352720192',
								'body' => $activeMembers[$number] . " is responding delayed."
						)
					);
					}
				}
			elseif ($response == "3")
				{
					$reply = "Response accepted: You are standing by.";

					foreach ($responseNotifyNumbers as $smsNumber) {
					$client->messages->create(
						$smsNumber,
						array(
								'from' => '+14352720192',
								'body' => $activeMembers[$number] . " is standing by."
						)
					);
					}
				}
			elseif ($response == "4")
				{
					$reply = "Response accepted: You are unable to respond.";

					foreach ($responseNotifyNumbers as $smsNumber) {
					$client->messages->create(
						$smsNumber,
						array(
								'from' => '+14352720192',
								'body' => $activeMembers[$number] . " is unable to respond."
						)
					);
					}
				}
			else
				{
					$reply = "Unknown reponse, please make sure you replied correctly without any extraneous information.";
				}
		}

header('Content-Type: text/xml');
?>
<Response>
    <Message>
    	<?php echo $reply; ?>
    </Message>
</Response>
