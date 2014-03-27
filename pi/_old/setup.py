"""
Authors: Nicholas Sanders & Humphrey Shotton
Filename: setup.py
Version: [2014/01/31]

Description:
Setup file for PiPark, allows user to fine-tune camera positioning, mark 
reference areas for parking spaces and register the PiPark unit with the
server.

"""

# -----------------------------------------------------------------------------
#  Imports
# -----------------------------------------------------------------------------
# python
import sys

# PiPark
import imageread
import main
import setup_selectarea

# Pythonware, Image library
from PIL import Image


# -----------------------------------------------------------------------------
#  Main Program
# -----------------------------------------------------------------------------
def __main():
    """Main function for setup.py. Contains and handles the menu loop."""
    
    print """
--------------------------------------------------------------------------------
    
                             Setup for PiPark, 2014
    
================================================================================
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
            # attempt to import the setup data and ensure 'boxes' is a list. If fail,
            # return to main menu prompt.
            try:
                import setup_data
                boxes = setup_data.boxes
                if not isinstance(boxes, list): raise ValueError()
            except:
                print "ERROR: Setup data does not exist. Please run options 1 and 2 first."
                continue
                
            # attempt to import the server senddata module. If fail, return to main menu
            # prompt.
            try:
                import senddata
            except:
                print "ERROR: Could not import send data file."
                continue
            
            # deregister all areas associated with this pi (start fresh)
            out = senddata.deregister_pi()
            
            try:
                out['error']
                print "ERROR: Error in connecting to server. Please update settings.py."
                continue
            except:
                pass
            
            # register each box on the server
            for box in boxes:
                if box[1] == 0:
                    senddata.register_area(box[0])
                    print "INFO: Registering area", box[0], "on server database."
                    
            print "\nRegistration complete."
        
        
        elif user_choice == '4':
            print "This will complete the setup and run the main PiPark program."
            user_input = raw_input("Continue and run the main program? (y/n) >")
            if user_input.lower in ('y', 'yes'):
                main.run_main()
                break
                                                 
        elif user_choice.lower() in ('h', "help"):
            print """
Welcome to PiPark setup, here's a quick run-through of the steps to successfully
setup your PiPark unit.
            
  1) Ensure that the PiPark unit is mounted suitable above the cark park so that
     the PiPark's camera is able to look down with a clear view upon the spaces
     that are required to be monitored.
            
  2) At the main menu prompt of this setup program enter option '1' to fine tune
     the direction of the camera so that it is clearly able to view the spaces.
     When you have finalised the position of the camera press ENTER to capture a
     setup image. If everything is correct and you do not wish to recapture the
     setup image, type 'y' or 'yes' at the prompt to continue the setup program.
     If you wish to recapture the setup image, type 'n' or 'no' at the prompt.
     
     Note: The setup image does not require the car park to be empty.

  3) Once back at the main menu prompt, enter option '2' to open up the setup
     GUI, which will open a new window allowing you to mark parking space areas
     and reference areas on the setup image that was captures as part of step 2.
     
     When the window has opened use the mouse to mark start and end corners of
     rectangles, which will represent the areas to be processed by the main
     program. To toggle between marking reference areas and parking space areas
     press 'T'. Blue areas represent parking spaces, and red areas represent
     reference areas.
     
     Currently up to ten areas can be marked, using the number keys from 1 - 0.
     There must be exactly 3 reference areas (RED) marked on the setup image
     and at least 1 parking space.
     
     When all areas have been marked on the image press 'O' to output the marked
     areas' co-ordinates to a file and close the window to continue completing
     the setup.
     
     Controls Summary:
       T -- Toggle between reference areas (RED) and parking spaces (BLUE).
       C -- Clear all marked areas.
       O -- Output the reference areas to a file.
       1 to 0 -- Change area ID numbers.

  4) The final step to completing the setup is to choose option '3' from the 
     main menu prompt. When selected the parking spaces will be registered to
     the server, and can now be viewed on the website.

  5) The setup is now complete; at the main menu prompt type 'q' or 'quit' to
     terminate the setup program. Alternatively, choose option 3 to immediately
     run the main PiPark program.
            """
            
            
        elif user_choice.lower() in ('q', "quit"):
            print ""
            break
        
        
        else:
            print "\nERROR: Invalid menu choice.\n"



# -----------------------------------------------------------------------------
#  Main Menu
# -----------------------------------------------------------------------------
def __menu_choice():
    """Print the menu options and return the user choice."""
    
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
