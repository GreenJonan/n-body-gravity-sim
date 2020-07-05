# colour constants
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

yellow = (255,255,0)
turquoise = (0,255,255)
magenta = (255,0,255)

purple = (127,0,255)
mid_blue = (0,127,255)
orange = (255,127,0)
dark_pink = (255,0,127)
yellow_green = (127,255,0)
lime = (0,255,127)
# yellow_green and lime are questionable names


light_blue = (0,161,255)



"""
Look at: https://www.html.am/html-codes/color/color-scheme.cfm?rgbColor=0,255,127 
for more colours
"""



import colorsys
import random as rnd


class HSVColour:
    def __init__(self, step=0):
        self.hue = 0
        self.sat = 1
        self.val = 1
        self.col_step = step
    
    def next_colour(self, reverse=False):
        
        dir = 1
        if reverse:
            dir = -1
        self.hue += dir * self.col_step
        
        if self.hue >= 1:
            self.hue -= 1
        elif self.hue <= 0:
            self.hue += 1
        return
    
    def get_rgb(self):
        rgb = colorsys.hsv_to_rgb(self.hue, self.sat, self.val)
        RGB = int(255 * rgb[0]), int(255 * rgb[1]), int(255 * rgb[2])
        return RGB




def random_rgb():
    """
    Return a random RGB tuple, with saturation=1 and value=1
    """

    hsv = HSVColour()
    hsv.hue = = rnd.random()
    return hsc.get_rgb()
