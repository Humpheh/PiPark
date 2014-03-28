#PiPark Setup
*README Revision 1.1 [2014/03/25]*
*Setup UI Version 2.1 [2014/03/26]*

Welcome to PiPark README, here's a quick run-through of the steps to successfully
setup your PiPark unit.

Welcome to PiPark setup, here's a quick run-through of the steps to successfully setup your PiPark unit.
            
### **Step 1**
After appropriately mounting the PiPark unit its positioning may need to be fine-tuned. To do this, click on the 'Capture New Setup Image' button and then 'Yes' when the dialogue box appears. A full-screen display of the unit's image feed will now be shown. Fine-tune the positioning of the unit, and once this has been finalised press the ENTER key to take a new setup image. Note: If at any time you wish to cancel the image feed without taking a new setup image press the ESCAPE button.
            
### **Step 2**
Next the parking spaces need to be marked onto the setup image. To do this click on the 'Add/Remove Spaces' button. To mark a space, click once on the setup image to signify a start location, and then click again for the end location of the rectangle that will represent the area of the parking space. For the best result the rectangle must be just smaller than the bounding lines of the parking space. 

Each parking space must be marked on the setup image. To add a new space press a NUMBER KEY between 0 and 9 and then LEFT-CLICK twice again as before. If you wish to remove a parking space, select its ID number (using NUMBER KEY between 0 and 9) and RIGHT-CLICK the mouse. A rundown of the controls is given below:

* To mark a parking space: LEFT-CLICK twice
* To delete a selected space: RIGHT-CLICK.
* To select a new parking space: press a NUMBER KEY 0 - 9.
            
### **Step 3**
Afterwards, three control points (CPs) need to be set. This can be done by clicking on the 'Add/Remove Control Points' button and performing single clicks on the setup image. Three control points are required for setup to be completed, and they should be set to a part of the car park that is not a parking space. As with adding/removing parking space references in step (2): RIGHT-CLICK to remove a selected space, and use the NUMBER KEYS 1 to 3 to select a new CP. A rundown of the control is given below:

* To mark a control point: LEFT-CLICK
* To delete a control point: RIGHT-CLICK.
* To select a new control point: press a NUMBER KEY 1 - 3.
            
### **Step 4**
The final step to completing the setup is to save and register the car park with the server. To save the reference data click the 'Save' button and the click 'OK' when the dialogue box appears. After the setup data has been saved you can now register with the server; click on the 'Register' button and then click 'OK' when the dialogue box appears.

The setup now is complete. To run the main PiPark software click on the 'Start PiPark' button or, if you wish to run PiPark later: click on the 'Quit' button and then run PiPark from the command line using the command './main.py' whilst in the '*/PiPark/pi' directory.
