"""
Authors: Nicholas Sanders & Humphrey Shotton
Filename: test_main_2.py
Version: 1.0 [2014/03/26]

Test main application

"""

import Tkinter as tk
import tkMessageBox
import imageread
import thread
import time

camera = imageread.setup_camera(is_fullscreen = False)

# ==============================================================================
#
#       Tkinter Application
#
# ==============================================================================
class MainApplication(tk.Frame):
    
    # output messages to the terminal?
    __is_verbose = True
    
    # pi camera
    __camera = None
    __preview_is_active = False
    
    def __init__(self, master = None, camera = None):
        """Application constructor method. """
        print "INFO: Constructor called."

        # run super constructor method
        tk.Frame.__init__(self, master)

        self.grid()
        
        self.__camera = camera
        
        # populate the application
        self.createWidgets()
        
        # create key-press handlers -> set focus to this frame
        self.bind("<Escape>", self.escapePressHandler)
        self.focus_set()
        
        # run the test app
        #thread.start_new_thread(self.run(), ())
        
    def escapePressHandler(self, event):
        if self.__is_verbose: print "ACTION: Escape key pressed."
        
        # if the camera is previewing -> stop the preview
        if self.__camera and self.__preview_is_active:
            self.__camera.stop_preview()
            self.__preview_is_active = False
            self.focus_set()
    
    def clickStartPreview(self):
        
        # turn on the camera preview
        if self.__camera and not self.__preview_is_active:
            
            tkMessageBox.showinfo(
                title = "Show Camera Feed",
                message = "Press the ESCAPE key to exit preview mode"
                )
            
            self.__camera.start_preview()
            self.__preview_is_active = True
            self.focus_set()
    
    def clickQuit(self):
        self.quit()
        self.master.destroy()
    
    def createWidgets(self):
        if self.__is_verbose: print "INFO: Creating Widgets!"
        
        # create show preview button
        self.preview_button = tk.Button(self, text = "Show Camera Feed",
            command = self.clickStartPreview)
        self.preview_button.grid()
        
        # create quit button
        self.quit_button = tk.Button(self, text = "Quit",
            command = self.clickQuit)
        self.quit_button.grid()
            
            
    # get __is_verbose
    def getIsVerbose():
        return self.__is_verbose
        
    def run(self):
        
        # >>>>>>>>>>
        # Replace main() code from here!!
        # <<<<<<<<<<

        # image save location
        image_location = "./images/testimage.jpeg"
        
        while True:
            self.__camera.capture(image_location)
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
    
    import imageread
    print "INFO: main()"
    # setup camera
    global camera
    #camera = imageread.setup_camera(is_fullscreen = False)
    
    # create the application
    root = tk.Tk()
    app = MainApplication(master = root, camera = camera)
    app.master.title("PiPark 2014")
    app.mainloop()

def run():
        
    # >>>>>>>>>>
    # Replace main() code from here!!
    # <<<<<<<<<<
    import imageread
    print "INFO: run()"
    global camera
    
    # image save location
    image_location = "./images/testimage.jpeg"
        
    while True:
        camera.capture(image_location)
        print "INFO: New image captured."
    
        print "INFO: Going to sleep for 5 seconds"
        imageread.time.sleep(5)
             
# -----------------------------------------------------------------------------
#  Run Program
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    
    time.sleep(3)
    
    try:
        thread.start_new_thread(main, ())
        thread.start_new_thread(run, ())
    except:
    	print "ERROR: Failed to start new thread"
    while True:
    	pass
    
    

