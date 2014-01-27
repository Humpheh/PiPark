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
    
          Setup for CARPARK-O-TRON-9000
    
    ==========================================
    """
    
    # continually loop menu unitl user chooses 'q' to quit
    setup_image_location = "./images/setup.jpeg"
    while True:
        user_choice = __menu_choice()
        
        if user_choice == '1':
            # set setup image save locaiton
            print "INFO: Setup image save location:", str(setup_image_location)
            
            # start picam
            print "INFO: Camera preview initiated."
            camera = imageread.setup_camera()
            camera.start_preview()
            
            # continually capture images until user accepts.
            while True:
                raw_input("Press enter to capture image.")
                camera.capture(setup_image_location)
        
                user_input = raw_input("Accept image (y/n)? > ")
                
                if user_input in ["y", "Y", "yes", "YES"]: break
            
            # picture saved, end preview
            print "INFO: Setup image has been saved to:", str(setup_image_location)
            print "      Ending camera preview."
            camera.close()
        
           
        elif user_choice == '2':
            # check setup image exists
            try:
                setup_image = Image.open(setup_image_location)

                # Run UI Allowing selection of spaces
                print "\nSelect and mark control-reference locations and parking"
                print "space locations."
                setup_selectarea.main(setup_image)
            except:
                print "ERROR: Setup image does not exist. Select option 1 to"
                print "create a new setup image."
        
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
                                                    
        elif user_choice in ['q', 'Q']:
            print "Setup complete."
            break
        
        else:
            print "\nERROR: Invalid menu choice.\n"

# -----------------------------------------------------------------------------
#  Main Menu
# -----------------------------------------------------------------------------
def __menu_choice():
    print """
    At the promt please make a selection.
    
    1 -- Take setup image.
    2 -- Mark parking spaces and control locations.
    3 -- Register on server
    q -- Quit
    
    """
    
    user_choice = raw_input("> ")
    
    return user_choice

# -----------------------------------------------------------------------------
#  Run Main Program
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    __main()
