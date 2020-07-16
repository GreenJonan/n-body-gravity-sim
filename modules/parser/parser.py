from modules.parser import objects
from modules.parser import special_parsers as pars
#import objects, special_parsers as pars

#from .. import body, colour, constants, draw, universe, vector
from modules import body
from modules import colour
from modules import draw
from modules import universe
from modules import vector
from modules import constants

import math
import sys

directory = "systems/"
extension = ".sys"


keyname_char = '`'

"""
keywords:
    file
    variables
    constants
    universe
    body
    vector
    colour
    screen
"""


# keywords

file_str = "root"
var_str = "variables"
const_str = "constants"
uni_str = "universe"
body_str = "body"
vect_str = "vector"
screen_str = "screen"
col_str = "colour"

for_str = "for"  # this is a for loop



def is_keyword(string:str):
    if string == for_str:
        return True
    else:
        return False



def is_variable_object(string:str):
    if string == vect_str:
        return True
    elif string == col_str:
        return True
    else:
        return False




default_variables = {"pi":math.pi, "au":1.496e11}







######## main parser.


class ParseTree:
    def __init__(self, file_name:str, strings, name:str=""):
        self.children = []
        self.strings = strings
        self.name = name
        self.parent = None
        self.fileName = file_name
    

    def add_child(self, strings, name=""):
        new_parse = ParseTree(self.fileName, strings, name)
        new_parse.parent = self
        self.children.append(new_parse)
        return new_parse
    
    
    def child_num(self):
        return len(self.children)


    ####

    def get_child_objects(self, parent_name, variables) -> list:
        """
        Suppose self is already parsed. Extract the key data and objects. Return list of objects in self.
        
        Get the object form of the children.
        """
        N = len(self.children)
        ls = [None] * N
    
        i = 0
        while i < N:
            tmp_ls = self.children[i].objectify(variables, parent_name)
            
            n = len(tmp_ls)
            if n == 0:
                raise ValueError("\nStack Trace: {0}\nIncorrectly objectified child objects.\n '{1}'"\
                                 .format(parent_name, tmp_ls))
            
            j = 1
            while j < n:
                ls.append(tmp_ls[j])
                j += 1
            ls[i] = tmp_ls[0]
            i += 1
        return ls
    
    
    
    def objectify(self, variables, parent_name=">") ->list:
        """
        Turn self into an object.
        """
        
        my_name = parent_name + self.name
        name = self.name
        
        if name == for_str:
            return objects.parse_forloop(self.strings, my_name, self.children, variables)
        
        
        child_objects = self.get_child_objects(my_name + ">", variables)
        #print(parent_name, my_name)

        if name == file_str:
            # return child objects, need constants, one universe, one screen to project.
            results = [None] * 3
            i = 0
            while i < len(child_objects):
                obj = child_objects[i]
                if isinstance(obj, constants.Constants):
                    results[0] = obj
                elif isinstance(obj, universe.Universe):
                    results[1] = obj
                elif isinstance(obj, draw.UniverseScreen):
                    results[2] = obj
                else:
                    pass #print("Ignoring:", obj)
                i += 1
            return results
        
        
        elif name == var_str:
            return [ objects.parse_variables(self.strings, my_name, child_objects, variables) ]
    
        elif name == uni_str:
            return [ objects.parse_universe(self.strings, child_objects, my_name, variables) ]
                
        elif name == body_str:
            return [ objects.parse_body(self.strings, child_objects, my_name, variables) ]

        elif name == const_str:
            return [objects.parse_constants(self.strings, my_name, variables)]
            # parse constants

        elif name == vect_str:
            return [ objects.parse_vector(self.strings, my_name, variables) ]

        elif name == screen_str:
            return [ objects.parse_screen(self.strings, child_objects, my_name, variables) ]
            # parse screen object
                
        elif name == col_str:
            return [ objects.parse_colour(self.strings, my_name, variables) ]
    
        else:
            raise TypeError("\nStack Trace: {0}\nUnknown Object type '{1}'\n in system file: {2}"\
                            .format(parent_name, self.name, self.fileName))
    




    def __repr__(self):
        tmp_string = ""
        string = ""
        
        n = len(self.strings)
        if n == 0:
            pass
        elif n == 1:
            tmp_string = self.strings[0]
        else:
            tmp_string = str(self.strings)
        
        string += self.name + ": " + tmp_string + '\n\n'

        for child in self.children:
            string += str(child)
        return string










