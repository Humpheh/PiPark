<?php

/** 
 * File for deregistering parking spaces from pi's via a HTTP request.
 * 
 * @author	Humphrey Shotton
 * @version	1.0 (2014-01-23)
 */
 
require_once( 'init.php' );

// Set the content as json
header('Content-type: application/json; charset=UTF-8');

// Checks that all the required keys are present in the post data
$keys = array( "deregister_password", "deregister_pi_id" );
foreach( $keys as $key )
	if( !array_key_exists( $key, $_POST ) )
		json_error( 'Incomplete post data.' );

// Check that the password is correct
if( $_POST[ 'deregister_password' ] != Conf::PI_PASSWORD )
	json_error( 'Password incorrect.' );

// Remove the spaces from the database 
$query = "DELETE FROM spaces WHERE space_pi_id = ?";
$stmt  = DB::get()->prepare($query);
$stmt->bindValue( 1, $_POST[ "deregister_pi_id" ], PDO::PARAM_INT );
$stmt->execute();

// Return success.
echo '{"success": "Parking Spaces from this pi ID have been deregistered."}';

?>
