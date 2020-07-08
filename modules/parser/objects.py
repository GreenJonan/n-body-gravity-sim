from modules.parser import special_parsers as parse

from modules import body
from modules import constants
from modules import draw
from modules import universe
from modules import vector
from modules import colour

#keywords


# constants
g_str = "G"
e_str = "E"
R_str = "R"
dist_err_str = "distanceError"
t_del_str = "timeDelay"
update_num_str = "updateNumber"
time_step_str = "timeStep"
max_dist_str = "maxDistance"


# universe
dim_str = "dimension"
centre_str = "centre"
rest_str = "resistance"
energy_consv_str = "conserveEnergy"


# body
x_str = "X"
v_str = "V"
m_str = "mass"
q_str = "charge"
r_str = "radius"
name_str = "name"


vect_str = "vector"

col_str = "colour"
rgb_str = "rgb"
col_name = "name"


# screen

w_str = "width"
h_str = "height"
scl_str = "scale"
back_str = "background"
default_msg = "defaultMessage"
txt_col_str = "textColour"
label_size_str = "labelSize"
title_size_str = "titleSize"




#########################################






######################

####
####   Parse specific objects
####


def parse_vector(string:str, parent_name:str):
    """
        Given a string representation of a vector parse it.
        """
    string_ls = string.split(",")
    n = len(string_ls)
    
    vec = [0] * n
    i = 0
    while i < n:
        sub_str = string_ls[i]
        
        if n == 1 and sub_str == '':
            raise ValueError("\nStack Trace: {0}\nCannot Make vector of zero length.".format(parent_name))
        else:
            tmp = parse.parse_maths_string(sub_str, parent_name)
            if tmp == None:
                raise ValueError("\nStack Trace: {0}\nMissing vector component.\n '{1}'".format(string))
            else:
                vec[i] = tmp
        
        i += 1
    
    return vector.Vector(vec)




def parse_colour(string:str, parent_name:str):
    """
    Parse string representation of a colour.
        
    If No value is given, raise ValueError
    """
    colours = parse.parse_key_values(string, parent_name)
    
    if len(colours) != 1:
        raise ValueError("\nFile Trace: {0}\nInvalid number of colour attributes: {1}".format(parent_name, string))
    else:
        name = colours[0][0]
        value = colours[0][1]
        
        if name == col_name:
            # value is one of the default colour names
            return colour.get_colour_name(value, parent_name)
        
        cols = value.split(",")
        vec = [0]*len(cols)
        i = 0
        while i < len(cols):
            tmp = parse.parse_maths_string(cols[i], parent_name)
            if tmp == None:
                raise ValueError("\nStack Trace: {0}\nMissing colour component.\n '{1}'".format(string))
            else:
                vec[i] = tmp
            i += 1

        if name == "" or name == rgb_str:
            if len(cols) != 3:
                raise ValueError("\nStack Trace: {0}\nInvalid rgb colour length, string: '{1}'"\
                                 .format(parent_name, value))
            else:
                return tuple(vec)
        else:
            raise NameError("\nStack Trace: {0}\nUnknown name: '{1}'".format(parent_name, name))
    return





def parse_constants(string:str, parent_name:str):
    key_values = parse.parse_key_values(string, parent_name)
    consts = constants.Constants()

    for pair in key_values:
        name = pair[0]
        value = pair[1]
        my_name = parent_name + ">" + name

        if name == g_str:
            tmp = parse.parse_maths_string(value, my_name)
            if tmp != None:
                consts.G = tmp
        elif name == e_str:
            tmp = parse.parse_maths_string(value, my_name)
            if tmp != None:
                consts.E = tmp
        elif name == R_str:
            tmp = parse.parse_maths_string(value, my_name)
            if tmp != None:
                consts.R = tmp
        
        elif name == dist_err_str:
            tmp = parse.parse_maths_string(value, my_name)
            if tmp != None:
                consts.distance_error = tmp
        
        elif name == t_del_str:
            tmp = parse.parse_maths_string(value, my_name)
            if tmp != None:
                consts.time_delay = int(tmp)
        elif name == update_num_str:
            tmp = parse.parse_maths_string(value, my_name)
            if tmp != None:
                consts.update_number = int(tmp)
        elif name == time_step_str:
            tmp = parse.parse_maths_string(value, my_name)
            if tmp != None:
                consts.time_step = tmp

        elif name == max_dist_str:
            tmp = parse.parse_maths_string(value, my_name)
            if tmp != None:
                consts.max_dist = tmp

        else:
            raise NameError("\nStack Trace: {0}\nUnknown keyword '{1}'"\
                           .format(parent_name, name))

    return consts






def parse_universe(string:str, children_obj, parent_name:str):
    """
    Given a string that represents a universe object, and it's children objects,
    return a universe object.
    """
    key_values = parse.parse_key_values(string, parent_name)

    # skim bodies out from universe object.
    child_num = 0
    for child in children_obj:
        if isinstance(child, body.Body):
            child_num += 1
            child.id = child_num

    bodies = [None]*child_num
    i = 0
    c = 0
    while c < child_num:
        obj = children_obj[i]
        if isinstance(obj, body.Body):
            bodies[c] = obj
            c += 1
        i += 1


    # format remainding values.
    dim = 2
    centre = None
    resistance = False
    energy_consv = False
    
    passed_dim = False


    for pair in key_values:
        keyword = pair[0]
        value = pair[1]
        
        my_name = parent_name + ">" + keyword

        if keyword == dim_str:
            dim = int(value)
            passed_dim = True
        
        elif keyword == centre_str:
            centre = get_vector_key_value(value, children_obj, my_name)

        elif keyword == rest_str:
            resistance = get_bool(value, my_name)

        elif keyword == energy_consv_str:
            energy_consv = get_bool(value, my_name)

        else:
            raise NameError("\nStack Trace: {0}\nUnknown keyword '{1}'"\
                           .format(parent_name, keyword))

    if centre == None:
        centre = vector.Vector.zero_vector(dim)

    uni = universe.Universe(centre, *bodies)
    uni.resistance = resistance
    uni.conserve_energy = energy_consv
    return uni







