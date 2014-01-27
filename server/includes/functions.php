<?php

/** 
 * Functions for use with the site.
 * 
 * @author	Humphrey Shotton
 * @version	1.0 (2014-01-27)
 */

/**
 * To throw a json error with a message
 */
function json_error( $message ){
	echo '{"error": "', $message, '"}';
	exit();
}

/**
 * Get the query to find the number of spaces in the car park.
 */
function get_num_space_query($id){
	return "SELECT count(*) FROM updates a 
			INNER JOIN ( SELECT update_space_id, MAX(update_time) max_date FROM updates GROUP BY 			update_space_id ) b 
				ON a.update_space_id = b.update_space_id AND a.update_time = b.max_date 
			LEFT JOIN spaces c ON space_id = a.update_space_id 
		WHERE space_park_id = " . intval($id) . " AND update_status <> 0";
}

/*
 * Print the time ago in a friendly format.
 * Function thanks to http://css-tricks.com/snippets/php/time-ago-function/
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

?>