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


grey = (127,127,127)





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
    hsv.hue = rnd.random()
    return hsv.get_rgb()


def rgb_inverse(rgb:tuple) -> tuple:
    """
    Given a colour, return it's HSV inverse as an rgb
    """

    hsv = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)

    hue = hsv[0] - 0.5
    if hue < 0:
        hue = 1 + hue
    val = 1 - hsv[2]

    tmp_rgb = colorsys.hsv_to_rgb(hue, hsv[1], val)
    return int(255 * tmp_rgb[0]), int(255 * tmp_rgb[1]), int(255 * tmp_rgb[2])



def get_colour_name(name:str, stack_pos:str=""):
    """
    Get a colour rgb value based on a name value.
    """
    
    if name == "random":
        return random_rgb()
    elif name == "white":
        return white
    elif name == "black":
        return black
    elif name == "grey":
        return grey
    elif name == "red":
        return red
    elif name == "green":
        return green
    elif name == "blue":
        return blue
    elif name == "yellow":
        return yellow
    elif name == "turquoise":
        return turquoise
    elif name == "magenta":
        return magenta
    elif name == "purple":
        return purple
    elif name == "orange":
        return orange
    elif name == "lime":
        return lime
    elif name == "light blue":
        return light_blue
    else:
        raise SyntaxError("\nStack Trace: {0}\nUnknown Colour '{1}'".format(stack_pos, name))




def get_rgb_str(col:tuple)->str:
    if len(col) != 3:
        raise ValueError("Not valid RGB value:", col)

    else:
        r = col[0]
        g = col[1]
        b = col[2]
        return "rgb: " + str(r) +"," +str(g) +","+ str(b)