def parse_file_section(f, parse_root:ParseTree):  #object_name=""):
    """
    f is a file object and parse_root is a parse tree.
        
    Open new parse tree with,  name {arg1}{arg2}...
    Comment out sections with []
    """
    
    
    def add_word(string, word):
        #print("Previous word:", word)
        new_string = ""
        if len(string) == 0:
            new_string = word
        else:
            last_char = string[-1]
            
            if last_char == pars.line_break or last_char == ':' or last_char == ' ':
                new_string = string + word
            else:
                # add space only if there exists previous non-grammar characters
                new_string = string + " " + word
        
        return new_string
    
    string = ""
    prev_word = ""
    new_word = True
    
    expect_object = False
    #parsed_num = 0
    expect_sub_object = False
    
    arg_search = False
    #keywords = []
    
    child = None
    
    cont = True
    while cont:
        #print("Parse:",parse_root)
        
        c = f.read(1)
        if c == "":
            cont = False
            raise SyntaxError("\nInvalid formatting of file.\nRequire '}}' to close object type '{0}'."\
                            .format(parse_root.name))
        else:
            # read file char
            #print(":", c)
            
            # comment parser
            if c == '[':
                #comment while open > 0, all closed means no longer comment.
                open_coms = 1
                
                #comment = ""
                while open_coms > 0 and cont:
                    c = f.read(1)
                    if c == "":
                        cont = False
                    else:
                        if c == ']':
                            open_coms -= 1
                        elif c == '[':
                            open_coms += 1
                        
                        #if open_coms != 0:
                        #    comment += c
                #print("Comment:", comment)
        
            else:
                
                if c == '{':
                    
                    if expect_object:
                        string += "#" + str(parse_root.child_num())
                        expect_object = False
                    
                    if not arg_search:
                        new_strings = []
                        child = parse_root.add_child(new_strings, name=prev_word)
                        # the empty string is needed otherwise the function will keep adding strings to
                        # old lists higher up in the heireichy and other places!
                        prev_word = ""
                    
                    arg_search = True
                
                    name = prev_word
                    parse_file_section(f, child)

            
                elif c == ' ' and arg_search:
                    pass  #allows for separation between arguments func {} {}
                
                else:
                    
                    if arg_search:
                        # end the search for the arguments and append all objects.
                        prev_word = ""
                        #parsed_num += 1
                        arg_search = False
                        child = None
                    
                    else:
                        pass #nothing to add
                    
                    if c == '\n':
                        c = pars.line_break

                    if pars.is_white_space(c):
                        new_word = True

                    else:
                        if c == '}':
                            cont = False
                
                        elif c == pars.line_break:
                            string = add_word(string, prev_word)
                            prev_word = ""
                            string += pars.line_break
                            expect_object = False

                        elif c == ':' or c == '=':
                            #add prev word to string, and set up key-value pair
                            string = add_word(string, prev_word)
                            string += c
                
                            expect_object = True
                            prev_word = ""

        
                        else:
                            if new_word:
                                # add previous word to parse string,
                                string = add_word(string, prev_word)
                                prev_word = ""
                                new_word = False
                            prev_word += c

    if arg_search:
        raise SyntaxError("\nNo closing brace for Object argument.\n Object: {0}\n String: {1}"\
                          .format(parse_root.name, string))


    string = add_word(string, prev_word)

    """
    parse_root.strings.append(string)
    print("string:", string)
    print(parse_root.strings, parse_root.name)
    print()
    print()
    """
    parse_root.strings.append(string)
    return parse_root








def parse_file(f, file_name):
    """
    Given a file, read the contents and output the result as a ParseTree.
    """
    
    sub_strings = []
    root = ParseTree(file_name, sub_strings, name="root")
    prev_word = ""
    new_word = True
    
    cont = True
    string = ""
    while cont:
        c = f.read(1)
        if c == "":
            cont = False
        else:
            # interpret character
            if c == '{':
                if prev_word == file_str:
                    parse_file_section(f, root)
                prev_word = ""
            
            elif c == '}':
                pass
            
            elif pars.is_white_space(c):
                new_word = True
            
            else:
                if new_word:
                    new_word = False
                    prev_word = str(c)
                else:
                    prev_word += c

    return root







"""
def parse_file(f):
    ###
    Let f be a file object. Read this file and return the contents as a tree.
    ###

    line = ""
    prev_str = ""

    open = 0
    closed = 0
    
    parse_tree_root = ParseTree()
    
    
    cont = True
    while cont:
        line = f.readline()
        if line == "":
            cont = False
        else:
            line_str = line.strip()
            
            n = len(line_str)
            i = 0
            
            
            while i < n:
                c = line_str[i]
                if c == '{':
                    pass # open parsing function
                    name = prev_str
                
                
                elif c == '}':
                    pass #close parsing function
                
                elif c == '}':
                    pass # find value
                
                elif c == " " or c =="\t" or c =="\n":
                    pass # next character is next word
                
                i += 1
"""


