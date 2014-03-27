"""
Author: Humphrey Shotton and Nicholas Sanders
Filename: settings.py
Version: [2014/01/20]

Description:
Settings file for car park sensor.

"""
from uuid import getnode as get_mac
PI_ID = get_mac() # Creates a unique ID for the PI

# -----------------------------------------------------------------------------
#  Camera Settings
# -----------------------------------------------------------------------------
WAKEUP_DELAY = 2
PICTURE_DELAY = 2
PICTURE_RESOLUTION = (960, 540)
CAMERA_WINDOW_SIZE = (0, 0, 960, 540)

# -----------------------------------------------------------------------------
#  Picture Settings
# -----------------------------------------------------------------------------
MAX_PICTURES = 4
IMAGE_THRESHOLD = 20

# -----------------------------------------------------------------------------
#  UI Settins
# ----------------------------------------------------------------------------- 
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

# -----------------------------------------------------------------------------
#  Server Settings and Pi Identification
# -----------------------------------------------------------------------------
PARK_ID = 1

SERVER_PASS = 'pi'
SERVER_URL = "http://10.173.33.129/pipark/server/"

