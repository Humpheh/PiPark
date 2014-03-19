"""
setup_classes2.py
Update of setup_classes.py to work with new UI.

Author: Humphrey Shotton
Version: 2.0 [2014/03/19]

"""
import Tkinter as tk

class ParkingSpace:
    # replacement for setup_classes.Area
    
    # instance attributes
    __id = -1
    __start_point = []
    __end_point = []
    __text = ""
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
            self.deleteRectangle()
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
        if not isinstance(canvas, tk.Canvas): return
        if self.__start_point == [] or self.__end_point == []: return
            
        fill_colour = "#CC0000"
        
        self.rect = canvas.create_rectangle(
            self.__start_point[0], self.__start_point[1],
            self.__end_point[0], self.__end_point[1],
            fill = fill_colour, 
            width = 0
            )
        
        return self
        
    
    def deleteRectangle(self, canvas):
    	"""
    	Delete the box rectangle from the canvas.
    	
    	Keyword Arguments:
        canvas -- TkCanvas from which to delete the rectangle
    	"""
        canvas.delete(self.rect)
        return self