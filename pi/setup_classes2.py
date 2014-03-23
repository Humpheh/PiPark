"""
setup_classes2.py
Update of setup_classes.py to work with new GUI.

Author: Humphrey Shotton and Nicholas Sanders
Version: 2.0 [2014/03/23]

"""
import Tkinter as tk

class ParkingSpace:
    # replacement for setup_classes.Area
    
    # instance attributes
    __id = -1
    __type = 0  # type '0' is parking space, type '1' is CP
    __start_point = []
    __end_point = []
    __label = ""  # __rectangle label
    __rectangle = None  # the drawn rectangle
    canvas = None
    
    def __init__(self, i, canvas = None):
        # set space id number
        self.__id = i
        self.canvas = canvas
    
    
    def clear(self):
    	"""Clear the coordinates of the space. """
        self.__start_point = []
        self.__end_point = []
        
        return self
    
    
    def setStartPoint(self, x, y):
    	"""
    	Set the start point of the parking space.
    	
    	Keyword Arguments: 
    	x -- x-coordinate of the parking space
        y -- y-coordinate of the parking space
        
        Returns:
        self -- The parking space
        
    	"""
        # guard against invalid arguments
        if not isinstance(x, int) and not isinstance(y, int):
            print "ERROR: Cannot set start point: x & y must be integers."
        
        # set the start point and return the space   
        self.__start_point = [x, y]
        return self
    
    
    def setEndPoint(self, x, y):
    	"""
    	Set the end point of the parking space.
    	
    	Keyword Arguments: 
    	x -- x-coordinate of the parking space
        y -- y-coordinate of the parking space
        
        Returns:
        self -- The parking space
        
    	"""
        # guard against invalid arguments
        if not isinstance(x, int) and not isinstance(y, int):
            print "ERROR: Cannot set end point: x & y must be integers."
        
        # set the end point and return the space   
        self.__end_point = [x, y]
        return self
    
    
    def updatePoints(self, x, y):
    	"""
    	Update the values of the co-ordinates.
    	
    	Keyword Arguments: 
    	x -- x-coordinate of the parking space
        y -- y-coordinate of the parking space
        
    	"""
        if self.__start_point == [] or self.__end_point != []:
            self.clear()
            self.deleteRectangle(self.canvas)
            self.setStartPoint(x, y)
        else:
            self.setEndPoint(x, y)
            self.drawRectangle(self.canvas)
    
    
    def drawRectangle(self, canvas):
    	"""
    	Draw the rectangle for the box on the canvas.
    	
    	Keyword Arguments: 
    	canvas -- TkCanvas in which to draw the rectangle
        
    	"""
        # guard against illegal data types
        if not isinstance(canvas, tk.Canvas): return
        
        # if either start or end point doesn't exist; a rectangle cannot be
        # drawn, so return
        if self.__start_point == [] or self.__end_point == []: return
        
        # set rectangle colour
        fill_colour = "#CC0000"
        outline_colour = "#660000"
        
        # draw the rectangle
        self.__rectangle = canvas.create_rectangle(
            self.__start_point[0], self.__start_point[1],
            self.__end_point[0], self.__end_point[1],
            fill = fill_colour,
            outline = outline_colour, 
            width = 0
            )
        
        return self
        
    
    def deleteRectangle(self, canvas):
    	"""
    	Delete the box rectangle from the canvas.
    	
    	Keyword Arguments:
        canvas -- TkCanvas from which to delete the rectangle
        
    	"""
        canvas.delete(self.__rectangle)
        return self



class ControlPoint:
    # replacement for setup_clases.Area
    
    def __init__(self, i, canvas = None):
        return
        


# and now for something completely different...

class Boxes:
    boxes = []
    
    current_box = 1
    
    MAX_SPACES = 10
    MAX_CPS = 3
    
    def __init__(self, canvas, type = 0):
        if type == 0:
            self.boxes = [ParkingSpace(i, canvas) for i in range(self.MAX_SPACES)]
        elif: type == 1:
            self.boxes = [ControlPoint(j, canvas) for j in range(self.MAX_CPS)]
        else:
            print "ERROR: setup_classes2.Boxes requires type 0 or 1."
        return
    
    #@staticmethod
    #def getCurrentBox(self):
    #    return self.boxes[self.current_box]

    def getCurrentBox(self):
        return self.current_box

    def get(self, id):
        return self.boxes[id]	

    def getLength(self):
        return len(self.boxes)

    def setCurrentBox(self, i):
        self.current_box = i
    
    def clearAll(self, canvas):
        for box in self.boxes:
            if isinstance(box, ParkingSpace):
                box.clear()
                box.deleteRectangle(canvas)
            if isinstance(box, ControlPoint):
                box.clear()
                box.deleteRectangle(canvas)