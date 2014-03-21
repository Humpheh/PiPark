<?php

/** 
 * Functions for use with the site.
 * 
 * @author	Humphrey Shotton
 * @version	1.1 (2014-03-21)
 */

/**
 * To throw a json error with a message
 * @param $message message to display in the JSON
 */
function json_error( $message ){
	echo '{"error": "', $message, '"}';
	exit();
}

/**
 * Get the query to find the number of spaces in the car park.
 * @param $id id of the space to find
 * @return the query for that space
 */
function get_num_space_query($id){
	return "SELECT count(*) 
		FROM spaces a
		LEFT JOIN (
			SELECT *
			FROM updates b
			WHERE update_time = (
				SELECT max( update_time )
				FROM updates um
				WHERE um.update_space_id = b.update_space_id
			)
			GROUP BY update_space_id
		) b ON a.space_id = b.update_space_id
		WHERE a.space_park_id = " . ($id) . " AND b.update_status <> 0";
}

/**
 * Print the time ago in a friendly format.
 * Function thanks to http://css-tricks.com/snippets/php/time-ago-function/
 *
 * @param $time time string to get the ago of
 * @return string of the time passed since the input
 */
function ago($time) {
	if(is_string($time)) 
		$time = strtotime($time);
	
	$periods = array("second", "minute", "hour", "day", "week", "month", "year", "decade");
	$lengths = array("60","60","24","7","4.35","12","10");
	
	$now = time();
	
	$difference = $now - $time;
	$tense = "ago";
	
	for($j = 0; $difference >= $lengths[$j] && $j < count($lengths)-1; $j++) {
	   $difference /= $lengths[$j];
	}
	
	$difference = round($difference);
	
	if($difference != 1) {
	   $periods[$j].= "s";
	}
	
	if($difference < 0) return "From the future!";
	
	return "$difference $periods[$j] ago";
} 

/**
 * Makes strings safer for MySql and XSS.
 * @param $variable variable to make safe.
 * @return safe variable with escaped chars
 */
function make_safe($variable) {
   $variable = strip_tags(mysql_real_escape_string(trim($variable)));
   return $variable; 
}

?>