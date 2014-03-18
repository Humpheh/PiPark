import Tkinter as tk
    
class ToggleButton(tk.Button):
    __is_active = False
    
    ACTIVE_BG = "blue"
    ACTIVE_FG = "white"
    NORMAL_BG = "grey"
    NORMAL_FG = "black"
    
    def __init__(self, master = None):
        tk.Button.__init__(self, master)
    
    def toggle(self):
        if self.__is_active:
            self.__is_active = False
            self.config(background = self.NORMAL_BG, foreground = self.NORMAL_FG)
        
        else:
            self.__is_active = True
            self.config(background = self.ACTIVE_BG, foreground = self.ACTIVE_FG)
    
    def getIsActive():
        return self.__is_active
        