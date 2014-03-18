import Tkinter as tk
    
class ToggleButton(tk.Button):
    __is_active = False
    
    ACTIVE_BG = "royalblue"
    ACTIVE_FG = "white"
    ACTIVE_HL = "cornflowerblue"
    NORMAL_BG = "gainsboro"
    NORMAL_FG = "black"
    NORMAL_HL = "#EDEDED"
    
    def __init__(self, master = None):
        tk.Button.__init__(self, master)
    
    def toggle(self):
        if self.__is_active:
            self.setOff()
        else:
            self.setOn()
    
    def setOff(self):
        self.__is_active = False
        self.config(background = self.NORMAL_BG, foreground = self.NORMAL_FG, activebackground = self.NORMAL_HL, activeforeground = self.NORMAL_FG)
        
    def setOn(self):
        self.__is_active = True
        self.config(background = self.ACTIVE_BG, foreground = self.ACTIVE_FG, activebackground = self.ACTIVE_HL, activeforeground = self.ACTIVE_FG)
          
    def getIsActive(self):
        return self.__is_active