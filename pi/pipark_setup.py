#!/usr/bin/env python
"""
Tkinter GUI for PiPark setup.

Allows the user to perform all setup tasks including: mark parking spaces, set
control points and register the car park with the server. The main PiPark
program can be invoked from the menu.

Author: Nicholas Sanders and Humphrey Shotton
Version: 2.0 [2014/03/20]

"""
import os
import Tkinter as tk
import tkMessageBox
from PIL import Image, ImageTk

import imageread
import main
import setup_selectarea as sa  # not currently used
import settings as s
from setup_classes2 import ParkingSpace, Boxes
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
    __is_verbose = True  # print messages to terminal
    __is_saved = False  # TODO: Implement is saved!
    
    # FIXME: Parking space implementation
    __parking_space = None
    __parking_spaces = None
    
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

        # run super constructor method
        tk.Frame.__init__(self, master)
        
        # set alignment inside the frame
        self.grid()
        
        # create widgets
        self.__createDisplay()  # display canvas: holds the image, CPs and spaces
        self.__createMenu()  # menu canvas: holds the buttons and menu bar image
        
        # create mouse button and key-press handlers -> set focus to this frame
        self.bind("<Return>", self.returnPressHandler)
        self.bind("<Key>", self.keyPressHandler)
        self.display.bind("<Button-1>", self.leftClickHandler)
        self.display.bind("<Button-3>", self.rightClickHandler)
        self.focus_set()
        
        # FIXME: parking space implementation
        self.__parking_space = ParkingSpace(1, self.display)
        self.__parking_spaces = Boxes(self.display)
        print "INFO: __parking_spaces length:", self.__parking_spaces.getLength()
        
        # load the default background
        self.loadImage(self.DEFAULT_IMAGE, self.display, 
            s.PICTURE_RESOLUTION[0]/2, s.PICTURE_RESOLUTION[1]/2)
    
    
# ==============================================================================
#
#  Public Application Methods
#
# ==============================================================================           
    # --------------------------------------------------------------------------
    #   Load Setup Image
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
            message = "Press the ENTER key to take a new setup image.")

        
        try:
            # initialise the camera using the settings in the imageread module
            self.__camera = imageread.setup_camera(is_fullscreen = False)
            self.__camera.start_preview()
            self.__camera_is_active = True
            if self.__is_verbose: print "INFO: PiCam activated."
        except:
            # camera failed to load, display error message
            tkMessageBox.showerror(title = "Error!",
                message = "Error: Failed to setup and start PiCam.")
    
    
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
        if not self.__camera_is_active or self.__camera: return
        
        try:
            # capture new setup image, then close the camera
            self.__camera.capture(self.SETUP_IMAGE)
            self.__camera.stop_preview()
            self.__camera.close()
            self.__camera_is_active = False
            
            if self.__is_verbose: 
                print "INFO: New setup image captured. 
                print "INFO: PiCam deactivated."
            
        except:
            # image failed to capture, show error message
            tkMessageBox.showerror(title = "Error!",
                message = "Error: Failed to capture new setup image.")
                
        # load the new setup image
        self.loadImage(self.SETUP_IMAGE, self.display,
            s.PICTURE_RESOLUTION[0]/2, s.PICTURE_RESOLUTION[1]/2)
        
        # activate buttons if they're disabled
        # TODO: add if statement. If self.cps_button.state == tk.DISABLED?
        self.cps_button.config(state = tk.ACTIVE)
        self.spaces_button.config(state = tk.ACTIVE)
    
    # --------------------------------------------------------------------------
    #   Key-press Event Handler
    # --------------------------------------------------------------------------
    def keyPressHandler(self, event):
        """Handle key-press events for numeric keys. """
        
        key = event.char
        NUM_KEYS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        
        if key in NUM_KEYS:
            if self.__is_verbose: print "INFO: Number-key pressed", key
            self.__parking_spaces.setCurrentBox(key)
    
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
            # TODO: Add CPs on click
        
        # add new parking space
        elif self.spaces_button.getIsActive():
            if self.__is_verbose: print "INFO: Add Parking Space"
            # TODO: Add multiple parking spaces, by number key-press event
            # TODO: Delete line v? Shrink line vv!
            #self.__parking_space.updatePoints(event.x, event.y)
            self.__parking_spaces.boxes[getCurrentBox()].updatePoints(event.x, event.y)
            
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
            # TODO: Remove CPs
        elif self.spaces_button.getIsActive():
            if self.__is_verbose: print "INFO: Remove parking space"
            # TODO: Remove Parking spaces
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
        # turn off toggle buttons
        self.spaces_button.setOff()
        self.cps_button.setOff()
        
        # if the user is positive, close the setup and run the main program
        response = tkMessageBox.askyesno(title = "Setup Complete",
            message = "Are you ready to leave setup and run PiPark?")
                
        if response:   
            self.quit_button.invoke()
            main.run_main()
    
    def clickRegister(self):
        """Register the car park with the server. """
        
        # turn off toggle buttons
        self.spaces_button.setOff()
        self.cps_button.setOff()
        
        if self.__is_verbose: print "ACTION: Clicked 'Register'"
        # TODO: Register carpark with the server as per CLI setup.
            
    
    def clickNewImage(self):
        """Use PiCam to take new 'setup image' for PiPark setup. """
        
        # turn off toggle buttons
        self.spaces_button.setOff()
        self.cps_button.setOff()
        
        # clear the current image in the GUI, then take a new image using the
        # PiCam, then load the new image into the GUI
        self.display.delete(tk.ALL)
        #TODO: self.__parking_spaces.clearAll()
        self.turnOnCamera()
    
    def clickSave(self):
        if self.__is_verbose: print "ACTION: Clicked Save'"
        # turn off toggle buttons
        self.spaces_button.setOff()
        self.cps_button.setOff()
    
    def clickLoad(self):
        if self.__is_verbose: print "ACTION: Clicked 'Load'"
        # turn off toggle buttons
        self.spaces_button.setOff()
        self.cps_button.setOff()
    
    def clickClear(self):
        if self.__is_verbose: print "ACTION: Clicked 'Clear'"
        # turn off toggle buttons
        self.spaces_button.setOff()
        self.cps_button.setOff()


    def clickSpaces(self):
        """Add/remove parking-space bounding boxes. """
        
        # toggle the button, and turn off other toggle buttons
        self.spaces_button.toggle()
        if self.cps_button.getIsActive(): self.cps_button.setOff()
        
        # TODO: add/remove spaces functionality! 
        # add spaces with two clicks (start & end corner points)?
        # removal of spaces whilst holding CTRL and click in box?

    def clickCPs(self):
        """Add/remove control points. """
        
        # toggle the button, and turn off other toggle buttons
        self.cps_button.toggle()
        if self.spaces_button.getIsActive(): self.spaces_button.setOff()
        
        # TODO: add/remove CPs functionality!
        # add CPs with single click?
        # removal of CPs whilst holding CTRL and click?
        
        
    def clickQuit(self):
        """Quit & terminate the application. """
        
        # turn off toggle buttons
        self.spaces_button.setOff()
        self.cps_button.setOff()
        
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
        
        # turn off toggle buttons
        self.spaces_button.setOff()
        self.cps_button.setOff()
        
        # load external README from command line
        # TODO: Put this in new Tkinter window with scroll bar
        os.system("leafpad " + "./SETUP_README.txt")
        
        
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