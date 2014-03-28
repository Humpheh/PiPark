"""
Authors: Humphrey Shotton and Nicholas Sanders
Filename: tkinter.py
Version: [2014/01/20]

Description:
Interface for setting up the areas for the car parking sensor to check. Draws an image
which allows for boxes to be drawn on top. 
"""

from Tkinter import *
from PIL import Image, ImageTk
from setup_classes import Area, Boxes, SelWindow
import tkMessageBox
import settings as s
import sys

# -----------------------------------------------------------------------------
# Event on mouse being clicked.
# -----------------------------------------------------------------------------

def callbackMouse(event):
    SelWindow.w.focus_set()
    Boxes.getCur().update_pos(event.x, event.y)
    print "INFO: Clicked at", event.x, event.y
    task()

# -----------------------------------------------------------------------------
# Event on key being pressed
# -----------------------------------------------------------------------------

def callbackKey(event):
    key = (event.char)
    try:
    	# Make an output file
        if key == 'o':
            output_coords()
		
	    # Swap the type of the box
        if key == 't':
            Boxes.getCur().swap_type()

	    # Clear the current box
        if key == 'c':
            Boxes.getCur().clear()
        
        # Switch the setting to a new number
        i = int(key)
        if i < 10 and i >= 0:
            Boxes.setCur(i)
            print "INFO: Switching to", i
    except: pass
    
    task()
  
# -----------------------------------------------------------------------------
# Updating canvas task
# -----------------------------------------------------------------------------
  
def task(cont = False):
    # Delete and redraw the current box
    Boxes.getCur().delete_rect(SelWindow.w).draw_rect(SelWindow.w)

    # Update the info text at the top
    SelWindow.w.delete(SelWindow.text)
    SelWindow.text = SelWindow.w.create_text((s.WINDOW_WIDTH/2, 10),
           		text = str(Boxes.sel) + "selected - O = save output, 1-9 to change box num, T = toggle type, C = clear current box, close window to return to setup")
    
    if cont:
        SelWindow.master.after(2000,task)  # reschedule event in 2 seconds

# -----------------------------------------------------------------------------
# Gets the image scaled to the window size
# -----------------------------------------------------------------------------

def get_image_scaled(image):
    # Calculate the aspect ratio of the image
    image_aspect = float(image.size[1]) / float(image.size[0])

    # Scale the image
    image_scaled = (s.WINDOW_WIDTH, int(s.WINDOW_WIDTH * image_aspect))
    
    if image_aspect > 1:
        image_scaled = (int(s.WINDOW_HEIGHT / image_aspect), s.WINDOW_HEIGHT)

    coords = ((s.WINDOW_WIDTH - image_scaled[0])/2,
              (s.WINDOW_HEIGHT - image_scaled[1])/2,
              image_scaled[0], image_scaled[1])

    # Creat the resized image and return it and the co-ordinates.
    return ImageTk.PhotoImage(
        image.resize(image_scaled, Image.ANTIALIAS)), coords

# -----------------------------------------------------------------------------
# Function to output the co-ordinates of the boxes
# -----------------------------------------------------------------------------

def output_coords():
    # Open the file to output the co-ordinates to
    f1 = open('./setup_data.py', 'w+')

    # Print the dictionary data to the file
    print >>f1, 'boxes = ['
    
    for i in range(Boxes.length()):
        c = Boxes.get(i).get_output(SelWindow.bgcoords)
        
        if c != None:
            o = (i)
            print >>f1, c, ','

    print >>f1, ']'
    print 'INFO: Box data saved in file boxdata.py.'
    tkMessageBox.showinfo("Pi Setup", "Box data saved in file.")

# -----------------------------------------------------------------------------
# Main Program
# -----------------------------------------------------------------------------

def main(image):
    # Initialise the canvas to draw on
    SelWindow.master = Tk()
    SelWindow.w = Canvas(SelWindow.master, width=s.WINDOW_WIDTH, height=s.WINDOW_HEIGHT)

    # Bind the keyboard and mouse events to functions
    SelWindow.w.bind("<Button-1>", callbackMouse)
    SelWindow.w.bind("<Key>", callbackKey)
    SelWindow.w.pack()

    # Schedule the task event
    task(True)

    # Drawing the under image
    try:
        print "INFO: Attempting to open", image
        bgimage, bgcoords = get_image_scaled(image)
    except:
        print "ERROR: Failed in loading image."

    # Store the co-ordinates and create image on the canvas
    SelWindow.bgcoords = bgcoords
    SelWindow.w.create_image((s.WINDOW_WIDTH/2,s.WINDOW_HEIGHT/2), image = bgimage)

    # Keep the program running
    mainloop()

if __name__ == "__main__":
    # Try and load a test image as background
    main(Image.open("test.jpg"))








