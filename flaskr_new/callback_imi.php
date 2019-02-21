<?php

if (array_key_exists('number', $_GET)) {
   $number = substr($_GET["number"], -10);
} else {
   echo 'Missing number.';
   exit(1);
}
if (array_key_exists('channel', $_GET)) {
   $channel = $_GET["channel"];
} else {
   $channel = 'main';
}

echo 'Calling on ' . $channel . ' channel: ' . $number . 'Via IMIMobile Solution';


//********************************************************************************************
//IMI functionality starts
echo '<br>IMI messages start.<br>';
$url = "http://api-openhouse.imimobile.com/1/obd/thirdpartycall/callSessions";
//X-www-form-urlencoded field to be sent in the POST body.
$rawdata="address=!address!&callflow_id=!menu!";
/*
Replace the following parameters:
address
menu(the call flow id created in the OPENHOUSE website)
*/
$address=$number;
$menu="6300";
$rawdata=str_replace("!address!","$address" ,$rawdata);
$rawdata=str_replace("!menu!","$menu" ,$rawdata);
//Curl variable to store headers and X-www-form-urlencoded field.
$ch = curl_init($url);
//1 stands for posting.
curl_setopt($ch, CURLOPT_POST, 1);
//Replace the secure Key associated with the registered service from your account on the website 
curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/X-www-form-urlencoded','key:01b8ab23-78cd-4317-bf41-95dd22fcece0'));
curl_setopt($ch, CURLOPT_POSTFIELDS, $rawdata);
$response = curl_exec($ch);
curl_close($ch);
echo $response;
echo '<br>IMI messages end <br>';

$ch2 = curl_init();
curl_setopt($ch2, CURLOPT_URL, "http://flask-aws-dev.ap-south-1.elasticbeanstalk.com/CGSwaraRecordNumber/$address");
curl_setopt($ch2, CURLOPT_HEADER, 0);
curl_exec($ch2);
curl_close($ch2);
//IMI functionality ends
//********************************************************************************************

$filename = $channel . '-' . $number . '.call';
$srcfile = '/tmp/' . $filename;
$dstfile = '/var/spool/asterisk/outgoing/' . $filename;
$contents = "Context: callback\n" .
	    "Extension: 1\n" .
            "MaxRetries: 1\n" .
            "RetryTime: 30\n" .
            "Channel: dahdi/g1/0" . $number . "\n" .
            "SetVar: swaraChannel=" . $channel . "\n" .
            "SetVar: targetnumber=" . $number . "\n" .
            "callerid: " . $number . "\n" .
            "Account: " . $number . "\n";
file_put_contents($srcfile, $contents);
$result = rename($srcfile, $dstfile);
if ($result) {
//   echo '  [OK]';
} else {
   echo '  [FAILED]';
}
?>