"""
setup_classes.py
Update of original setup_classes.py to work with new GUI.

Author: Humphrey Shotton and Nicholas Sanders
Version: 2.0 [2014/03/23]

"""
import Tkinter as tk

# ==============================================================================
#
#   Parking Space Class
#
# ==============================================================================
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
    __label = None
    
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
        outline_colour = "#990000"
        
        # draw the rectangle
        self.__rectangle = canvas.create_rectangle(
            self.__start_point[0], self.__start_point[1],
            self.__end_point[0], self.__end_point[1],
            fill = fill_colour,
            outline = outline_colour, 
            width = 0,
            stipple = "gray50"
            )
        
        self.__label = canvas.create_text(self.getOrigins(), text = (str(self.__id) + "(space)"))
        return self
        
    
    def deleteRectangle(self, canvas):
    	"""
    	Delete the box rectangle from the canvas.
    	
    	Keyword Arguments:
        canvas -- TkCanvas from which to delete the rectangle
        
    	"""
        canvas.delete(self.__rectangle)
        canvas.delete(self.__label)
        return self

    def getOrigins(self):
    	"""Gets the most upper left co-ordinate of the box. """
        result = []
        
        if self.__start_point[0] < self.__end_point[0]: result.append(self.__start_point[0])
        else: result.append(self.__end_point[0])
        
        if self.__start_point[1] < self.__end_point[1]: result.append(self.__start_point[1])
        else: result.append(self.__end_point[1])
        
        return result
        
    def getOutput(self):
    	"""
    	Gets the output to be saved in a file.
    		
    	Returns:
    	Tuple of (id, type, x1, y1, x2, y2) or None if box is not present/complete.
        
    	"""
        
        if self.__start_point != [] and self.__end_point != []:
            space = (
                self.__id, 
                self.__type,
                self.__start_point[0],
                self.__start_point[1],
                self.__end_point[0],
                self.__end_point[1]
                )

            return space
        else:
            return None

# ==============================================================================
#
#   Control Point Class
#
# ==============================================================================
class ControlPoint:
    # replacement for setup_clases.Area
    
    # instance attributes
    __id = -1
    __type = 1  # type '1' is parking space, type '1' is CP
    __start_point = []
    __end_point = []
    __label = ""  # __rectangle label
    __rectangle = None  # the drawn rectangle
    __label = None
    canvas = None
    
    def __init__(self, i, canvas):
        self.__id = i
        self.canvas = canvas
        return
    
    def clear(self):
    	"""Clear the coordinates of the space. """
        self.__start_point = []
        self.__end_point = []
        
        return self
    
    def setStartPoint(self, x, y):
    	"""
    	Set the start point of the control point.
    	
    	Keyword Arguments: 
    	x -- x-coordinate of the control point
        y -- y-coordinate of the control point
        
        Returns:
        self -- The control point
        
    	"""
        # guard against invalid arguments
        if not isinstance(x, int) and not isinstance(y, int):
            print "ERROR: Cannot set start point: x & y must be integers."
        
        # set the start point and return the space   
        self.__start_point = [x, y]
        return self
    
    
    def setEndPoint(self, x, y):
    	"""
    	Set the end point of the control point.
    	
    	Keyword Arguments: 
    	x -- x-coordinate of the control point
        y -- y-coordinate of the control point
        
        Returns:
        self -- The control point
        
    	"""
        # guard against invalid arguments
        if not isinstance(x, int) and not isinstance(y, int):
            print "ERROR: Cannot set end point: x & y must be integers."
        
        # set the end point and return the space   
        self.__end_point = [x, y]
        return self
    
    
    def updatePoints(self, x, y):
    	"""
    	Update the values of the control point co-ordinates.
    	
    	Keyword Arguments: 
    	x -- x-coordinate of the control point
        y -- y-coordinate of the control point
        
    	"""
        x1 = x - 25
        y1 = y - 25
        x2 = x + 25
        y2 = y + 25
        
        self.clear()
        self.deleteRectangle(self.canvas)
        self.setStartPoint(x1, y1)
        self.setEndPoint(x2, y2)
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
        fill_colour = "#0066CC"
        outline_colour = "#003399"
        
        # draw the rectangle
        self.__rectangle = canvas.create_rectangle(
            self.__start_point[0], self.__start_point[1],
            self.__end_point[0], self.__end_point[1],
            fill = fill_colour,
            outline = outline_colour, 
            width = 0,
            stipple = "gray50"
            )
        
        display_id = str(self.__id + 1)
        self.__label = canvas.create_text([self.__start_point[0], self.__start_point[1]], text = display_id + "(control)")
        return self
        
    
    def deleteRectangle(self, canvas):
    	"""
    	Delete the box rectangle from the canvas.
    	
    	Keyword Arguments:
        canvas -- TkCanvas from which to delete the rectangle
        
    	"""
        canvas.delete(self.__rectangle)
        canvas.delete(self.__label)
        return self

    def getOutput(self):
    	"""
    	Gets the output to be saved in a file.
    		
    	Returns:
    	Tuple of (id, type, x1, y1, x2, y2) or None if box is not present/complete.
        
    	"""
        
        if self.__start_point != [] and self.__end_point != []:
            cp = (
                self.__id, 
                self.__type,
                self.__start_point[0],
                self.__start_point[1],
                self.__end_point[0],
                self.__end_point[1]
                )

            return cp
        else:
            return None
        


# and now for something completely different...

# ==============================================================================
#
#   Boxes Class
#
# ==============================================================================
class Boxes:
    boxes = []
    
    current_box = 1
    __type = 0
    
    MAX_SPACES = 10
    MAX_CPS = 3
    
    def __init__(self, canvas, type = 0):
        if type == 0:
            self.__type = 0
            self.boxes = [ParkingSpace(i, canvas) for i in range(self.MAX_SPACES)]
        elif type == 1:
            self.__type = 1
            self.current_box = 0
            self.boxes = [ControlPoint(j, canvas) for j in range(self.MAX_CPS)]
        else:
            print "ERROR: setup_classes.Boxes requires type 0 or 1."
        return
    
    #@staticmethod
    #def getCurrentBox(self):
    #    return self.boxes[self.current_box]

    def getCurrentBox(self):
        return self.current_box

    def get(self, id):
        return self.boxes[id]

    def length(self):
        return len(self.boxes)

    def setCurrentBox(self, i):
        self.current_box = i
    
    def clearAll(self, canvas):

        if self.__type == 0: self.setCurrentBox(1)
        elif self.__type == 1: self.setCurrentBox(0)

        for box in self.boxes:
            box.clear()
            box.deleteRectangle(canvas)