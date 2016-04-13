#!/usr/bin/env python
"""
Tkinter GUI for PiPark setup.

Allows the user to perform all setup tasks including: mark parking spaces, set
control points and register the car park with the server. The main PiPark
program can be invoked from the menu.

Author: Nicholas Sanders and Humphrey Shotton
Version: 2.1 [2014/03/26]

"""
import os
import Tkinter as tk
import tkMessageBox
from PIL import Image, ImageTk

import imageread
import main
import data.settings as s
from setup_classes import ParkingSpace, Boxes
from ToggleButton import ToggleButton

# ==============================================================================
#
#   Application Class
#
# ==============================================================================
class Application(tk.Frame):

    # --------------------------------------------------------------------------
    #   Instance Attributes
    # --------------------------------------------------------------------------
    
    # booleans
    __is_verbose = s.IS_VERBOSE  # print messages to terminal
    __is_saved = False
    
    # lists to hold parking space and control point references
    __parking_spaces = None
    __control_points = None
    
    # picamera
    __camera = None
    __camera_is_active = False
    
    # image load/save locoations
    SETUP_IMAGE = "./images/setup.jpeg"
    DEFAULT_IMAGE = "./images/default.jpeg"
    
    
    # --------------------------------------------------------------------------
    #   Constructor Method
    # --------------------------------------------------------------------------
    def __init__(self, master = None):
        """Application constructor method. """

        # run super constructor method
        tk.Frame.__init__(self, master)
        
        # set alignment inside the frame
        self.grid()
        
        # create widgets
        self.__createDisplay()  # display canvas: holds the image, CPs and spaces
        self.__createMenu()  # menu canvas: holds the buttons and menu bar image
        
        # lists to hold parking space and control point references
        self.__parking_spaces = Boxes(self.display, type = 0)
        self.__control_points = Boxes(self.display, type = 1)
        
        # create mouse button and key-press handlers -> set focus to this frame
        self.bind("<Return>", self.returnPressHandler)
        self.bind("<Key>", self.keyPressHandler)
        self.bind("<Escape>", self.escapePressHandler)
        self.display.bind("<Button-1>", self.leftClickHandler)
        self.display.bind("<Button-3>", self.rightClickHandler)
        self.focus_set()

        if self.__is_verbose:
            print "INFO: __parking_spaces length:", self.__parking_spaces.length()
            print "INFO: __control_points length:", self.__control_points.length()
        
        # load the default background
        self.loadImage(self.DEFAULT_IMAGE, self.display, 
            s.PICTURE_RESOLUTION[0]/2, s.PICTURE_RESOLUTION[1]/2)
    
    
