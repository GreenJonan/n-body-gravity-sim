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


def float_maths_parse(string:str, parent_name:str):
    val = 0.0
    try:
        val = float(string)
    except ValueError:
        raise ValueError("\nFile Trace: {0}\nCannot connvert non-numeric string '{1}' into float expression.".format(parent_name, string))
    return val



