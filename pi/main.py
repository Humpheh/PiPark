"""
Authors: Nicholas Sanders & Humphrey Shotton
Filename: main.py
Version: 2.0 [2014/03/25]

Description:
PiPark Smart Sparking Sensor. PiPark detects changes in car parking spaces as 
specified by user after running the setup script (./pipark_setup.py). 

When changes are consistent over three ticks, the server is updated with the 
present availability of each parking space.

"""

import urllib

import imageread
import senddata
import settings as s

try:
    # check setup_data exists
    import setup_data
except ImportError:
    print "ERROR: setup_data.py does not exist. Run ./pipark_setup.py first."
    sys.exit()


# ==============================================================================
#
#       Main Program
#
# ==============================================================================
def main():
    """
    Run main program loop. Detect changes to parking spaces and update 
    appropriate availabity of the spaces to the server.
    
    """
    
    # setup camera and image save location
    camera = imageread.setup_camera()
    camera.start_preview()
    image_location = "./images/pipark.jpeg"

    # load data sets and count num spaces on control boxes
    space_boxes, control_boxes = __setup_box_data()
    
    num_spaces = len(space_boxes)
    num_controls = len(control_boxes)

    print "Number of spaces:", num_spaces, "Number of Control boxes:", num_controls
    
    assert num_spaces > 0
    assert num_controls == 3
    
    last_status = [None for i in range(10)]
    last_ticks = [3 for i in range(10)]
    
    # run centralised program loop
    while True:
        space_averages = []
        control_averages = []
        
        # take new picture, save to specified location
        camera.capture(image_location)
        print "INFO: New picture taken,", image_location

        # load image
        try:
            image = imageread.Image.open(image_location)
            pixels = image.load()
        except:
            print "ERROR: Image has failed to load."

        # setup spaces
        for space in space_boxes:
            space_x = space[2]
            space_y = space[3]
            space_w = abs(space[4] - space[2])
            space_h = abs(space[5] - space[3])
            
            #space_x, space_y, space_w, space_h = __get_area_values(space)
            
            print "Space dims:", "x", space_x, "y", space_y, "w", space_w, "h", space_h

            space_averages.append(imageread.get_area_average(pixels, space_x, space_y, space_w, space_h))

        # setup control
        for control in control_boxes:
            
            control_x = control[2]
            control_y = control[3]
            control_w = abs(control[4] - control[2])
            control_h = abs(control[5] - control[3])

            #control_x, control_y, control_w, control_h = __get_area_values(control)

            print "Control dims:", "x", control_x, "y", control_y, "w", control_w, "h", control_h

            control_averages.append(imageread.get_area_average(pixels, control_x, control_y, control_w, control_h))
            
        print "\n\n"
        # compare control points to spaces
        for i, space in zip(space_boxes, space_averages):

            num_controls = 0
            for control in control_averages:
                if imageread.compare_area(space, control):
                    num_controls += 1

            # Determine if occupied
            is_occupied = False
            if num_controls >= 2: is_occupied = True
            
            print "INFO: Space", i[0], "is", ("occupied" if is_occupied else "vacant"), "\n"
            
            if last_status[i[0]] != is_occupied:
                print "INFO: Detected change in space", i[0]
                print "INFO: Space", i[0], "has been the", ("occupied" if is_occupied else "vacant"), "for", last_ticks[i[0]], "tick(s).\n"
                if last_ticks[i[0]] < 3:
                    last_ticks[i[0]] += 1
                else:
                    last_status[i[0]] = is_occupied
                    last_ticks[i[0]] = 1
                    print "INFO: Space", i[0], "has changed status, sending update to server...\n"
                    num = 1 if is_occupied else 0
                    print senddata.send_update(i[0], num), "\n"
            else:
                last_ticks[i[0]] = 1
                
            # old version    
            """if num_controls >= 2:
               # last_status
                print "INFO: Space", i[0], "occupied!"
                print senddata.send_update(i[0], 1), "\n"
            else:
                print "INFO: Space", i[0], "vacant!"
                print senddata.send_update(i[0], 0), "\n" """

        print "INFO: Sleeping for 5s"
        imageread.time.sleep(5)

# -----------------------------------------------------------------------------
#  Get Area Values
# -----------------------------------------------------------------------------
def __get_area_values(area):
    """
    Calculate the co-ordinates and widths of the area values, from the 
    resolution of the image used.
    
    Keyword Arguments:
    area -- tuple in form (x1, y1, x2, y2) from setup.py

    Returns:
    x, y, width, height
    """

    try:
        assert isinstance(area, tuple)
    except AssertionError:
        print "ERROR: Area must be tuple data type [__get_area_values()]."

    min_x_percent = area[2] if area[2] < area[4] else area[4]
    min_y_percent = area[3] if area[3] < area[5] else area[5]
    width_percent = abs(area[2] - area[4])
    height_percent = abs(area[3] - area[5])

    min_x = int(min_x_percent * s.PICTURE_RESOLUTION[0])
    min_y = int(min_y_percent * s.PICTURE_RESOLUTION[1])
    width = int(width_percent * s.PICTURE_RESOLUTION[0])
    height = int(height_percent * s.PICTURE_RESOLUTION[1])

    return min_x, min_y, width, height

# -----------------------------------------------------------------------------
#  Setup Box Data
# -----------------------------------------------------------------------------
def __setup_box_data():
    """Import and return the boxes dictionary from setup_data.py. """
    
    # attempt to load dictionary from setup_data.py, if file does not exist
    # print error message and quit the program
    try:
        box_data = setup_data.boxes
        print "INFO: box_data successfully created."
    except:
        print "ERROR: setup_data.py does not contain the variable 'boxes'."
        sys.exit()
    
    # setup_data.py exists, check that dictionary contains items, if dicionary
    # is empty print error message and quit the program
    if not box_data:
        print "ERROR: boxes in setup_data.py is empty!"
        sys.exit()
    else:
        print "INFO: box_data contains data!"

    space_boxes = []
    control_boxes = []
    
    for data_set in box_data:
        if data_set[1] == 0: space_boxes.append(data_set)
        elif data_set[1] == 1: control_boxes.append(data_set)
        else: print "ERROR: Box-type not set to either 0 or 1."

    print "space boxes:", space_boxes, "\ncontrol boxes:", control_boxes
    return space_boxes, control_boxes

    
# -----------------------------------------------------------------------------
#  Run Program
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
