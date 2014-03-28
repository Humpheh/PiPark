#PiPark Setup
*Version 1.1*
Welcome to PiPark README, here's a quick run-through of the steps to successfully
setup your PiPark unit.

###**Step 1** - Mount the PiPark unit
Ensure that the PiPark unit is mounted suitable above the cark park so that
the PiPark's camera is able to look down with a clear view upon the spaces
that are required to be monitored.

###**Step 2** - Run setup.py
Run setup.py.
     
At the main menu prompt of the setup program enter option '1' to fine tune
the direction of the camera so that it is clearly able to view the spaces.
When you have finalised the position of the camera press ENTER to capture a
setup image. If everything is correct and you do not wish to recapture the
setup image, type 'y' or 'yes' at the prompt to continue the setup program.
If you wish to recapture the setup image, type 'n' or 'no' at the prompt.

Note: The setup image does not require the car park to be empty.}

###**Step 3** - Mark reference areas using GUI
Once back at the main menu prompt, enter option '2' to open up the setup
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
* T -- Toggle between reference areas (RED) and parking spaces (BLUE).
* C -- Clear all marked areas.
* O -- Output the reference areas to a file.
* 1 to 0 -- Change area ID numbers.

###**Step 4** - Register spaces with server
The final step to completing the setup is to choose option '3' from the 
main menu prompt. When selected the parking spaces will be registered to
the server, and can now be viewed on the website.

###**Step 5** - Finish
The setup is now complete; at the main menu prompt type 'q' or 'quit' to
     terminate the setup program. Alternatively, choose option 3 to immediately
     run the main PiPark program.