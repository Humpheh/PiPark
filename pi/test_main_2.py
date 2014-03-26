"""
Authors: Nicholas Sanders & Humphrey Shotton
Filename: test_main_2.py
Version: 1.0 [2014/03/26]

Test main application

"""

import Tkinter as tk
import tkMessageBox
import imageread
    
# ==============================================================================
#
#       Tkinter Application
#
# ==============================================================================
class MainApplication(tk.Frame):
    
    # output messages to the terminal?
    __is_verbose = False
    
    # pi camera
    __camera = None
    __preview_is_active = False
    
    def __init__(self, master = None):
        """Application constructor method. """

        # run super constructor method
        tk.Frame.__init__(self, master, camera)
        
        self.__camera = camera
        
        # populate the application
        self.createWidgets()
        
        # create key-press handlers -> set focus to this frame
        self.bind("<Escape>", self.escapePressHandler)
        self.focus_set()
        
        # run the test app
        self.run()
        
    def escapePressHandler(self, event):
        
        # if the camera is previewing -> stop the preview
        if self.__camera and self.__preview_is_active:
            self.__camera.stop_preview()
            self.__preview_is_active = False
            self.set_focus()
    
    def clickStartPreview(self):
        
        # turn on the camera preview
        if self.__camera and not self.__preview_is_active:
            
            tkMessagebox.showinfo(
                title = "Show Camera Feed",
                message = "Press the ESCAPE key to exit preview mode"
                )
            
            self.__camera.start_preview()
            self.__preview_is_active = True
            self.set_focut()
    
    def clickQuit(self):
        self.quit()
        self.master.destroy()
    
    def createWidgets(self):
        
        # create show preview button
        self.preview_button = tk.Button(title = "Show Camera Feed",
            command = self.clickStartPreview)
        
        # create quit button
        self.quit_button = tk.Button(title = "Quit",
            command = self.clickQuit)
            
            
    # get/set __is_verbose
    def setIsVerbose(value):
        if isinstance(value, bool): self.__is_verbose = value
        
    def getIsVerbose():
        return self.__is_verbose
        
    def run(self):
        
        # >>>>>>>>>>
        # Replace main() code from here!!
        # <<<<<<<<<<
        
        while True:
            camera.capture(image_location)
            print "INFO: New image captured."
    
            print "INFO: Going to sleep for 5 seconds"
            imageread.time.sleep(5)
        

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
    camera = imageread.setup_camera(is_fullscreen = True)
    image_location = "./images/testimage.jpeg"
    
    # create the application
    root = tk.Tk()
    app = Application(master = root, camera = camera)
    app.master.title("PiPark 2014")
    app.mainloop()

        
# -----------------------------------------------------------------------------
#  Run Program
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
