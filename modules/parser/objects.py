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

warning_str = "WARNING"

# universe
dim_str = "dimension"
centre_str = "centre"
rest_str = "resistance"
energy_consv_str = "conserveEnergy"

max_v_str = "maxSpeed"
relat_str = "relativistic"

trail_str = "trailHistory"

nlaw_str = "__nLaw"
nmetric_str = "__nMetric"


# body
x_str = "X"
v_str = "V"
m_str = "mass"
q_str = "charge"
r_str = "radius"
name_str = "name"
anch_str = "anchor"

skip_str = "trailSkip"
max_trail_str = "maxTrail"
trail_col_str = "trailColour"


vect_str = "vector"
polar_str = "polar"
cart_str = "cartesian"


col_str = "colour"
rgb_str = "rgb"
col_name = "name"

collide_str = "collide"
elast_str = "elasticity"


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





# variable parser

def parse_variables(strings:list, parent_name:str, variables:dict):
    """
    Given a set of variables and values, place them into the variables dictionary.
    Variables are specified by '=' rather than ':', which indicates attributes.
    """
    if len(strings) != 1:
        param_error(parent_name, strings, 1)
    string = strings[0]
    
    key_values = parse.parse_key_values(string, parent_name, sep="=")

    for pair in key_values:
        name = pair[0]
        value = pair[1]

        val = parse.parse_maths_string(value, parent_name, variables)
        variables[name] = val
    return variables




# for loop parser

def parse_forloop(strings:list, parent_name:str, children, variables:dict):
    """
    Given a for loop and set of arguments, return the iterator.
    
    Children is a parser object.
    """
    if len(strings) != 2:
        param_error(parent_name, strings, 2)
    args = strings[0]
    string = strings[1]

    output = []


    # format parsing
    parts = args.split(";")
    if len(parts) != 3:
        raise SyntaxError("\nStack Trace: {0}\Invalid number of parameters in for loop, require three.\n '{1}'"\
                            .format(parent_name, args))

    start_str = parts[0]
    end_str = parts[1]
    loop_str = parts[2]

    """
    i = 0 #start
    while i < N: #end
        i += 1 #loop
    """

    start_pairs_full = parse.parse_key_values(start_str, parent_name, sep="=", num=1)
    loop_pairs_full = parse.parse_key_values(loop_str, parent_name, sep="=", num=1)

    start_pairs = start_pairs_full[0]
    loop_pairs = loop_pairs_full[0]

    i = start_pairs[0]
    j = loop_pairs[0]

    if len(start_pairs) > 1:
        variables[i] = parse.parse_maths_string(start_pairs[1], parent_name, variables)

    cont = True
    while cont:
        check = parse.parse_maths_string(end_str, parent_name, variables)
        
        if not check:
            cont = False
        else:
            # MAIN BODY
            for child in children:
                result = child.objectify(variables, parent_name + ">")
                output.append(result[0])

            # end main body

            if len(loop_pairs) > 1:
                variables[j] = parse.parse_maths_string(loop_pairs[1], parent_name, variables)


    #print(output)
    return output




######################

####
####   Parse specific objects
####


def parse_vector(strings:list, parent_name:str, variables:dict):
    """
    Given a string representation of a vector parse it.
    """
    if len(strings) != 1:
        param_error(parent_name, strings, 1)
    string = strings[0]

    key_values = parse.parse_key_values(string, parent_name)
    
    if len(key_values) != 1:
        raise ValueError("\nFile Trace: {0}\nInvalid number of Vector attributes: {1}"\
                         .format(parent_name, string))
    else:
        name = key_values[0][0]
        value = key_values[0][1]
        
        string_ls = value.split(",")
        n = len(string_ls)
    
        vec = [0] * n
        i = 0
        while i < n:
            sub_str = string_ls[i]
        
            if sub_str == '':
                raise ValueError("\nStack Trace: {0}\nCannot Make vector of zero length."\
                                 .format(parent_name))
            else:
                tmp = parse.parse_maths_string(sub_str, parent_name, variables)
                if tmp == None:
                    raise ValueError("\nStack Trace: {0}\nMissing vector component.\n '{1}'"\
                                    .format(string))
                else:
                    vec[i] = tmp
            i += 1
                
        if name == "" or name == cart_str:
            return vector.Vector(vec)
        elif name == polar_str:
            radius = vec[0]
            angles = vec[1:len(vec)]
            return vector.Vector.polar_vector(radius, angles)
        else:
            raise NameError("\nStack Trace: {0}\nUnknown keyword '{1}'."\
                            .format(parent_name, name))




