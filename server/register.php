<?php

/** 
 * File for recieving initial data from the pi's via a HTTP request.
 * 
 * @author	Humphrey Shotton
 * @version	1.0 (2014-01-16)
 */
 
require_once( 'init.php' );

// Set the content as json
header('Content-type: application/json; charset=UTF-8');

// Checks that all the required keys are present in the post data
$keys = array( "register_password", "register_park_id", "register_pi_id", "register_area_id" );
foreach( $keys as $key )
	if( !array_key_exists( $key, $_POST ) )
		json_error( 'Incomplete post data.' );

// Check that the password is correct
if( $_POST[ 'register_password' ] != Conf::PI_PASSWORD )
	json_error( 'Password incorrect.' );

// Check that the space does not already exist
$query = "SELECT space_id FROM spaces WHERE space_park_id = ? AND space_pi_id = ? AND space_area_code = ?";
$stmt  = DB::get()->prepare($query);
$stmt->bindValue( 1, $_POST[ "register_park_id" ], PDO::PARAM_INT );
$stmt->bindValue( 2, $_POST[ "register_pi_id" ], PDO::PARAM_INT );
$stmt->bindValue( 3, $_POST[ "register_area_id" ], PDO::PARAM_INT );
$stmt->execute();

// If there is a row, cannot continue
if( $stmt->rowCount() != 0 )
	json_error( 'This combination of pi, park and area data has already been registered.' );
	
unset($stmt);
unset($query);

// Check that the park exists
$query = "SELECT park_id FROM parks WHERE park_id = ?";
$stmt  = DB::get()->prepare($query);
$stmt->bindValue( 1, $_POST[ "register_park_id" ], PDO::PARAM_INT );
$stmt->execute();

// If there is a row, cannot continue
if( $stmt->rowCount() != 1 )
	json_error( 'This park does not exist, or there are two of them, which is wrong.' );

// Register the space on the database.
$query2 = "INSERT INTO spaces (space_park_id, space_pi_id, space_area_code) VALUES (?, ?, ?)";
$stmt2  = DB::get()->prepare( $query2 );
$stmt2->bindValue( 1, $_POST[ "register_park_id" ], PDO::PARAM_INT );
$stmt2->bindValue( 2, $_POST[ "register_pi_id" ], PDO::PARAM_INT );
$stmt2->bindValue( 3, $_POST[ "register_area_id" ], PDO::PARAM_INT );
$stmt2->execute();

// Return success.
echo '{"success": "Parking Space has been registered."}';

?>
