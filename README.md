# PiPark

**By Humphrey Shotton and Nicholas Sanders**

---

Raspberry Pi car parking sensor with server.

View the website [http://humpheh.github.io/PiPark/](http://humpheh.github.io/PiPark/)!

Images of our test setup can be seen [here (http://imgur.com/a/VdfVp)](http://imgur.com/a/VdfVp).

## Setup Instructions
To setup server, see [server/README.md](server/README.md).

To setup pi software, see [pi/README.md](pi/README.md).

## What you will need
To setup this software, you will need:
* Raspberry Pi
* Raspberry Pi Camera
* Computer to run as the server
* Power and internet connection to the Pi (wired or wireless)
* Keyboard and mouse for Pi setup

### Pi Software
On the Pi, you will need to have the software for:
* Python Image Library (PIL): [https://developers.google.com/appengine/docs/python/images/installingPIL#linux](https://developers.google.com/appengine/docs/python/images/installingPIL#linux)
* PiCamera: [https://pypi.python.org/pypi/picamera](https://pypi.python.org/pypi/picamera)

Most Raspberry Pi's will also already have the following installed, however they are also required to run the Pi software:
* Python 2.7 (Python 3 is not supported)

### Server Software
The server must have:
* MySQL
* PHP

Both of these are available on most web servers, or part of the open source XAMPP project, if running on a computer [http://www.apachefriends.org/](http://www.apachefriends.org/).