# ==============================================================================
#
#  Public Application Methods
#
# ==============================================================================           
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
    #   Activate the Pi Camera
    # --------------------------------------------------------------------------
    def turnOnCamera(self):
        """
        Instruct the user how to take a new setup image, then activate 
        the PiCam. If the camera fails to load, catch the exception and present
        error message.

        """
        # show quick dialogue box with basic instruction
        tkMessageBox.showinfo(title = "",
            message = "Press the ENTER key to take a new setup image "
            + "or the ESCAPE key to cancel.")

        
        try:
            # initialise the camera using the settings in the imageread module
            self.__camera = imageread.setup_camera(is_fullscreen = True)
            self.__camera.awb_mode = 'auto';
            self.__camera.exposure_mode = 'auto';
            self.__camera.start_preview()
            self.__camera_is_active = True
            if self.__is_verbose: print "INFO: PiCam activated."
        except:
            # camera failed to load, display error message
            tkMessageBox.showerror(title = "Error!",
                message = "Error: Failed to setup and start PiCam.")
    
    # --------------------------------------------------------------------------
    #   Save Data
    # --------------------------------------------------------------------------
    def saveData(self):
        """Save the CP and parking space reference data to ./setup_data.py. """
        
        # Open the file to output the co-ordinates to
        f1 = open('./setup_data.py', 'w+')

        # Print the dictionary data to the file
        print >> f1, 'boxes = ['
        
        # for every parking space, save the data to ./setup_data.py
        for i in range(self.__parking_spaces.length()):
            space = self.__parking_spaces.get(i).getOutput()
            
            # ignore the space if no data present
            if space != None:
                o = (i)
                print >> f1, space, ','
        
        # for every control point, save the data to ./setup_data.py
        for j in range(self.__control_points.length()):
            cp = self.__control_points.get(j).getOutput()
            
            # ignore the CP if no data present
            if cp != None:
                o = (i)
                print >> f1, cp, ','
        
        # save to ./setup_data.py        
        print >> f1, ']'
        self.__is_saved = True
            
        if self.__is_verbose: print 'INFO: Data saved in file setup_data.py.'
        tkMessageBox.showinfo(title = "PiPark Setup", 
            message = "Data saved successfully.")
    
    # --------------------------------------------------------------------------
    #   Load Data
    # --------------------------------------------------------------------------        
    def loadData(self):
        try:
            # load the setup data, reload to refresh the data
            import setup_data 
            reload(setup_data)
        except:
            if self.__is_verbose: 
                print "ERROR: Problem loading data from ./setup_data.py"
            tkMessageBox.showerror(
                title = "Error!", 
                message = "Problem loading data from setup_data.py"
                )
        self.__is_saved = True
        return setup_data.boxes
        
    # --------------------------------------------------------------------------
    #   Check Data
    # --------------------------------------------------------------------------
    def checkData(self):
        """
        Check that the setup data meets the following criteria:
        
            1) There is at least 1 parking space.
            2) There are exactly 3 control points.
            
        Returns:
        Boolean -- True if criteria is met, False if not.
            
        """
        if self.__is_verbose: print "INFO: Data is being checked for validity."
        
        # get the boxes data to check from setup_data
        try:
            # load the setup data
            import setup_data
            reload(setup_data)
            
            # ensure that boxes exists and is not empty
            box_data = setup_data.boxes
            if not box_data: raise ValueError
            
        except ImportError:
            if self.__is_verbose: 
                print "ERROR: Problem loading data from ./setup_data.py"
        except ValueError:
            if self.__is_verbose:
                print "ERROR: ./setup_data.py 'boxes' is empty."
        except:
            if self.__is_verbose:
                print "ERROR: ./setup_data.py does not contain 'boxes'."
               
        # create lists to hold data of each type
        space_boxes = []
        control_boxes = []
        
        # append the box data to space or control list as appropriate
        for data_set in box_data:
            if data_set[1] == 0: 
                space_boxes.append(data_set)
            elif data_set[1] == 1: 
                control_boxes.append(data_set)
            elif self.__is_verbose:
                print "ERROR: Box-type not set to either 0 or 1."
        
        # data is valid if there is at least 1 space and exactly 3 control points
        if len(space_boxes) > 0 and len(control_boxes) == 3: 
            valid_data = True
        else:
            valid_data = False
        
        if self.__is_verbose: print "INFO: Data checked. Data is", valid_data
        return valid_data
                    
    # --------------------------------------------------------------------------
    #   Register Data
    # --------------------------------------------------------------------------
    def register(self):
        """Register the Pi with the server. """
        
        # if setup hasn't been saved recently since last change, ask the if 
        # user to save first
        if not self.__is_saved:
            response = tkMessageBox.askokcancel(title = "Save Setup",
                message = "Setup data must be saved before the registration"
                + " process can be completed. Would you like to save now?")
                
            # if user selects 'yes' save the data and continue, else do not 
            # register the pi
            if response: 
                self.saveData()
            else:
                tkMessageBox.showinfo(title = "PiPark Setup",
                    message = "Registration not completed.")
                return
                
        # check that most recent saved data is valid (#CPs == 3, #Spaces > 0)
        if not self.checkData():

            # data invalid, so display message and return
            tkMessageBox.showinfo(
                title = "PiPark Setup",
                message = "Registration not complete.\n\nSaved data is "
                + "invalid. Please ensure that there are 3 control points and "
                + "at least 1 parking spaces marked."
                )
            return
                
        # attempt to import the setup data and ensure 'boxes' is a list
        try:
            import setup_data
            reload(setup_data)
            boxes = setup_data.boxes
            if not isinstance(boxes, list): raise ValueError()
        except:
            print "ERROR: Setup data does not exist. Please run options 1 and 2 first."
            return
            
        # attempt to import the server senddata module
        try:
            import senddata
        except:
            print "ERROR: Could not import send data file."
            return
        

        # deregister all areas associated with this pi (start fresh)
        out = senddata.deregister_pi()
        
        try:
            out['error']
            print "ERROR: Error in connecting to server. Please update settings.py."
            return
        except:
            pass
        
        # register each box on the server
        for box in boxes:
            if box[1] == 0:
                output = senddata.register_area(box[0])
                if "error" in output.keys():
                    if self.__is_verbose: print "ERROR:", output["error"]
                    return
                else:
                    if self.__is_verbose:
                        print "INFO: Registering area", box[0], "on server."
         
        # print success message if verbose        
        if self.__is_verbose: print "\nINFO: Server registration successful."
        
        
