from modules.parser import special_parsers as pars

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
dist_err_str = "distanceError"
t_del_str = "timeDelay"
update_num_str = "UpdateNumber"
time_step_str = "timeStep"


# universe
dim_str = "dimension"
centre_str = "centre"
rest_str = "resistance"
energy_consv_st = "conserveEnergy"


# body
x_str = "X"
v_str = "V"
m_str = "mass"
q_str = "charge"
r_str = "radius"
name_str = "name"



# screen

w_str = "width"
h_str = "height"
scl_str = "scale"
back_str = "background"




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
            raise ValueError("\nFile Trace:: {0}\n Cannot Make vector of zero length.".format(parent_name))
        else:
            vec[i] = pars.float_maths_parse(sub_str, parent_name)
        
        i += 1
    
    return vector.Vector(vec)




def parse_colour(string:str, parent_name:str):
    """
        Parse string representation of a colour.
        
        If No value is given, raise ValueError
        """
    colours = pars.parse_key_values(string)
    
    if len(colours) != 1:
        raise ValueError("\nFile Trace: {0}\nInvalid number of colour attributes: {1}".format(parent_name, string))
    else:
        pass
    return





def parse_constants(string:str, parent_name:str):
    key_values = pars.parse_key_values(string)
    return



def parse_universe(string:str, children_obj, parent_name:str):
    key_values = pars.parse_key_values(string)
    return





