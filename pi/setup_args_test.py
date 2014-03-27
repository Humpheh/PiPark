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
import settings as s
import Tkinter as tk

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
    __is_verbose = False  # print messages to terminal
    __is_saved = False
    
    
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
        self.__createMenu()  # menu canvas: holds the buttons and menu bar image
    

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

        self.inputs = [['Wakeup Delay', 'text', s.WAKEUP_DELAY, 'WAKEUP_DELAY'],
                 ['Picture Delay', 'text', s.PICTURE_DELAY,'PICTURE_DELAY'],
                 ['Picture Resolution W', 'text', s.PICTURE_RESOLUTION[0], 'PICTURE_RESOLUTION[0]'],
                 ['Picture Resolution H', 'text', s.PICTURE_RESOLUTION[1], 'PICTURE_RESOLUTION[1]'],
                 ['Camera Window X', 'text', s.CAMERA_WINDOW_SIZE[0], 'CAMERA_WINDOW_SIZE[0]'],
                 ['Camera Window Y', 'text', s.CAMERA_WINDOW_SIZE[1], 'CAMERA_WINDOW_SIZE[1]'],
                 ['Camera Window W', 'text', s.CAMERA_WINDOW_SIZE[2], 'CAMERA_WINDOW_SIZE[2]'],
                 ['Camera Window H', 'text', s.CAMERA_WINDOW_SIZE[3], 'CAMERA_WINDOW_SIZE[3]'],
                 ['Max Pictures', 'text', s.MAX_PICTURES, 'MAX_PICTURES'],
                 ['Image Threshold', 'text', s.IMAGE_THRESHOLD, 'IMAGE_THRESHOLD'],
                 ['Window Width', 'text', s.WINDOW_WIDTH, 'WINDOW_WIDTH'],
                 ['Window Height', 'text', s.WINDOW_HEIGHT, 'WINDOW_HEIGHT'],
                 ['Is Verbose?', 'check', s.IS_VERBOSE, 'IS_VERBOSE'],
                 ['Park ID', 'text', s.PARK_ID, 'PARK_ID'],
                 ['Server Password', 'text', s.SERVER_PASS, 'SERVER_PASS'],
                 ['Server URL', 'text', s.SERVER_URL, 'SERVER_URL']]

        self.options = [[] for i in range(len(self.inputs))]

        for i in range(0, len(self.options)):
            self.options[i] = [0, 0, 0]
            
            self.options[i][0] = tk.Label(self, text = self.inputs[i][0],
                                        padx = PADDING)
            self.options[i][0].grid(row = i, column = 1,
                sticky = tk.W + tk.E + tk.N + tk.S)

            if self.inputs[i][1] == 'text':
                self.options[i][2] = tk.StringVar()
                self.options[i][1] = tk.Entry(self, width = 20,
                                             textvariable=self.options[i][2])
                self.options[i][2].set(self.inputs[i][2])
                
            elif self.inputs[i][1] == 'check':
                self.options[i][2] = tk.IntVar()
                self.options[i][1] = tk.Checkbutton(self, variable=self.options[i][2])
                self.options[i][2].set(1 if self.inputs[i][2] else 0)
                
            self.options[i][1].grid(row = i, column = 2,
                sticky = tk.W + tk.E + tk.N + tk.S)

        self.save_button = tk.Button(self, text = "Save Settings",
            command = self.save, padx = PADDING, pady = PADDING)
        self.save_button.grid(row = len(self.options), column = 1,
            sticky = tk.W + tk.E + tk.N + tk.S, columnspan = 2)
        
    def save(self):
        for i in range(len(self.inputs)):
            option = self.inputs[i]
            if option[1] == 'text':
                print option[3], '=', self.options[i][1].get() 
        
        return True
        
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