# ==============================================================================
#
#  Event Handlers
#
# ==============================================================================
    # --------------------------------------------------------------------------
    #   Return-key-press Event Handler
    # --------------------------------------------------------------------------
    def returnPressHandler(self, event):
        """
        Handle Return-key-press events. Capture a new setup image when PiCam
        is active, and load the image.
        
        """
        # ensure focus on window
        self.focus_set()
        
        # do nothing if camera is not active, or no camera object exists
        if not self.__camera_is_active or not self.__camera: return
        
        try:
            # capture new setup image, then close the camera
            self.__camera.capture(self.SETUP_IMAGE)
            self.__camera.stop_preview()
            self.__camera.close()
            self.__camera_is_active = False
            
            if self.__is_verbose: 
                print "INFO: New setup image captured." 
                print "INFO: PiCam deactivated."
            
        except:
            # image failed to capture, show error message
            tkMessageBox.showerror(title = "Error!",
                message = "Error: Failed to capture new setup image.")
                
        # load the new setup image
        self.loadImage(self.SETUP_IMAGE, self.display,
            s.PICTURE_RESOLUTION[0]/2, s.PICTURE_RESOLUTION[1]/2)
        
        # activate buttons if they're disabled
        self.cps_button.config(state = tk.ACTIVE)
        self.spaces_button.config(state = tk.ACTIVE)
    
    # --------------------------------------------------------------------------
    #   Escape-key-press Event Handler
    # --------------------------------------------------------------------------
    def escapePressHandler(self, event):
        # ensure focus on window
        self.focus_set()
        
        # do nothing if camera is not active, or no camera object exists
        if not self.__camera_is_active or not self.__camera: return
        
        try:
            # close the camera without taking new image
            self.__camera.stop_preview()
            self.__camera.close()
            self.__camera_is_active = False
            
            if self.__is_verbose: 
                print "INFO: PiCam deactivated."
            
        except:
            # image failed to close for some reason, show error message
            if self.__is_verbose:
                print "ERROR: PiCam failed to close correctly."
    
    # --------------------------------------------------------------------------
    #   Key-press Event Handler
    # --------------------------------------------------------------------------
    def keyPressHandler(self, event):
        """Handle key-press events for numeric keys. """
        
        key = event.char
        NUM_KEYS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        
        if key in NUM_KEYS:
            if self.__is_verbose: print "INFO: Number-key pressed", key
            
            if self.spaces_button.getIsActive():
                self.__parking_spaces.setCurrentBox(int(key))
                
            if self.cps_button.getIsActive():
                # ignore all other numbers, but 1, 2 and 3 as 3 is the maximum
                # number of control points allowed.
                if key not in ['1', '2', '3']: return
                
                # NB: -1 from key press, because list indices are [0, 1, 2],
                # but for ease of user selection the numbers 1, 2, 3 are used 
                # for input
                self.__control_points.setCurrentBox(int(key) - 1)
    
    # --------------------------------------------------------------------------
    #   LMB Event Handler
    # --------------------------------------------------------------------------
    def leftClickHandler(self, event):
        """Handle LMB-click events to add/remove control points & spaces. """
        
        # ensure focus on display canvas to recieve mouse clicks
        self.display.focus_set()
        
        # perform correct operation, dependent on which toggle button is active
        
        # add new control points (max = 3)
        if self.cps_button.getIsActive():
            if self.__is_verbose: print "INFO: Add Control Point"
            self.__is_saved = False
            
            this_cp_id = self.__control_points.getCurrentBox()
            this_cp = self.__control_points.boxes[this_cp_id]
            this_cp.updatePoints(event.x, event.y)
        
        # add new parking space
        elif self.spaces_button.getIsActive():
            if self.__is_verbose: print "INFO: Add Parking Space"
            self.__is_saved = False
            
            this_space_id = self.__parking_spaces.getCurrentBox()
            this_space = self.__parking_spaces.boxes[this_space_id]
            this_space.updatePoints(event.x, event.y)
            
        # do nothing -- ignore LMB clicks
        else:
            if self.__is_verbose: print "INFO: Just clicking LMB merrily =D"

        # return focus to the main frame for key-press events
        self.focus_set()
        
    # --------------------------------------------------------------------------
    #   RMB Event Handler
    # --------------------------------------------------------------------------
    def rightClickHandler(self, event):
        """Handle RMB-click events to add/remove control points & spaces. """
        
        # ensure focus is set to the display canvas
        self.display.focus_set()
        
        # perform correct operation, dependent on which toggle button is active
        if self.cps_button.getIsActive():
            if self.__is_verbose: print "INFO: Remove Control Point"
            self.__is_saved = False
            
            self.__control_points.boxes[self.__control_points.getCurrentBox()].clear()
            self.__control_points.boxes[self.__control_points.getCurrentBox()].deleteRectangle(self.display)
            
        elif self.spaces_button.getIsActive():
            if self.__is_verbose: print "INFO: Remove parking space"
            self.__is_saved = False
            
            self.__parking_spaces.boxes[self.__parking_spaces.getCurrentBox()].clear()
            self.__parking_spaces.boxes[self.__parking_spaces.getCurrentBox()].deleteRectangle(self.display)
            
        else:
            if self.__is_verbose: print "INFO: Just clicking RMB merrily =)"
        
        # return focus to the main frame for key-press events
        self.focus_set()


