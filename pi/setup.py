"""
Authors: Nicholas Sanders & Humphrey Shotton
Filename: setup.py
Version: [2014/01/21]

Description:
...

"""

# -----------------------------------------------------------------------------
#  Imports
# -----------------------------------------------------------------------------

import sys

import imageread
from PIL import Image
import setup_selectarea

# -----------------------------------------------------------------------------
#  Main Program
# -----------------------------------------------------------------------------
def __main():
    print """
------------------------------------------
    
         Setup for PiPark, 2014
    
==========================================
    """
    
    # continually loop menu unitl user chooses 'q' to quit
    setup_image_location = "./images/setup.jpeg"
    while True:
        user_choice = __menu_choice()
        
        if user_choice == '1':
            # initialise camera and start pi camera preview
            camera = imageread.setup_camera()
            camera.start_preview()
            
            print "INFO: Setup image save location:", str(setup_image_location)
            print "INFO: Camera preview initiated."
            print ""
            
            # when user presses enter, take a new setup image. Then ask the user to confirm or
            # reject the image. If image is rejected, take a new image.
            while True:
                raw_input("When ready, press ENTER to capture setup image.")
                camera.capture(setup_image_location)
                user_input = raw_input("Accept image (y/n)? > ")
                
                if user_input.lower() in ('y', "yes"): break
                    
            # picture saved, end preview
            camera.close()
            print ""
            print "INFO: Setup image has been saved to:", str(setup_image_location)
            print "INFO: Camera preview closed."
        
        
        elif user_choice == '2':
            # check setup image exists, if not print error directing to option 1
            try:
                setup_image = Image.open(setup_image_location)
            except:
                print "ERROR: Setup image does not exist. Select option 1 to"
                print "create a new setup image."
            
            # setup image exists, so open GUI window allowing selection of spaces and
            # reference areas
            print """
            When the window opens use the mouse to mark parking spaces and 3 reference
            areas. Press T to toggle between marking parking spaces and reference areas and
            the numbers 1 - 0 to mark new areas.
            """
            raw_input("\nPress ENTER to continue...\n")
            setup_selectarea.main(setup_image)
        
        
        elif user_choice == '3':
            # attempt to import the setup data and box data
            bxs = None
            try:
                import setup_data
                
                bxs = setup_data.boxes
                if not isinstance(bxs, list):
                    raise ValueError()
            except:
                print "Setup data does not exist. Please run options 1 and 2 first."
                continue
                
            # attempt to import the server senddata module
            try:
                import senddata
            except:
                print "Could not import send data file."
                continue
            
            # deregister all areas associated with this pi (start fresh)
            out = senddata.deregister_pi()
            
            try:
                out['error']
                print "Error in connecting to server. Please update settings.py."
                continue
            except:
                pass
            
            # for each box in boxes
            for b in bxs:
                if b[1] == 0:
                    senddata.register_area(b[0])
                    print "Registering area", b[0], "on database."
                    
            print "Registration complete."
        
        
        elif user_choice == '4':
            main.run_main()
        
                                                 
        elif user_choice.lower() in ('h', "help"):
            print """
            help message
            """
            
            
        elif user_choice.lower() in ('q', "quit"):
            print "Setup complete."
            break
        
        
        else:
            print "\nERROR: Invalid menu choice.\n"



# -----------------------------------------------------------------------------
#  Main Menu
# -----------------------------------------------------------------------------
def __menu_choice():
    print """
At the promt please type a menu selection. For setup instructions type 'help'.
    
1 -- Take setup image.
2 -- Mark parking spaces and control locations.
3 -- Register on server
4 -- Run PiPark main program
h -- Help
q -- Quit
    
    """
    
    user_choice = raw_input("> ")
    
    return user_choice

# -----------------------------------------------------------------------------
#  Run Main Program
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    __main()
