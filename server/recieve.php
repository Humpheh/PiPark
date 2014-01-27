<?php

/** 
 * File for recieving the data from the pi's via a HTTP request.
 * 
 * @author	Humphrey Shotton
 * @version	1.0 (2014-01-16)
 */
 
require_once( 'init.php' );

// Set the content as json
header('Content-type: application/json; charset=UTF-8');

// Checks that all the required keys are present in the post data
$keys = array( "update_password", "update_park_id", "update_pi_id", "update_area_id", "update_status" );
foreach( $keys as $key )
	if( !array_key_exists( $key, $_POST ) )
		json_error( 'Incomplete post data.' );

// Check that the password is correct
if( $_POST[ 'update_password' ] != Conf::PI_PASSWORD )
	json_error( 'Password incorrect.' );

// Get the space_id from the database using the park, pi and area id's
$query = "SELECT space_id FROM spaces WHERE space_park_id = ? AND space_pi_id = ? AND space_area_code = ?";
$stmt  = DB::get()->prepare($query);
$stmt->bindValue( 1, $_POST[ "update_park_id" ], PDO::PARAM_INT );
$stmt->bindValue( 2, $_POST[ "update_pi_id" ], PDO::PARAM_INT );
$stmt->bindValue( 3, $_POST[ "update_area_id" ], PDO::PARAM_INT );
$stmt->execute();

// If there is more than one row, or no row, throw an error
if( $stmt->rowCount() != 1 )
	json_error( 'Pi, park or area data not registered on database.' );

// Get the space id from the query
$row = $stmt->fetch( PDO::FETCH_ASSOC );
$spaceid = $row[ 'space_id' ];

// Update the database with the new values.
$query2 = "INSERT INTO updates (update_space_id, update_status) VALUES (?, ?)";
$stmt2  = DB::get()->prepare( $query2 );
$stmt2->bindValue( 1, $spaceid, PDO::PARAM_INT );
$stmt2->bindValue( 2, $_POST[ "update_status" ], PDO::PARAM_INT );
$stmt2->execute();

// Return success.
echo '{"success": "Database updated."}';

?>