# ==============================================================================
#
#  Button Handlers
#
# ==============================================================================
    def clickStart(self):
        """
        Close the current setup application, then initiate the main
        PiPark program.

        """
        if self.__is_verbose: print "ACTION: Clicked 'Start'"
        
        # turn off toggle buttons
        self.spaces_button.setOff()
        self.cps_button.setOff()
        
        # set initial responses
        response = False
        response1 = False
        response2 = False
        
        # if setup data has not been saved. Ask user if they would like to save
        # before continuing.
        if not self.__is_saved:
            response = tkMessageBox.askyesno(
                title = "Save Setup",
                type = tkMessageBox.YESNOCANCEL,
                message = "Most recent changes to setup have not been saved."
                + "Would you like to save before running PiPark?"
                )
            if response: self.saveData()
            
        # data is saved, ask the user if they are sure they wish to quit.
        else:
            response = tkMessageBox.askyesno(
                title = "Save Setup",
                message = "Are you ready to leave setup and run PiPark?"
                )
        
        # user wishes to quit setup and run pipark, so do it!
        if response:
            # ensure data is valid before continuing
            if not self.checkData():

                # data invalid, so display message and return
                tkMessageBox.showinfo(
                    title = "PiPark Setup",
                    message = "Saved data is invalid. Please ensure that "
                    + "there are 3 control points and at least 1 parking "
                    + "space marked."
                    )
                return
                    
            self.quit_button.invoke()
            if self.__is_verbose: print "INFO: Setup application terminated. "
            main.main()
    
    def clickRegister(self):
        """Register the car park with the server. """
        if self.__is_verbose: print "ACTION: Clicked 'Register'"
        
        # turn off toggle buttons
        self.spaces_button.setOff()
        self.cps_button.setOff()
        
        self.register()
            
    
    def clickNewImage(self):
        """Use PiCam to take new 'setup image' for PiPark setup. """
        if self.__is_verbose: print "ACTION: Clicked 'Capture New Image'"
        self.__is_saved = False
        
        # turn off toggle buttons
        self.spaces_button.setOff()
        self.cps_button.setOff()
        
        # clear the Tkinter display canvas, and all related setupdata. Then
        # turn on PiCam to allow for new image to be taken.
        self.__parking_spaces.clearAll(self.display)
        self.__control_points.clearAll(self.display)
        self.turnOnCamera()
    
    def clickSave(self):
        if self.__is_verbose: print "ACTION: Clicked Save'"
        
        # turn off toggle buttons
        self.spaces_button.setOff()
        self.cps_button.setOff()

        self.saveData()
    
    def clickLoad(self):
        if self.__is_verbose: print "ACTION: Clicked 'Load'"
        
        # turn off toggle buttons
        self.spaces_button.setOff()
        self.cps_button.setOff()
        
        if not self.loadImage(self.SETUP_IMAGE, self.display, 
                s.PICTURE_RESOLUTION[0]/2, s.PICTURE_RESOLUTION[1]/2):
                
                tkMessageBox.showerror(title = "Error!",
                message = "Error loading setup image."
                + " Please ensure setup image exists as ./image/setup_image.jpeg.")
                
                return
        
        # clear all previous data, and activate buttons
        self.clear_button.invoke()
        self.cps_button.config(state = tk.ACTIVE)
        self.spaces_button.config(state = tk.ACTIVE)
    
    def clickClear(self):
        if self.__is_verbose: print "ACTION: Clicked 'Clear'"
        self.__is_saved = False
        
        # clear all data points, to start afresh
        self.__parking_spaces.clearAll(self.display)
        self.__control_points.clearAll(self.display)


    def clickSpaces(self):
        """Add/remove parking-space bounding boxes. """
        if self.__is_verbose: print "ACTION: Clicked 'Add/Remove Spaces'"
        
        # toggle the button, and turn off other toggle buttons
        self.spaces_button.toggle()
        if self.cps_button.getIsActive(): self.cps_button.setOff()

    def clickCPs(self):
        """Add/remove control points. """
        if self.__is_verbose: print "ACTION: Clicked 'Add/Remove CPs'"
        
        # toggle the button, and turn off other toggle buttons
        self.cps_button.toggle()
        if self.spaces_button.getIsActive(): self.spaces_button.setOff()
        
        
    def clickQuit(self):
        """Quit & terminate the application. """
        if self.__is_verbose: print "ACTION: Clicked 'Quit'"
        
        # turn off toggle buttons
        self.spaces_button.setOff()
        self.cps_button.setOff()
        
        response = True
        # if the user hasn't recently saved, ask if they really wish to quit
        if not self.__is_saved: 
            response = tkMessageBox.askyesno(
                title = "Quit?",
                message = "Are you sure you wish to quit?"
                + "All unsaved setup will be lost."
                )
            
        if response:
            # user wishes to quit, destroy the application
            self.quit()
            self.master.destroy()
    
    
    def clickAbout(self):
        """Open the README file for instructions on GUI use. """
        if self.__is_verbose: print "ACTION: Clicked 'Open README'"
        
        # turn off toggle buttons
        self.spaces_button.setOff()
        self.cps_button.setOff()
        
        # load external README from command line
        # TODO: Put this in new Tkinter window with scroll bar
        os.system("leafpad " + "./SETUP_README.txt")
        if self.__is_verbose: print "INFO: Opened ./SETUP_README.txt in leafpad."
        
        
