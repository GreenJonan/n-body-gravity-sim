#import body, colour, constants, draw, universe, vector
from modules import body, colour, draw, universe, vector, constants
from modules.parser import objects, special_parsers as pars

import sys

directory = "systems/"
extension = ".sys"

"""
keywords:
    file
    constants
    universe
    body
    vector
    colour
    screen
"""


# keywords

file_str = "root"
const_str = "constants"
uni_str = "universe"
body_str = "body"
vect_str = "vector"
screen_str = "screen"
col_str = "colour"











######## main parser.


class ParseTree:
    def __init__(self, file_name:str, string:str="", name:str=""):
        self.children = []
        self.string = string
        self.name = name
        self.parent = None
        self.fileName = file_name
    

    def add_child(self, string="", name=""):
        new_parse = ParseTree(self.fileName, string,name)
        new_parse.parent = self
        self.children.append(new_parse)
        return new_parse


    ####

    def get_child_objects(self, parent_name) -> list:
        """
        Suppose self is already parsed. Extract the key data and objects. Return list of objects in self.
        
        Get the object form of the children.
        """
        N = len(self.children)
        ls = [None] * N
    
        i = 0
        while i < N:
            tmp_ls = self.children[i].objectify(parent_name)
            if len(tmp_ls) > 1:
                # there is no reason the lists shouldn't be length 1
                raise ValueError("\nStack Trace: {0}\nIncorrectly objectified child objects. '{1}'"\
                                 .format(parent_name, tmp_ls))
            
            ls[i] = tmp_ls[0]
            i += 1
        return ls
    
    
    
    def objectify(self, parent_name=">") ->list:
        """
        Turn self into an object.
        """
        
        my_name = parent_name + self.name
        child_objects = self.get_child_objects(my_name + ">")
        #print(parent_name, my_name)
        
        
        if self.name == file_str:
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
    
    
        elif self.name == uni_str:
            return [ objects.parse_universe(self.string, child_objects, my_name) ]
                
        elif self.name == body_str:
            return [ objects.parse_body(self.string, child_objects, my_name) ]

        elif self.name == const_str:
            return [objects.parse_constants(self.string, my_name)]
            # parse constants

        elif self.name == vect_str:
            return [ objects.parse_vector(self.string, my_name) ]

        elif self.name == screen_str:
            return [ objects.parse_screen(self.string, child_objects, my_name) ]
            # parse screen object
                
        elif self.name == col_str:
            return [ objects.parse_colour(self.string, my_name) ]
                
        else:
            raise TypeError("\nStack Trace: {0}\nUnknown Object type '{1}' in system file: {2}"\
                            .format(parent_name, self.name, self.fileName))
    




    def __repr__(self):
        string = ""
        string += self.name + ": " + self.string + '\n\n'
        
        for child in self.children:
            string += str(child)
        return string











def parse_file_section(f, parse_root:ParseTree):
    """
    If f is a file object and parse_root is a parse tree.
        
    Open new parse tree with name {}
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
    parsed_num = 0
    expect_sub_object = False
    
    cont = True
    while cont:
        c = f.read(1)
        if c == "":
            cont = False
            raise SyntaxError("Invalid formatting of file. Require '}}' to close object type '{0}'."\
                            .format(parse_root.name))
        else:
            # read file char
            #print(":", c)
            
            # comment parser
            if c == '[':
                print("HERERERE")
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
                if c == '\n':
                    c = pars.line_break
            
                if c == '}':
                    cont = False
                elif c == '{':
                    if expect_object:
                        string += "#" + str(parsed_num)
                        expect_object = False
                
                    child_parse = parse_root.add_child(name=prev_word)
                
                    parse_file_section(f, child_parse)
                    prev_word = ""
                    parsed_num += 1
            
                elif c == pars.line_break:
                    string = add_word(string, prev_word)
                    prev_word = ""
                    string += pars.line_break
                    expect_object = False
            
                elif pars.is_white_space(c):
                    new_word = True

                elif c == ':':
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


    if len(prev_word) > 0:
        string = add_word(string, prev_word)

    parse_root.string = string
    #print("string:", string)
    return









def parse_file(f, file_name):
    """
    Given a file, read the contents and output the result as a ParseTree.
    """
    
    root = ParseTree(file_name, name="root")
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


