#!/usr/bin/env python
"""
Authors: Nicholas Sanders & Humphrey Shotton
Filename: main.py
Version: 2.1 [2014/03/27]

Main application. Two threads are created, one to deal with GUI and inputs, and
the other to handle the PiPark Smart Parking System detection software.

"""
# les importations
import Tkinter as tk
import tkMessageBox
import thread
import time
import urllib

from PIL import Image, ImageTk

import senddata
import imageread
import data.settings as s

try:
    # check setup_data exists
    import setup_data
except ImportError:
    # oh noes, it doesn't =(
    print "ERROR: setup_data.py does not exist. Run ./pipark_setup.py first."
    sys.exit(1)

# global variables
app = None
camera = None
has_quit = False
occupancy = [None for i in range(10)]  # list of booleans. True for occupied, False for empty. None for no space.

# ==============================================================================
#
#       Tkinter Application
#
# ==============================================================================
class MainApplication(tk.Frame):
    # ------------------------------------------------------------------------------
    #  Instance Attributes
    # ------------------------------------------------------------------------------
    
    # output messages to the terminal?
    __is_verbose = s.IS_VERBOSE
    
    # pi camera
    __camera = None
    __preview_is_active = False
    
    __label = ""
    
    # --------------------------------------------------------------------------
    #  Constructor Method
    # --------------------------------------------------------------------------
    def __init__(self, master = None):
        """Application constructor method. """
        if self.__is_verbose: print "INFO: Application constructor called."

        # run super constructor method
        tk.Frame.__init__(self, master)
        
        # apply grid layout
        self.grid()
        
        # give application a reference to the global camera object
        global camera
        self.__camera = camera
        self.__camera.awb_mode = 'auto'
        self.__camera.exposure_mode = 'auto'
        
        # populate the application WITH W-W-W-WWIDDDDGEETTSS
        self.__createWidgets()
        
        # create canvas to display logo
        self.logo = tk.Canvas(self, width = 400, height = 148)
        self.logo.grid(row = 0, column = 0, rowspan = 1, columnspan = 2)
        self.loadImage("./images/logo_main.jpeg", self.logo, 400/2, 148/2)
        self.updateText()
        
        # create key-press handlers -> set focus to this frame
        self.bind("<Escape>", self.escapePressHandler)
        self.focus_set()
    
    def updateText(self):
        num_spaces = 0
        occupied = 0
        
        global occupancy
        
        
        for i in occupancy:
            if i != None: num_spaces += 1
            if i == True: occupied += 1
        
        self.__label = "Parking Spaces Available:", occupied, "/", num_spaces
        
        self.loadImage("./images/logo_main.jpeg", self.logo, 400/2, 148/2)
        self.logo.create_text((200, 130), text = self.__label, fill = "white")
        
    # --------------------------------------------------------------------------
    #  Key Event Handlers
    # --------------------------------------------------------------------------
    def escapePressHandler(self, event):
        """Handle ESCAPE key events. """
        
        if self.__is_verbose: print "ACTION: ESCAPE key pressed."
        
        
        # if the camera is previewing -> stop the preview
        if self.__camera and self.__preview_is_active:
            self.__camera.stop_preview()
            self.__preview_is_active = False
            if self.__is_verbose: print "INFO: Camera preview stopped. "
            
            # reset focus to application frame
            self.focus_set()
    
    # --------------------------------------------------------------------------
    #  Button Press Events
    # --------------------------------------------------------------------------
    def clickStartPreview(self):
        """Handle 'Start Preview' button click events. """
        if self.__is_verbose: print "ACTION: 'Start Preview' clicked! "
        
        # turn on the camera preview
        if self.__camera and not self.__preview_is_active:
            
            tkMessageBox.showinfo(
                title = "Show Camera Feed",
                message = "Press the ESCAPE key to exit preview mode"
                )

            #self.__camera.brightness = 70;
            #self.__camera.awb_mode = 'auto';
            
            self.__camera.start_preview()
            self.__preview_is_active = True
            if self.__is_verbose: print "INFO: Camera preview started. "
            
            # reset focus to the application frame
            self.focus_set()
    
    
    def clickQuit(self):
        """Handle 'Quit' button click events. """
        
        # use global variable 'has_quit'
        global has_quit
        
        self.quit()
        self.master.destroy()
        has_quit = True  # trigger exit of program
    
    # --------------------------------------------------------------------------
    #  Create Widgets
    # --------------------------------------------------------------------------
    def __createWidgets(self):
        """Create the widgets. """
        if self.__is_verbose: print "INFO: Creating Widgets!"
        
        # create show preview button
        self.preview_button = tk.Button(self, text = "Show Camera Feed",
            command = self.clickStartPreview)
        self.preview_button.grid(row = 1, column = 0, 
            sticky = tk.W + tk.E + tk.N + tk.S)
        
        # create quit button
        self.quit_button = tk.Button(self, text = "Quit",
            command = self.clickQuit)
        self.quit_button.grid(row = 1, column = 1, 
            sticky = tk.W + tk.E + tk.N + tk.S)
    
    # --------------------------------------------------------------------------
    #   Load Image
    # --------------------------------------------------------------------------
    def loadImage(self, image_address, canvas, width, height):
        """
        Load image at image_address. If the load is successful then return True,
        otherwise return False.
        
        Keyword Arguments:
        image_address -- The address of the image to be loaded (default = './').
        canvas -- The Tkinter Canvas into which the image is loaded.
        width -- Width of the image to load.
        height -- Height of the image to load.
        
        Returns:
        Boolean -- True if load successful, False if not.
        
        """
        # clear the old canvas
        canvas.delete(tk.ALL)
        
        if self.__is_verbose:
            print "INFO: Tkinter Canvas cleared. Read to load new image. "
        
        try:
            # guard against incorrect argument datatypes
            if not isinstance(canvas, tk.Canvas): raise TypeError
            if not isinstance(image_address, str): raise TypeError
            if not isinstance(width, int): raise TypeError
            if not isinstance(height, int): raise TypeError
            
            # load the image into the canvas
            photo = ImageTk.PhotoImage(Image.open(image_address))
            canvas.create_image((width, height), image = photo)
            canvas.image = photo
            
            # image load successful
            return True
        
        except TypeError:
            # arguments of incorrect data type, load unsuccessful
            if self.__is_verbose: 
                print "ERROR: loadImage() arguments of incorrect data type."
            return False
        except:
            # image failed to load
            if self.__is_verbose: 
                print "ERROR: loadImage() failed to load image " + image_address
            return False
            
    
    # --------------------------------------------------------------------------
    #  Getter(s)
    # --------------------------------------------------------------------------
    # is verbose
    def getIsVerbose():
        """Retrun boolean whether application is verbose or not. """
        return self.__is_verbose
        


