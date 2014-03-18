#!/usr/bin/env python
"""
Tkinter GUI for PiPark setup.

Allows the user to perform all setup tasks including: mark parking spaces, set
control points and register the car park with the server. The main PiPark
program can be invoked from the menu.

Author: Nicholas Sanders
Version: 0.1 [2014/03/17]

"""
import os
import Tkinter as tk
import tkMessageBox
from PIL import Image, ImageTk

import imageread
import main
import setup_selectarea as ssa
import settings as s

# ==============================================================================
#
#   Application Class
#
# ==============================================================================
class Application(tk.Frame):

    # --------------------------------------------------------------------------
    #   Instance Attributes
    # --------------------------------------------------------------------------
    
    # print messages to the terminal?
    __is_verbose = False
    __is_saved = False  # TODO: Implement is saved!
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
        self.createDisplay()
        self.createMenu()
        
        self.display.bind("<Return>", clickReturnHangler)
            
        # if setup image exists then load it, otherwise load the default image
        if not self.loadImage(self.SETUP_IMAGE, self.display):
            self.loadImage(self.DEFAULT_IMAGE, self.display)
        
    def clickReturnHandler(self, event):
        self.display.focus_set()
        
        if __camera_is_active and __camera:
            __camera.capture(self.SETUP_IMAGE)
            __camera.stop_preview()
            __camera.close()
            __camera_is_active = False
            
            
    # --------------------------------------------------------------------------
    #   Load Setup Image
    # --------------------------------------------------------------------------
    def loadImage(self, image_address = None, canvas = None):
        """
        Load image at image_address. If the load is successful then return True,
        otherwise return False.
        
        Keyword Arguments:
        image_address -- The address of the image to be loaded (default = './').
        canvas -- The Tkinter Canvas into which the image is loaded.
        
        Returns:
        Boolean -- True if load successful, False if not.
        
        """
        
        try:
            # guard against incorrect datatypes
            if not isinstance(canvas, tk.Canvas): raise TypeError
            if not isinstance(image_address, str): raise TypeError
            
            # load the image into the canvas
            photo = ImageTk.PhotoImage(Image.open(image_address))
            canvas.create_image(
                (s.PICTURE_RESOLUTION[0]/2, s.PICTURE_RESOLUTION[1]/2),
                image = photo
            )
            canvas.image = photo
            
            return True
        
        except TypeError:
            # arguments of incorrect data type
            if self.__is_verbose: 
                print "ERROR: loadImage() arguments of incorrect data type."
            return False
        except:
            # image failed to load
            if self.__is_verbose: 
                print "ERROR: loadImage() failed to load image " + image_address
            return False
        
        
    # --------------------------------------------------------------------------
    #   Take New Setup Image
    # --------------------------------------------------------------------------
    def newSetupImage(self):
        """
        Instruct the user to take a new setup image. Then save the image
        to the specified location 'SETUP_IMAGE_ADDRESS', and finally load the
        new image into the GUI.

        """
        # show quick dialogue box with basic instruction
        tkMessageBox.showinfo(title = "",
            message = "Press the ENTER key to take a new setup image.")

        # initialise the camera using the settings in the imageread module
        try:
            __camera = imageread.setup_camera(is_fullscreen = False)
            __camera.start_preview()
            __camera_is_active = True
        except:
            tkMessageBox.showerror(title = "Error!",
                message = "Error: Failed to setup and start PiCam.")
        
        # capture and save a new setup image when the ENTER key is pressed
        # FIXME: Ensure focus isn't lost when camera is initialised. 
        #        Try implementing entirely into key <Return> event.
        #self.display.focus_set()
        #raw_input()
        #camera.capture(self.SETUP_IMAGE)
        
        # end the preview and close the camera.
        #camera.stop_preview()
        #camera.close()

    
    # --------------------------------------------------------------------------
    #   Button Handlers
    # --------------------------------------------------------------------------
    def clickQuit(self):
        """Quit & terminate the application. """
        
        # if the user hasn't recently saved, ask if they really wish to quit
        if not __is_saved: 
            response = tkMessageBox.askyesno(title = "Quit?",
                message = "Are you sure you wish to quit?"
                + " All unsaved setup will be lost.")
            
        if response:
            self.quit()
            self.master.destroy()

    def clickSpaces(self):
        """Add/remove parking-space bounding boxes. """
        
        print "ACTION: Clicked 'Add/Remove Spaces'"
        __is_saved = False
        # add spaces with two clicks (start & end corner points)
        # removal of spaces whilst holding CTRL and click in box

    def clickCPs(self):
        """Add/remove control points. """
        
        print "ACTION: Clicked 'Add/Remove Control Points'"
        __is_saved = False
        # add CPs with single click
        # removal of CPs whilst holding CTRL and click

    def clickRegister(self):
        """Register the car park with the server. """
        
        print("ACTION: Clicked 'Register'")
        # register with the server as per CLI setup

    def clickNewImage(self):
        """Use PiCam to take new 'setup image' for PiPark setup. """
        
        # clear the current image in the GUI, then take a new image using the
        # PiCam, then load the new image into the GUI
        self.display.delete(tk.ALL)
        self.newSetupImage()
        self.loadImage(self.SETUP_IMAGE, self.display)

    def clickStart(self):
        """
        Close the current setup application, then initiate the main
        PiPark program.

        """
        # if the user is positive, close the setup and run the main program
        response = tkMessageBox.askyesno(title = "Setup Complete",
            message = "Are you ready to leave setup and run PiPark?")
                
        if response:   
            self.quit_button.invoke()
            main.run_main()
            

    def clickAbout(self):
        """Open the README file for instructions on GUI use. """
        
        # load external README from command line
        os.system("leafpad " + "./SETUP_README.txt")
        

    # --------------------------------------------------------------------------
    #   Create Image Display Canvas
    # --------------------------------------------------------------------------
    def createDisplay(self):
        self.display = tk.Canvas(
            self, 
            width = s.PICTURE_RESOLUTION[0],
            height = s.PICTURE_RESOLUTION[1]
        )
        self.display.grid(row = 1, column = 0, columnspan = 7)


    # --------------------------------------------------------------------------
    #   Create Options Menu
    # --------------------------------------------------------------------------
    def createMenu(self):
        PADDING = 10;

        # draw a background for the menu on a new canvas
        
        self.bg = tk.Canvas(self, width = 960, height = 40)
        self.bg.grid(row = 0, column = 0, columnspan = 7)
        self.bg.create_rectangle(0, 0, 960, 50, fill = "grey")
        
        # about button - display information about PiPark
        self.about_button = tk.Button(self, text = "Open README",
            command = self.clickAbout, padx = PADDING)
        self.about_button.grid(row = 0, column = 5)

        # add/remove spaces button
        self.spaces_button = tk.Button(self, text = "Add/Remove Spaces",
            command = self.clickSpaces, padx = PADDING)
        self.spaces_button.grid(row = 0, column = 3)

        # add/remove control points button
        self.cps_button = tk.Button(self, text = "Add/Remove Control Points",
            command = self.clickCPs, padx = PADDING)
        self.cps_button.grid(row = 0, column = 4)

        # take new setup image button
        self.image_button = tk.Button(self, text = "Take New Setup Image",
            command = self.clickNewImage, padx = PADDING)
        self.image_button.grid(row = 0, column = 1)

        # register the car park button
        self.register_button = tk.Button(self, text = "Register",
            command = self.clickRegister, padx = PADDING)
        self.register_button.grid(row = 0, column = 2)

        # start the main program
        self.start_button = tk.Button(self, text = "Start PiPark",
            command = self.clickStart, padx = PADDING)
        self.start_button.grid(row = 0, column = 0)

        # quit setup
        self.quit_button = tk.Button(self, text = "Quit",
            command = self.clickQuit, padx = PADDING)
        self.quit_button.grid(row = 0, column = 6)


    # --------------------------------------------------------------------------
    #   Get/Set Is Verbose?
    # --------------------------------------------------------------------------
    def getIsVerbose():
        return self.__is_verbose
    
    def setIsVerbose(value):
        if isinstance(value, bool): __is_verbose = value


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