def parse_colour(strings:list, parent_name:str, variables:dict):
    """
    Parse string representation of a colour.
        
    If No value is given, raise ValueError
    """
    if len(strings) != 1:
        param_error(parent_name, strings, 1)
    string = strings[0]

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
            tmp = parse.parse_maths_string(cols[i], parent_name, variables)
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





def parse_constants(strings:list, parent_name:str, variables:dict):
    
    if len(strings) != 1:
        param_error(parent_name, strings, 1)
    string = strings[0]


    key_values = parse.parse_key_values(string, parent_name)
    consts = constants.Constants()

    for pair in key_values:
        name = pair[0]
        value = pair[1]
        my_name = parent_name + ">" + name

        if name == g_str:
            tmp = parse.parse_maths_string(value, my_name, variables)
            if tmp != None:
                consts.G = tmp
        elif name == e_str:
            tmp = parse.parse_maths_string(value, my_name,variables)
            if tmp != None:
                consts.E = tmp
        elif name == R_str:
            tmp = parse.parse_maths_string(value, my_name, variables)
            if tmp != None:
                consts.R = tmp
        
        elif name == dist_err_str:
            tmp = parse.parse_maths_string(value, my_name, variables)
            if tmp != None:
                consts.distance_error = tmp
        
        elif name == t_del_str:
            tmp = parse.parse_maths_string(value, my_name, variables)
            if tmp != None:
                consts.time_delay = int(tmp)
        elif name == update_num_str:
            tmp = parse.parse_maths_string(value, my_name, variables)
            if tmp != None:
                consts.update_number = int(tmp)
        elif name == time_step_str:
            tmp = parse.parse_maths_string(value, my_name, variables)
            if tmp != None:
                consts.time_step = tmp

        elif name == max_dist_str:
            tmp = parse.parse_maths_string(value, my_name, variables)
            if tmp != None:
                consts.max_dist = tmp

        elif name == warning_str:
            if value != "":
                b = get_bool(value, my_name)
                consts.warning = b
                consts.warning_possible = b
    

        else:
            raise NameError("\nStack Trace: {0}\nUnknown keyword '{1}'"\
                           .format(parent_name, name))

    return consts






def parse_universe(strings:list, children_obj, parent_name:str, variables:dict):
    """
    Given a string that represents a universe object, and it's children objects,
    return a universe object.
    """
    if len(strings) != 1:
        param_error(parent_name, strings, 1)
    string = strings[0]

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
    
    max_speed = -1
    relativistic = False
    
    disp_trail = False
    
    nlaw = 2
    nmetric = 2

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

        elif keyword == max_v_str:
            tmp = parse.parse_maths_string(value, my_name, variables)
            if tmp != None:
                max_speed = tmp
        elif keyword == relat_str:
            relativistic = True
            if value != "":
                relativistic = get_bool(value, my_name)
        
        elif keyword == trail_str:
            disp_trail = True
            if value != "":
                disp_trail = get_bool(value, my_name)
    
        elif keyword == nlaw_str:
            tmp = parse.parse_maths_string(value, my_name, variables)
            if tmp != None:
                nlaw = tmp
        elif keyword == nmetric_str:
            tmp = parse.parse_maths_string(value, my_name, variables)
            if tmp != None:
                nmetric = tmp

        else:
            raise NameError("\nStack Trace: {0}\nUnknown keyword '{1}'"\
                           .format(parent_name, keyword))

    if centre == None:
        centre = vector.Vector.zero_vector(dim)

    uni = universe.Universe(centre, *bodies)
    uni.resistance = resistance
    uni.conserve_energy = energy_consv

    uni.relativistic = relativistic
    uni.max_speed = max_speed

    uni.display_trails = disp_trail

    uni._nlaw = nlaw
    uni._nmetric = nmetric
    return uni







