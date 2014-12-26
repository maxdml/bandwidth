<?php

$str_json = file_get_contents('php://input') . "\n";
error_log("raw post data: $str_json");

$handle = fopen('/var/www/html/bandwidth/raw_data', 'a') or die ('Can\'t open file' . "\n");

if (!fwrite($handle, $str_json)) {
    error_log("could not write to file $handle");;
    exit;
}

fclose($handle);

?>