def parse_body(string:str, child_obj:list, parent_name:str):
    """
    Given a string that represents a body object, and it's children objects, 
    return a body object.
    """
    key_values = parse.parse_key_values(string, parent_name)
    #print("Body objects:", child_obj)
    X = None
    V = None
    
    mass = 0
    charge = 0
    radius = 0
    col = colour.black
    name = ""
    
    
    for pair in key_values:
        keyword = pair[0]
        value = pair[1]
        
        key_name = parent_name + ">" + keyword
    
        if keyword == x_str:
            X = get_vector_key_value(value, child_obj, key_name)
    
        elif keyword == v_str:
            V = get_vector_key_value(value, child_obj, key_name)
        
        elif keyword == m_str:
            tmp = parse.parse_maths_string(value, key_name)
            if tmp != None:
                mass = tmp

        elif keyword == q_str:
            tmp = parse.parse_maths_string(value, key_name)
            if tmp != None:
                charge = tmp

        elif keyword == r_str:
            tmp = parse.parse_maths_string(value, key_name)
            if tmp != None:
                radius = tmp

        elif keyword == name_str:
            name = value

        elif keyword == col_str:
            col = get_colour_key_value(value, child_obj, key_name)
        else:
            raise NameError("\nStack Trace: {0}\nUnknown keyword '{1}'"\
                           .format(parent_name, keyword))
    
    
    if X == None:
        raise ValueError("\nStack Trace: {0}\nNo Position vector was passed to body '{1}'."\
                         .format(parent_name, string))
    if V == None:
        raise ValueError("\nStack Trace: {0}\nNo Velocity vector was passed to body '{1}'."\
                         .format(parent_name, string))

    id = -1
    return body.Body(id,X, V, mass, radius, charge, col, name)





def parse_screen(string:str, child_obj:list, parent_name):
    """
    Given a string that represents a screen object, and a set of the subchildren,
    return the screen object.
    """

    key_values = parse.parse_key_values(string, parent_name)

    width = constants.screen_width
    height = constants.screen_height

    screen_col = colour.white
    text_col = colour.black
    
    msg = None
    title_size = 100
    label_size = 50
    
    scale = -1

    for pair in key_values:
        name = pair[0]
        value = pair[1]
        
        my_name = parent_name + ">" + name

        if name == w_str:
            tmp = parse.parse_maths_string(value, my_name)
            if tmp != None:
                width = int( tmp )
        
        elif name == h_str:
            tmp = parse.parse_maths_string(value, my_name)
            if tmp != None:
                height = int( tmp )

        elif name == scl_str:
            tmp = parse.parse_maths_string(value,my_name)
            if tmp != None:
                scale = tmp

        elif name == back_str:
            screen_col = get_colour_key_value(value, child_obj, my_name)
        elif name == txt_col_str:
            text_col = get_colour_key_value(value, child_obj, my_name)

        elif name == default_msg:
            msg = value

        elif name == title_size_str:
            tmp = parse.parse_maths_string(value, my_name)
            if tmp != None:
                title_size = int( tmp )
        elif name == label_size_str:
            tmp = parse.parse_maths_string(value, my_name)
            if tmp != None:
                label_size = int( tmp )

        else:
            raise NameError("\nStack Trace: {0}\nUnknown keyword '{1}'"\
                           .format(parent_name, name))

    return draw.UniverseScreen(width, height, scale, screen_col, text_col, label_size, title_size, msg)




################### helper functions


def get_vector_key_value(value:str, ls:list, parent_name:str):
    err = False
    if len(value) < 2:
        err = True
    elif value[0] != '#':
        err = True
    if err:
        raise SyntaxError("\nStack Trace: {0}\nIncorrectly parsed Vector string '{2}'"\
                            .format(parent_name, value))

    pos = value.lstrip('#')
    pos_int = int(pos)
                              
    sub_obj = ls[pos_int]
    if not isinstance(sub_obj, vector.Vector):
        raise TypeError("\nStack Trace: {0}\nVector subvalue is non-vector, type: '{1}'"\
                        .format())
    else:
        return sub_obj



def get_colour_key_value(value:str, ls:list, parent_name:str):
    err = False
    if len(value) < 2:
        err = True
    elif value[0] != '#':
        err = True
    if err:
        raise SyntaxError("\nStack Trace: {0}\nIncorrectly parsed Colour string '{2}'"\
                          .format(parent_name, value))

    pos = value.lstrip('#')
    pos_int = int(pos)
    
    sub_obj = ls[pos_int]
    if not isinstance(sub_obj, tuple):
        raise TypeError("\nStack Trace: {0}\nColour subvalue is non-tuple, type: '{1}'"\
                        .format())
    else:
        return sub_obj



def get_bool(value:str, parent_name):
    if value == "True":
        return True
    elif value == "False":
        return False
    else:
        raise SyntaxError("\nStack Trace: {0}\nUnknowwn Boolean Type '{1}'"\
                          .format(parent_name, value))