# ==============================================================================
#
#       Main Program Functions
#
# ==============================================================================
# ------------------------------------------------------------------------------
#  Create the Application
# ------------------------------------------------------------------------------
def create_application():
    """
    Create an instance of the MainApplication class defined in this module. 
    Set the GUI to run in its mainloop().
    
    """
    if s.IS_VERBOSE: print "INFO: create_application() called. "
    
    global app
    
    # create the TKinter application
    root = tk.Tk()
    app = MainApplication(master = root)
    app.master.title("PiPark 2014")
    app.mainloop()

# ------------------------------------------------------------------------------
#  Run PiPark
# ------------------------------------------------------------------------------
def run():
    """
    Run the main PiPark program. This function periodically captures a new image
    and then tests for changes in the parking space reference areas compared to
    the control points as set during the setup procedure (./pipark_setup.py).
    
    When a change has been detected for 3 ticks the server (to which the pi is
    registered) is updated to accordingly show whether the appropriate parking
    spaces are filled or empty.
    
    This function is run mainly as an infinite loop until the application
    is destroyed.
    
    """
    if s.IS_VERBOSE: print "INFO: run() called. "
    
     # --- Pre-loop Setup ------------------------------------------------------
    
    # variables
    global camera  # use global pi camera object!
    global occupancy
    global app
    
    image_location = "./images/pipark.jpeg"  # image save location
    loop_delay = s.PICTURE_DELAY  # duration between each loop in seconds
        
    # load data sets and count the number of spaces and control boxes
    space_boxes, control_boxes = __setup_box_data()
    num_spaces = len(space_boxes)
    num_controls = len(control_boxes)
    if s.IS_VERBOSE: print "INFO: #Spaces:", num_spaces, "\t#CPs:", num_controls
    
    # assert that the correct number of spaces and CPs are present in the data
    assert num_spaces > 0
    assert num_controls == 3
    
    # set initial values for status and ticks
    last_status = [None for i in range(10)]
    last_ticks = [3 for i in range(10)]
    
    
    while True:
        # --- Space and CP Average Calculation Phase ---------------------------
        
        # clear lists containing average colour values for spaces
        space_averages = []
        control_averages = []
        
        # capture new image & save to specified location
        camera.capture(image_location)
        print "INFO: New image saved to:", image_location

        try:
            # load image for processing
            image = imageread.Image.open(image_location)
            pixels = image.load()
        except:
            print "ERROR: The image has failed to load. Check camera setup. "
            sys.exit(1)

        # setup space dimensions and averages, and if verbose, print to terminal
        for space in space_boxes:
            space_x = space[2]
            space_y = space[3]
            space_w = abs(space[4] - space[2])
            space_h = abs(space[5] - space[3])
            
            if s.IS_VERBOSE: 
                print "INFO: Space", space[0], "dimensions:"
                print "      x:", space_x, "y:", space_y, "w:", space_w, "h:", space_h
            
            # append space average pixel to list of averages
            space_average = imageread.get_area_average(
                pixels, 
                space_x, 
                space_y, 
                space_w, 
                space_h
                )
            space_averages.append(space_average)
        
        
        if s.IS_VERBOSE: print ""  # line break

        # setup CP dimensions and averages and, if verbose, print to terminal
        for control in control_boxes:
            control_x = control[2]
            control_y = control[3]
            control_w = abs(control[4] - control[2])
            control_h = abs(control[5] - control[3])

            if s.IS_VERBOSE: 
                print "INFO: CP", control[0], "dimensions:"
                print "      x:", control_x, "y:", control_y, "w:", control_w, "h:", control_h
            
            # append control average pixel to list of averages
            control_average = imageread.get_area_average(
                pixels, 
                control_x, 
                control_y, 
                control_w, 
                control_h
                )
            control_averages.append(control_average)
            
            
        # --- Average Comparisons and Data Upload Phase ------------------------
        
        # average pixel values now calculated for all Control Points and Parking
        # Spaces. Now move on to comparison and upload phase.
        if s.IS_VERBOSE: print "\n\n"  # doubleline break
        
        # compare control points averages to parking spaces averages
        for i, space in zip(space_boxes, space_averages):
            
            # number of control points that conflict with parking space reading
            num_controls = 0
            
            print "INFO: Checking for differences...\n     ",
            # for each control point (3 in total) compare each parking space
            for control in control_averages:
                
                # make comparison
                if imageread.compare_area(space, control):
                    num_controls += 1
                    print "Y",
                else:
                    print "N",

            # determine if parking space is occupied. If at least two CPs agree
            # that the space is occupied, set the space to occupied.
            is_occupied = False
            if num_controls >= 2: is_occupied = True
            
            if s.IS_VERBOSE and is_occupied:
                print "=> Space", i[0], "is filled.\n"
            elif s.IS_VERBOSE and not is_occupied:
                print "=> Space", i[0], "is empty.\n"
            
            # update the server with most recent space values after 3 ticks
            if last_status[i[0]] != is_occupied:
                print "      Detected change in space", i[0]
                print "      Space", i[0], "has been", ("occupied" if is_occupied else "vacant"), "for", last_ticks[i[0]], "tick(s).\n"
                
                if last_ticks[i[0]] < 3:
                    last_ticks[i[0]] += 1
                else:
                    last_status[i[0]] = is_occupied
                    last_ticks[i[0]] = 1
                    print "      Space", i[0], "has changed status, sending update to server...\n"
                    num = 1 if is_occupied else 0
                    occupancy = last_status
                    
                    
                    sendoutput = senddata.send_update(i[0], num)
                    if "success" in sendoutput.keys():
                        print "      Success:", sendoutput["success"]
                    elif "error" in sendoutput.keys():
                        print "      Error:", sendoutput["error"]
                    print ''
            else:
                last_ticks[i[0]] = 1
                
        app.updateText()
        if s.IS_VERBOSE: print "INFO: Sleep for", loop_delay, "seconds... Zzz."
        imageread.time.sleep(loop_delay)


# -----------------------------------------------------------------------------
#  Main
# -----------------------------------------------------------------------------
def main():
    """Start PiPark application and Smart Parking System loop. """
    
    # use global variables (Oh D-d-d-dear)!
    global has_quit
    global camera
    
    # instantiate the camera object to global camera variable
    camera = imageread.setup_camera(is_fullscreen = False)
    
    # now create two threads, one in which to run the MainApplication and
    # the other the run the main program loop.
    
    try:
        thread.start_new_thread(create_application, ())
        thread.start_new_thread(run, ())
    except:
    	print "ERROR: Failed to start new thread. =("
        
    # do not end main thread until user has quit and destroyed the application
    while not has_quit:
    	pass

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
    
    

