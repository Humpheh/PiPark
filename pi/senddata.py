"""
Author: Humphrey Shotton
Filename: senddata.py
Version: 1.0 (2014-01-17)

Description:
Pi Car Park sensor server communication module.

Used to send update data about changed in the car parking spaces
to a central server.

"""
import urllib
import urllib2
import json
import data.settings as s

def post_request(vals, url):
    """
    Build a post request.

    Args:
        vals: Dictionary of (field, values) for the POST
            request.
        url: URL to send the data to.

    Returns:
        Dictionary of JSON response or error info.
    """
    # Build the request and send to server
    data = urllib.urlencode(vals)
    
    try:
        request  = urllib2.Request(url, data)
        response = urllib2.urlopen(request)
    except urllib2.HTTPError, err:
        return {"error": err.reason, "error_code": err.code}
    except:
        return {"error": "Error in connecting to server."}
    # Return the response parsed as a array from json
    try:
        return json.loads(response.read())
    except ValueError, err:
        return {"error": "JSON decoding error"}

def send_update(area_id, status_code):
    """
    Sends the data of parking space status to the server
    using a HTTP POST request.

    Args:
        area_id: Car park space area id.
        status_code: Status of the car park.

    Returns:
        Dictionary of elements from the JSON response.
    """
    # Create the post data
    vals = {"update_password" : s.SERVER_PASS,
            "update_park_id" : s.PARK_ID,
            "update_pi_id" : s.PI_ID,
            "update_area_id" : area_id,
            "update_status" : status_code}

    return post_request(vals, s.SERVER_URL + "recieve.php")


def register_area(area_id):
    """
    Sends the data to register a new parking space to the
    server using a HTTP POST request.

    Args:
        area_id: The area id to register.

    Returns:
        Dictionary of elements from the JSON response.
    """
    # Create the post data
    vals = {"register_password" : s.SERVER_PASS,
            "register_park_id" : s.PARK_ID,
            "register_pi_id" : s.PI_ID,
            "register_area_id" : area_id}

    return post_request(vals, s.SERVER_URL + "register.php")


def deregister_pi():
    """
    Deregisters all areas associated with this pi.
    
    Returns:
        Dictionary of elements from the JSON response.
    """
    # Create the post data
    vals = {"deregister_password" : s.SERVER_PASS,
            "deregister_pi_id" : s.PI_ID}

    return post_request(vals, s.SERVER_URL + "deregister.php")


if __name__ == "__main__":
    # Example for sending updates
    for i in range(0,5):
        j = send_update(i, 1)
        print j
