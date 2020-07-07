# key line commands
"""
Made is such that when the input file is parsed, ALL NEW LINE ('\n') characters are replaced
with line break characters.
"""

line_break = ";" # other option is '\n', but then need to change all of parse_file_section function.





def is_white_space(c:str):
    if len(c) == 0:
        pass
    else:
        if c == " " or c == "\n" or c == "\t" or c == "　":
            return True
        else:
            pass
    return False





#####
#####   Transform keyword, value pairs into tuples.


def parse_key_values(string:str):
    """
    Parse a:b into (a,b). Each section
    """
    output = []
    #print(string)
    #print("Nothing has caused me to reset the value parameter!")
    # dont worry I fixed it such that new lines ('\n') are replaced with ';'
    
    name = ""
    value = ""
    word = ""
    
    c = ""
    
    has_char = False
    new_word = False
    
    
    N = len(string)
    i = 0
    #print(string, N)
    while i <= N:
        if i == N:
            if c != line_break:
                c = line_break
            else: break
        else:
            c = string[i]
        
        if c == ":":
            name = word
            word = ""
            key = False
            has_char = False
        #new_word = True   # no need, already set 'word' to empty string
        
        elif c == line_break:
            value = word
            if len(name) > 0 or len(value) > 0:
                output.append((name, value))
            name = ""
            value = ""
            word = ""
            has_char = False
        #new_word = True
        
        elif is_white_space(c):
            new_word = True
        
        else:
            if new_word:
                new_word = False
                if has_char:
                    word += " "
            word += c
            has_char = True
        
        #print("here:", i)
        i += 1
    
    
    print(output)
    return output





####   Maths parser
####


"""
Mathematical Operations:
 
  +  addition
  -  subtraction
  *  multiplication
  /  division
  ^  power
"""



class MathTree:
    def __init__(self, val):
        self.value = None
        self.left_child = None
        self.right_child = None
        self.function = None

    """
    def add(self):
        return self.left_child.value + self.right_child.value  # x + y

    def sub(self):
        return self.left_child.value - self.right_child.value  # x - y

    def mult(self):
        return self.left_child.value * self.right_child.value  # x * y

    def div(self):
        return self.left_child.value / self.right_child.value  # x / y

    def pow(self):
        return self.left_child.value ** self.right_child.value # x ** y
    """
    
    @staticmethod
    def add(x,y):
        return x+y
    @staticmethod
    def sub(x,y):
        return x-y
    @staticmethod
    def mult(x,y):
        return x*y
    @staticmethod
    def div(x,y):
        return x/y
    @staticmethod
    def pow(x,y):
        return x**y

    def identity(self):
        return self.value


    def get_tree_value(self):
        left_none = self.left_child == None
        right_none = self.right_child == None
        is_leaf = is_leaf and right_none
        if is_leaf:
            return self.identity()
        elif left_none or right_none:
            raise ValueError("MathTree Parser incorrectly constructed,\
                             comparing None type with non-None type.")
        
        else:
            x = self.left_child.get_tree_value()
            y = self.right_child.get_tree_value()
        
            return self.function(x,y)



    def construct_tree(string:str, parent_name:str):
        n = len(string)

        i = 0
        while i < n:

            i += 1




def float_maths_parse(string:str, parent_name:str):
    subvalues = []
    
    # first re-format string to
    val = 0.0
    try:
        val = float(string)
    except ValueError:
        raise ValueError("\nFile Trace: {0}\nCannot connvert non-numeric string '{1}' into float expression."\
                         .format(parent_name, string))
    return val



