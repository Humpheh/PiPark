"""
Authors: Humphrey Shotton and Nicholas Sanders
Filename: setup_classes.py
Version: [2014/01/20]

Description:
File with classes to be used in the setup interface.
"""

# -----------------------------------------------------------------------------
# Class for organising the boxes drawn on the image.
# -----------------------------------------------------------------------------
class Area:
    def __init__(self, i):
    	"""
    	Setup the box area.
    	
    	Args: 
    		i: The ID of the box.
    	"""
        self.id = i
        self.p1 = self.p2 = []
        self.rect = None
        self.text = None
        self.type = 0
        return

    def swap_type(self):
    	"""
    	Swaps the type of the box between parking and control.
    	"""
        self.type = 0 if self.type == 1 else 1
        return self

    def clear(self):
    	"""
    	Clear the co-ordinates of the box.
    	"""
        self.p1 = self.p2 = []
        return self

    def set_p1(self, x, y):
    	"""
    	Set the first co-ordinate of the box.
    	
    	Args: 
    		x, y: Co-ordinate of the first box point.
    	"""
        self.p1 = [x, y]
        return self

    def set_p2(self, x, y):
    	"""
    	Set the second co-ordinate of the box.
    	
    	Args: 
    		x, y: Co-ordinate of the second box point.
    	"""
        self.p2 = [x, y]
        return self

    def get_origins(self):
    	"""
    	Gets the most upper left co-ordinate of the box.
    	"""
        out = []
        
        if self.p1[0] < self.p2[0]: out.append(self.p1[0])
        else: out.append(self.p2[0])
        
        if self.p1[1] < self.p2[1]: out.append(self.p1[1])
        else: out.append(self.p2[1])
        
        return out

    def draw_rect(self, w):
    	"""
    	Draw the rectangle for the box on the canvas.
    	
    	Args: 
    		w: TkCanvas to draw the box to.
    	"""
        if self.p1 != [] and self.p2 != []:
            fillcol = "#6633FF" if self.type == 0 else "#CC0000"
            
            self.rect = w.create_rectangle(self.p1[0], self.p1[1],
                                           self.p2[0], self.p2[1],
                                           fill=fillcol, width=0)

            suffix = " (space)" if self.type == 0 else " (control)"
                                    
            self.text = w.create_text(self.get_origins(), text = (str(self.id) + suffix))
        return self

    def delete_rect(self, w):
    	"""
    	Deletes the box rectangle from the canvas.
    	
    	Args: 
    		w: TkCanvas to remove box and text from.
    	"""
        w.delete(self.rect)
        w.delete(self.text)
        return self

    def update_pos(self, x, y):
    	"""
    	Update the position of the co-ordinates.
    	
    	Args: 
    		x, y: Co-ordinate of the new box point.
    	"""
        if self.p1 == [] or self.p2 != []:
            self.clear().set_p1(x, y)
        else:
            self.set_p2(x, y)

    def _get_pos_percent_ind(self, coord, org, length):
    	"""
    	Calculates the percentage across the screen a point is.
    	
    	Args: 
    		coord: The co-ordinate to test.
    		org: The origin of the image on the canvas in the same plane as coord.
    		length: The length of the image in the same plane as coord.
    		
    	Returns:
    		Float of the percentage coord is across image length.
    	"""
        coord = float(coord - org) / float(length)

        return 1 if coord > 1 else coord if coord > 0 else 0
    
    def get_output(self, imgc):
    	"""
    	Gets the output to be saved in a file.
    	
    	Args: 
    		imgc: The coordinates and size of the image on the canvas.
        		  (x, y, width, height)
    		
    	Returns:
    		Tuple of (id, type, x1, y1, x2, y2) or None if box is not present/complete.
    	"""
        if self.p1 != [] and self.p2 != []:
            box = (self.id, self.type,
                   self._get_pos_percent_ind(self.p1[0], imgc[0], imgc[2]),
                   self._get_pos_percent_ind(self.p1[1], imgc[1], imgc[3]),
                   self._get_pos_percent_ind(self.p2[0], imgc[0], imgc[2]),
                   self._get_pos_percent_ind(self.p2[1], imgc[1], imgc[3]))

            return box
        
        return None


class SelWindow:
    # Other random variables to be stored statically
    bgcoords = None
    w = None
    text = None
    master = None
        
class Boxes:
    # Variables relevant to box class
    rects = [Area(i) for i in range(10)]
    sel = 1

    # Other random variables to be stored statically
    bgcoords = None
    w = None
    text = None
    master = None

    @staticmethod
    def getCur():
        return Boxes.rects[Boxes.sel]

    @staticmethod
    def get(id):
        return Boxes.rects[id]	

    @staticmethod
    def length():
        return len(Boxes.rects)

    @staticmethod
    def setCur(i):
        Boxes.sel = i 
