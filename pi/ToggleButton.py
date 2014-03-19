"""
Toggle button component, created from tkinter Button class for PiPark 
Raspberry Pi project.

Allows a Tkinter button to be toggled on and off with each click.

NB: Configurations to the button's appearance must be made after the object has
been instantiated by using the *.config() method. Only the button's master can
be set through the constructor method.

Author: Nicholas Sanders
Version: 1.0 [2014/03/19]

"""
import Tkinter as tk

# ==============================================================================
#
#   Toggle Button Class
#
# ==============================================================================

class ToggleButton(tk.Button):
    
    # --------------------------------------------------------------------------
    #   Instance Attributes
    # --------------------------------------------------------------------------
    
    # is the button toggled or not?
    __is_active = False
    
    # toggle button active and normal state colours
    # NB: 'HL' = Button highlight, 'BG' = background, 'FG' = foreground
    ACTIVE_BG = "royalblue"
    ACTIVE_FG = "white"
    ACTIVE_HL = "cornflowerblue"
    NORMAL_BG = "gainsboro"
    NORMAL_FG = "black"
    NORMAL_HL = "#EDEDED"  # this colour doesn't have a name, lets call him bob
    
    
    # --------------------------------------------------------------------------
    #   Constructor Method
    # --------------------------------------------------------------------------
    def __init__(self, master = None):
        """Constructor Method, just runs the super constructor. """
        
        # run super constructor method
        tk.Button.__init__(self, master)
    
    # --------------------------------------------------------------------------
    #   Toggle the Button
    # --------------------------------------------------------------------------
    def toggle(self):
        """
        Change the button's state (active<->normal) and appearance accordingly.
        
        """
        if self.__is_active:
            self.setOff()
        else:
            self.setOn()
    
    # --------------------------------------------------------------------------
    #   Set the Button to off/ on
    # --------------------------------------------------------------------------
    def setOff(self):
        """Set the button to 'normal' (off, untoggled) state. """
        self.__is_active = False
        self.config(
            background = self.NORMAL_BG,
            foreground = self.NORMAL_FG,
            activebackground = self.NORMAL_HL,
            activeforeground = self.NORMAL_FG
        )
        
    def setOn(self):
        """Set the button to 'active' (on, toggled) state. """
        self.__is_active = True
        self.config(
            background = self.ACTIVE_BG,
            foreground = self.ACTIVE_FG,
            activebackground = self.ACTIVE_HL,
            activeforeground = self.ACTIVE_FG
        )
        
        
    # --------------------------------------------------------------------------
    #   Get __is_active
    # --------------------------------------------------------------------------      
    def getIsActive(self):
        """Return whether the button is active (True) or not (False). """
        return self.__is_active