# ==============================================================================
#
#  Application Layout Management
#
# ==============================================================================  
    # --------------------------------------------------------------------------
    #   Create Image Display Canvas
    # --------------------------------------------------------------------------
    def __createDisplay(self):
        """
        Create the display tkinter canvas to hold the images taken by the
        pi camera.
        
        """
        
        self.display = tk.Canvas(
            self, 
            width = s.PICTURE_RESOLUTION[0],
            height = s.PICTURE_RESOLUTION[1]
            )
        self.display.grid(row = 2, column = 0, rowspan = 1, columnspan = 6)


    # --------------------------------------------------------------------------
    #   Create Options Menu
    # --------------------------------------------------------------------------
    def __createMenu(self):
        """Create a tkinter canvas in which to hold the menu buttons. """
        
        # Layout:
        # -------
        #  ------------------------------------------------------------------
        # |   Start  ||   Capture New Image   || Add/Remove Spaces ||  Quit  |
        #  ------------------------------------------------------------------
        # | Register || Save || Load || Clear ||  Add/Remove CPs   || ReadMe |
        #  ------------------------------------------------------------------
        
        # padding around buttons
        PADDING = 10;
        
        # start the main program
        self.start_button = tk.Button(self, text = "Start PiPark",
            command = self.clickStart, padx = PADDING)
        self.start_button.grid(row = 0, column = 0,
            sticky = tk.W + tk.E + tk.N + tk.S)
        
        # register the car park button
        self.register_button = tk.Button(self, text = "Register",
            command = self.clickRegister, padx = PADDING)
        self.register_button.grid(row = 1, column = 0,
            sticky = tk.W + tk.E + tk.N + tk.S)
        
        
        # take new setup image button
        self.image_button = tk.Button(self, text = "Capture New Setup Image",
            command = self.clickNewImage, padx = PADDING)
        self.image_button.grid(row = 0, column = 1, rowspan = 1, columnspan = 3,
            sticky = tk.W + tk.E + tk.N + tk.S)
        
        # save setup data & image
        self.save_button = tk.Button(self, text = "Save",
            command = self.clickSave, padx = PADDING)
        self.save_button.grid(row = 1, column = 1,
            sticky = tk.W + tk.E + tk.N + tk.S)
        
        # load setup data & image
        self.load_button = tk.Button(self, text = "Load",
            command = self.clickLoad, padx = PADDING)
        self.load_button.grid(row = 1, column = 2,
            sticky = tk.W + tk.E + tk.N + tk.S)
        
        # clear all parking spaces and CPs
        self.clear_button = tk.Button(self, text = "Clear",
            command = self.clickClear, padx = PADDING)
        self.clear_button.grid(row = 1, column = 3,
            sticky = tk.W + tk.E + tk.N + tk.S)
        
        
        # add/remove spaces button
        self.spaces_button = ToggleButton(self)
        self.spaces_button.config(text = "Add/Remove Spaces",
            command = self.clickSpaces, padx = PADDING, state = tk.DISABLED)
        self.spaces_button.grid(row = 0, column = 4,
            sticky = tk.W + tk.E + tk.N + tk.S)

        # add/remove control points button
        self.cps_button = ToggleButton(self)
        self.cps_button.config(text = "Add/Remove Control Points",
            command = self.clickCPs, padx = PADDING, state = tk.DISABLED)
        self.cps_button.grid(row = 1, column = 4,
            sticky = tk.W + tk.E + tk.N + tk.S)
        
        
        # quit setup
        self.quit_button = tk.Button(self, text = "Quit",
            command = self.clickQuit, padx = PADDING)
        self.quit_button.grid(row = 0, column = 5,
            sticky = tk.W + tk.E + tk.N + tk.S)
        
        # about button - display information about PiPark
        self.about_button = tk.Button(self, text = "Open ReadMe",
            command = self.clickAbout, padx = PADDING)
        self.about_button.grid(row = 1, column = 5,
            sticky = tk.W + tk.E + tk.N + tk.S)


# ==============================================================================
#
#   Getters and Setters
#
# ==============================================================================  
    # --------------------------------------------------------------------------
    #   Is Verbose?
    # --------------------------------------------------------------------------
    def getIsVerbose():
        return self.__is_verbose
    
    def setIsVerbose(value):
        if isinstance(value, bool): self.__is_verbose = value


# ==============================================================================
#
#   Run Main Program
#
# ==============================================================================  
if __name__ == "__main__":

    root = tk.Tk()
    app = Application(master = root)
    app.master.title("PiPark Setup")
    app.mainloop()
