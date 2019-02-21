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

echo 'Calling on ' . $channel . ' channel: ' . $number;

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
