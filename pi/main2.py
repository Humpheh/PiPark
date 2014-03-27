"""
Authors: Nicholas Sanders & Humphrey Shotton
Filename: main2.py
Version: 2.0 [2014/03/27]

Main application. Spins two threads, one to deal with GUI and inputs, and the
other to handle the pipark detection software.

"""
# les importations
import Tkinter as tk
import tkMessageBox
import imageread
import thread
import time

# global variables
camera = imageread.setup_camera(is_fullscreen = False)
has_quit = False

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
        global has_quit
        
        self.quit()
        self.master.destroy()
        has_quit = True
    
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
def create_application():
    """
    Run main program loop. Detect changes to parking spaces and update 
    appropriate availabity of the spaces to the server.
    
    """
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
    print "INFO: run()"
    global camera
    
    # image save location
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

def main():
    # use global variable DUN DUN DUNNN!
    global has_quit
    
    # sleep for 3 seconds to ensure camera has loaded before continuing.
    time.sleep(3)
    
    try:
        # spin thread for the application and for the detection software
        thread.start_new_thread(create_application, ())
        thread.start_new_thread(run, ())
    except:
    	print "ERROR: Failed to start new thread =("
        
    # do not end main thread until user 
    while not has_quit:
    	pass
           
# -----------------------------------------------------------------------------
#  Run Program
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
    
    

