"""
Author: Humphrey Shotton and Nicholas Sanders
Filename: imageread.py
Version: [2014/01/31]

Description:
Utility functions for PiPark Smart Parking Sensor programs.

"""

# -----------------------------------------------------------------------------
#  Imports
# -----------------------------------------------------------------------------
# python
import sys
import time

# PiPark
import data.settings as s
    
try: 
    import picamera
except ImportError:
    print "ERROR: PiCamera Module needs to be installed."
    sys.exit()

# Pythonware, Image Library
try:
    from PIL import Image
except ImportError:
    print "ERROR: Python Image Library needs to be installed."
    sys.exit()


# -----------------------------------------------------------------------------
#  Setup Camera
# -----------------------------------------------------------------------------
def setup_camera(is_fullscreen = True):
    """
    Setup the PiCam to default PiPark settings, and return the camera as
    an object.
    
    Keyword Arguments:
    is_fullscreen -- Boolean value. True for fullscreen, false for window.
    
    """
    
    # ensure that camera is correctly installed and set it up to output to a
    # window and turn off AWB and exposure modes. If camera does not exist
    # print error message and quit program.
    camera = picamera.PiCamera()
    camera.resolution = s.PICTURE_RESOLUTION
    camera.preview_fullscreen = is_fullscreen
    camera.awb_mode = "off"
    #camera.exposure_mode = "off"
    if not is_fullscreen: camera.preview_window = s.CAMERA_WINDOW_SIZE
    time.sleep(s.WAKEUP_DELAY)  # camera wake-up time: 2 s
    
    return camera

# -----------------------------------------------------------------------------
#  Load Image
# -----------------------------------------------------------------------------
def load_image(filename):
    """
    Loads a picture using PIL.

    Arguments:
    filename -- Filename to the image.

    Return:
    (images, pixels) -- Tuple of image data and pixel data.

    Raises:
    IOError -- When image is not found.
    
    """
    
    # Load the file
    print "INFO: Loading Image: " +str(filename)
    image = Image.open(filename)
    pixels = image.load()
    print "INFO: Image loaded."
    
    return (image, pixels)


# -----------------------------------------------------------------------------
#  Get Area Average
# -----------------------------------------------------------------------------
def get_area_average(pixels, x, y, w, h):
    """
    Calculate and return the average RGB values in a selected area of a picture
    and return the result as a list.
    
    Arguments:
    pixels -- Pixel data of image file.
    x -- Starting x co-ordinate of area.
    y -- Starting y co-ordinate of area.
    w -- Width of area.
    h -- Height of area.
    
    Return:
    totals -- List of average RGB value in selected area.
    
    """
    
    # setup variables
    totals = [0, 0, 0, 0]
    
    # for each pixel in the defined area total up the RGB values and then 
    # calculate the average of each. Finally calculate the average of all three
    # values as the last element of the list 'totals'.
    for cx in range(x, x + w):
        for cy in range(y, y + h):
            for i in range(3):   
                totals[i] += pixels[cx, cy][i]
    
    # calculate average RGB values by dividing cumulative totals by total
    # number of pixels
    num_pixels = w * h
    for i in range(3):   
        totals[i] /= num_pixels

    # get the average of all colours.
    totals[3] = (totals[0] + totals[1] + totals[2]) / 3
    
    return totals


# -----------------------------------------------------------------------------
#  Compare Area
# -----------------------------------------------------------------------------
def compare_area(test, expected):
    """
    Compare the RGB values of the test average RGB values and the expected 
    average RGB values against the image threshold.
    
    Arguments:
    test -- List of test area average RGB values.
    expected -- List of expected area average RGB values.
    
    Returns:
    is_different -- (Bool) True if threshold is exceeded and false if not.
    
    """
    
    # ensure test and expected are both lists and of the same length
    if not isinstance(test, list) or not isinstance(expected, list):
        raise ValueError("Colour arrays are not lists.")
    
    if len(test) != len(expected):
        raise ValueError("Colour arrays are not same length.")
    
    # set boolean, then compare each RGB value and if threshold is exceeded
    # change bool from False to True
    is_different = False
    
    for test_value, expected_value in zip(test, expected):
        if abs(test_value - expected_value) > s.IMAGE_THRESHOLD:
            is_different = True
    
    return is_different


# -----------------------------------------------------------------------------
#  Test
# -----------------------------------------------------------------------------   
def test(filename):
    """
    Test functions in this module (get_area_average() and compare_area()).
    
    Arguments:
    filename -- Filename of the image to be tested.
    
    """
    
    # Load the image and pixel data for the file
    image, pixels = load_image(str(filename))
    
    # compare the areas in the image using module functions
    test_area = get_area_average(pixels, 50, 600, 620, 50)
    expected_area = get_area_average(pixels, 1500, 600, 300, 300)

    compare_area(test_area, expected_area)
