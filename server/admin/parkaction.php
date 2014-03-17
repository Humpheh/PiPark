<?php

/**
 * File for setting up the car parks or editing them.
 *
 * @author	Humphrey Shotton
 * @version	1.0 (2014-01-17)
 */

require_once ('../init.php');

if (isset($_POST['park_action']) && $_POST['park_action'] == 'add') {
	
	// Checks that all the required keys are present in the post data
	$keys = array("park_name", "park_description");
	foreach ($keys as $key)
		if (!array_key_exists($key, $_POST))
			json_error('Incomplete post data.');
	
	// Register the space on the database.
	$query2 = "INSERT INTO parks (park_name, park_desc) VALUES (?, ?)";
	$stmt2 = DB::get() -> prepare($query2);
	$stmt2 -> bindValue(1, $_POST["park_name"], PDO::PARAM_INT);
	$stmt2 -> bindValue(2, $_POST["park_description"], PDO::PARAM_INT);
	$stmt2 -> execute();
    
} else if (isset($_POST['park_action']) && $_POST['park_action'] == 'update') {
	
	// Checks that all the required keys are present in the post data
	$keys = array("park_id", "park_name", "park_description");
	foreach ($keys as $key)
		if (!array_key_exists($key, $_POST))
			json_error('Incomplete post data.');

	if( is_int ( trim($_POST[ 'park_id' ]) ) )
		json_error('Park id is not a number. (update)');
    
	// Register the space on the database.
	$query2 = "UPDATE parks SET park_name = ?, park_desc = ? WHERE park_id = ?";
	$stmt2 = DB::get() -> prepare($query2);
	$stmt2 -> bindValue(1, $_POST["park_name"], PDO::PARAM_INT);
	$stmt2 -> bindValue(2, $_POST["park_description"], PDO::PARAM_INT);
	$stmt2 -> bindValue(3, intval($_POST["park_id"]), PDO::PARAM_INT);
	$stmt2 -> execute();
	
} else if (isset($_POST['park_action']) && $_POST['park_action'] == 'delete') {
	
	// Checks that all the required keys are present in the post data
	$keys = array("park_id");
	foreach ($keys as $key)
		if (!array_key_exists($key, $_POST))
			json_error('Incomplete post data.');
		
	// Register the space on the database.
	$query2 = "DELETE FROM parks WHERE park_id = ?";
	$stmt2 = DB::get() -> prepare($query2);
	$stmt2 -> bindValue(1, intval($_POST["park_id"]), PDO::PARAM_INT);
	$stmt2 -> execute();
	
}

header("Location: parks.php");
?>
