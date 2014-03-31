<?php

/**
 * API for acessing data via JSON.
 *
 * @author	Humphrey Shotton
 * @version	1.0 (2014-01-28)
 */

require_once ('init.php');

// Set the content as json
header('Content-type: application/json; charset=UTF-8');

$stmt = DB::get()->prepare('SELECT *, (SELECT count(*) FROM spaces WHERE space_park_id = park_id) AS ps, 
			('.get_num_space_query("park_id").') AS spaces FROM parks');
$stmt->execute();
$res = $stmt->fetchAll(PDO::FETCH_ASSOC);

echo '{
    "carparks":[';

foreach ($res as $row){
	echo '{
        "id": '.intval($row['park_id']).',
        "name": "'.($row['park_name']).'",
        "desc": "'.($row['park_desc']).'",
        "totalspaces": '.intval($row['ps']).',
        "usedspaces": '.intval($row['spaces']).',
        "location": "'.($row['park_location']).'"
    }';
	if ($row != end($res)) echo ',';
}
echo ']
}';

?>