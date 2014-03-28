<?php

/**
 * Class for storing global variables.
 *
 * @author	Humphrey Shotton
 * @version	1.1 (2014-03-21)
 */

class Conf{
	// MySQL Database Settings.
	const DB_HOST = "127.0.0.1";
	const DB_USER = "root";
	const DB_PASS = "";
	const DB_DATABASE = "raspi";
	
	// Base URL on the server.
	const URL_BASE = "/pipark/server/";
	
	// The password for the pi's to submit data.
	const PI_PASSWORD = 'exeterPiPark';
	
	// Title of the website.
	const TITLE = 'PiPark';
	
	// Google maps API key
	const MAPS_API_KEY = 'AIzaSyCxTGtd15r1PXxGyPSA17YjoPcN73ENmPc';
}
?>