def parse_body(strings:list, child_obj:list, parent_name:str, variables:dict):
    """
    Given a string that represents a body object, and it's children objects, 
    return a body object.
    """
    
    if len(strings) != 1:
        param_error(parent_name, strings, 1)
    string = strings[0]
    
    key_values = parse.parse_key_values(string, parent_name)
    #print("Body objects:", child_obj)
    X = None
    V = None
    
    mass = 0
    charge = 0
    radius = 0
    col = colour.black
    name = ""
    
    trail_col = colour.white
    max_trail = 0
    skip_num = 0
    
    anchor = False
    elasticity = 1
    collide = False
    
    for pair in key_values:
        keyword = pair[0]
        value = pair[1]
        
        key_name = parent_name + ">" + keyword
    
        if keyword == x_str:
            X = get_vector_key_value(value, child_obj, key_name)
    
        elif keyword == v_str:
            V = get_vector_key_value(value, child_obj, key_name)
        
        elif keyword == m_str:
            tmp = parse.parse_maths_string(value, key_name, variables)
            if tmp != None:
                mass = tmp

        elif keyword == q_str:
            tmp = parse.parse_maths_string(value, key_name, variables)
            if tmp != None:
                charge = tmp

        elif keyword == r_str:
            tmp = parse.parse_maths_string(value, key_name, variables)
            if tmp != None:
                radius = tmp

        elif keyword == name_str:
            name = value

        elif keyword == col_str:
            col = get_colour_key_value(value, child_obj, key_name)
        
        elif keyword == anch_str:
            anchor = True
            if value != "":
                anchor = get_bool(value, parent_name)
        
        elif keyword == collide_str:
            collide = True
            if value != "":
                collide = get_bool(value, parent_name)
        elif keyword == elast_str:
            tmp = parse.parse_maths_string(value, key_name, variables)
            if tmp != None:
                elasticity = tmp
    
        elif keyword == trail_col_str:
            trail_col = get_colour_key_value(value, child_obj, key_name)
        elif keyword == skip_str:
            tmp = parse.parse_maths_string(value, key_name, variables)
            if tmp != None:
                skip_num = int(tmp)
        elif keyword == max_trail_str:
            tmp = parse.parse_maths_string(value, key_name, variables)
            if tmp != None:
                max_trail = int(tmp)
    
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
    b = body.Body(id,X, V, mass, radius, charge, col, name)

    # final adjustments
    if anchor:
        b.toggle_anchor()
    
    b.can_collide = collide
    b.elasticity = elasticity

    b.trail_history.max_num = max_trail
    b.trail_history.colour = trail_col
    b.trail_history.skip_num = skip_num

    #print(b.trail_history, name, b.trail_history.max_num)
    return b





def parse_screen(strings:list, child_obj:list, parent_name, variables:dict):
    """
    Given a string that represents a screen object, and a set of the subchildren,
    return the screen object.
    """
    
    if len(strings) != 1:
        param_error(parent_name, strings, 1)
    string = strings[0]


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
            tmp = parse.parse_maths_string(value, my_name, variables)
            if tmp != None:
                width = int( tmp )
        
        elif name == h_str:
            tmp = parse.parse_maths_string(value, my_name, variables)
            if tmp != None:
                height = int( tmp )

        elif name == scl_str:
            tmp = parse.parse_maths_string(value,my_name, variables)
            if tmp != None:
                scale = tmp

        elif name == back_str:
            screen_col = get_colour_key_value(value, child_obj, my_name)
        elif name == txt_col_str:
            text_col = get_colour_key_value(value, child_obj, my_name)

        elif name == default_msg:
            msg = value

        elif name == title_size_str:
            tmp = parse.parse_maths_string(value, my_name, variables)
            if tmp != None:
                title_size = int( tmp )
        elif name == label_size_str:
            tmp = parse.parse_maths_string(value, my_name, variables)
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
        raise SyntaxError("\nStack Trace: {0}\nIncorrectly parsed Vector string '{1}'"\
                            .format(parent_name, value))

    pos = value.lstrip('#')
    pos_int = int(pos)
                              
    sub_obj = ls[pos_int]
    if not isinstance(sub_obj, vector.Vector):
        raise TypeError("\nStack Trace: {0}\nVector subvalue is non-vector, type: '{1}'\n '{2}'"\
                        .format(parent_name, type(sub_obj), sub_obj))
    else:
        return sub_obj



def get_colour_key_value(value:str, ls:list, parent_name:str):
    err = False
    if len(value) < 2:
        err = True
    elif value[0] != '#':
        err = True
    if err:
        raise SyntaxError("\nStack Trace: {0}\nIncorrectly parsed Colour string '{1}'"\
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





def param_error(parent_name:str, params:list, max_params):
    raise SyntaxError("\nStack Trace: {0}\nInvalid number of variables, '{1}'\n Maximum is {2}."\
                      .format(parent_name, params, max_params))
