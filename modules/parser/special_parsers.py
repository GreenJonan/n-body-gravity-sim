# key line commands
"""
Made is such that when the input file is parsed, ALL NEW LINE ('\n') characters are replaced
with line break characters.
"""

"""
Specific variables specified in the variables section of the .sys files (NOT IMPLEMENTED), or default values,
such as pi, can be used to evaluate numeric expressions in the maths parser.
"""


line_break = ';' # other option is '\n', but then need to change all of parse_file_section function.
exponent = 'e'
verbatim = '"'



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


def parse_key_values(string:str, parent_name:str, sep=':', num = -1):
    """
    Parse a:b into (a,b). Each section
    """
    output = []
    # dont worry I fixed it such that new lines ('\n') are replaced with ';'
    
    def add_pair(ls, name, val):
        if len(name) > 0 or len(val) > 0:
            ls.append((name, val))
        return "",""
    
    name = ""
    value = ""
    word = ""
    
    c = ""
    
    has_char = False
    new_word = False
    
    seen_keyword = False
    seps = 0
    
    N = len(string)
    i = 0
    
    while i <= N:
        if i == N:
            if c != line_break:
                c = line_break
            else: break
        else:
            c = string[i]
        """
        if c == ')':
            raise SyntaxError("\nStack Trace: {0}\nNo opening bracket exists, '{1}'"\
                              .format(parent_name, string))
        elif c == '(':
            ######
            # add phrase verbatim
            if new_word:
                new_word = False
                if has_char:
                    word += " "
            open_num = 0 #number of open brackets
            cont = True
            j = i
            while cont:
                if j == N:
                    cont = False
                else:
                    c = string[j]
                    if c == ')':
                        open_num -= 1
                    elif c == '(':
                        open_num += 1
                    else:
                        word += c
                
                    if open_num <= 0:
                        cont = False
                    else:
                        j += 1

            if j == N:
                raise SyntaxError("\nStack Trace: {0}\nFinal closing bracket does not exist, '{1}'"\
                                  .format(parent_name, string))
            else:
                pass #i -= 1 # compensate for += 1 later
            
            if i+1 < j:
                has_char = True
            i = j
            ######
        """
        if c == verbatim:
            # acts as verbatim string
            
            # add phrase verbatim
            if new_word:
                new_word = False
                if has_char:
                    word += " "
            
            cont = True
            j = i+1
            while cont:
                if j == N:
                    cont = False
                else:
                    c = string[j]
                    if c == verbatim:
                        cont = False
                    else:
                        word += c
                        j += 1
            
            if j == N:
                raise SyntaxError("\nStack Trace: {0}\nClosing quote character does not exist, '{1}'"\
                                  .format(parent_name, string))
            else:
                pass
                    
            if i+1 < j:
                has_char = True
                i = j
        
        elif c == sep:
            if seen_keyword and num < 0:
                ######
                # find beggining and end part of the string
                j = i
                d = string[j]
                while j >= 0 and d != ';':
                    j -= 1
                    if j >= 0:
                        d = string[j]
                beggining = j + 1
                
                j = i
                e = string[j]
                while j < N and e != ';':
                    j += 1
                    if j < N:
                        e = string[j]
                ending = j
                
                raise SyntaxError("\nStack Trace: {0}\nInvalid use of keyword value pairs. Cannot place multiple 'keyword:value' instances within one code section.\n'{1}'"\
                                  .format(parent_name, string[beggining:ending]))
                ######
                
            
            
            if num < 0 or (seps < num):
                seen_keyword = True
                name = word
                word = ""
                key = False
                has_char = False
                #new_word = True   # no need, already set 'word' to empty string
            else:
                word += c
            seps += 1
        
        elif c == line_break:
            value = word
            name, value = add_pair(output, name, value)
            word = ""
            has_char = False
            seen_keyword = False  #reset keyword searching
        
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
    
    
    #print("output:",output)
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


def maths_2func(c:str):
    if c == '+':
        return True
    elif c == '-':
        return True
    elif c == '*':
        return True
    elif c == '/':
        return True
    elif c == '^':
        return True
    elif c == '<':
        return True
    elif c == '>':
        return True
    else:
        return False


def maths_1func(c:str):
    if maths_1left_func(c):
        return True
    else:
        return maths_1right_func(c)


def maths_1left_func(c:str):
    if c == '-':
        return True
    elif c == '+':
        return True
    elif c == '~':
        return True
    else:
        return False


def maths_1right_func(c:str):
    if c == '!':
        return True
    else:
        return False


def maths_syntax(c:str):
    if c == '(':
        return True
    elif c == ')':
        return True
    elif c == '=':
        return True
    elif maths_2func(c):
        return True
    else:
        return maths_1func(c)






class MathList:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_elem(self, val):
        new_node = LinearNode(val)
        if self.head == None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        return new_node

    def __repr__(self):
        string = ""
        if self.head != None:
            string += "("
            p = self.head
            while p != None:
                if p == self.head:
                    pass
                else:
                    string += " "
                string += str(p.value)
                p = p.next

            string += ")"
        return string
    
    
    def __len__(self):
        length = 0
        p = self.head
        while p != None:
            length += 1
            p = p.next
        return length


    @staticmethod
    def get_maths_list(string:str, parent_name:str):
        """
        Given a string, decompose it into sub units strings of operands and parameters
        """
        parse = MathList()
        param_word = True
        prev_char = ''
        
        n = len(string)

        has_char = False
        word_added = False
        
        #print()
        #print("Decompose:", string)

        i = 0
        word_start = i
        word_end = i
        
        while i < n:
            c = string[i]
            #print(":",c, string[word_start:word_end])
            
            if maths_syntax(c):
                if c == ')':
                    raise SyntaxError("\nStack Trace: {0}\nClose bracket has no opening bracket in '{1}'"\
                                      .format(parent_name, string))
                elif c == '(':
                    if word_start != word_end:
                        if param_word:
                            raise SyntaxError("\nStack Trace: {0}\nUndefined function between two numbers: '{1}'"\
                                              .format(parent_name, string))
                        else:
                            # add function
                            #print("Adding operand:",string[word_start:word_end])
                            new_str = string[word_start:word_end]
                            parse.add_elem(new_str)
                
                    params = False
                    #next element cannot be params!
                    
                    # Read opening bracket sub-syntax
                    open_brac_num = 1
                    j = i+1
                    while open_brac_num > 0 and j < n:
                        c = string[j]
                        if c == ')':
                            open_brac_num -= 1
                        else:
                            if c == '(':
                                open_brac_num += 1
                        if open_brac_num != 0:
                            j += 1
        
                    if j == n:
                        raise SyntaxError("\nStack Trace: {0}\nNo closing bracket for '{1}'"\
                                          .format(parent_name, string))
                    else:
                        new_string = string[i+1:j]
                        sub_list = MathList.get_maths_list(new_string, parent_name)
                        parse.add_elem(sub_list)
                        i = j
                    
                    word_start = i+1
                    word_end = word_start
                    word_added = True

                    has_char = True
                    param_word = False
                
                else:
                    has_char = True # allows for -() syntax
                    
                    if prev_char == exponent and (c =='+' or c == '-'):
                        word_end += 1
                    else:
                        if (c == '-' or c =='+')\
                            and (prev_char == '*' or prev_char == '/' or prev_char == '^'):
                            # allows for x*-y syntax
                            param_word = True
                    
                        if param_word:
                            #print("Adding parametre:",string[word_start:word_end])
                            if word_start == word_end:
                                pass # don't add empty/non-parameter
                            else:
                                new_str = string[word_start:word_end]
                                parse.add_elem(new_str)
                        
                            param_word = False
                            word_start = i
                            word_end = word_start + 1
                        else:
                            word_end = i + 1

            else:
                """
                if is_white_space(c) and word_start == i:
                    # if word is set to start at i, but i is a white space, they move to next character
                    word_start += 1
                    print("here")
                else:
                    print("there")
                    if not param_word:
                        new_str = string[word_start:i]
                        parse.add_elem(new_str)
                    
                        param_word = True
                        word_start = i
            
                    if not is_white_space(c):
                        has_char = True
                """
                if is_white_space(c):
                    # if is white space add previous word
                    if word_start != word_end:
                        #print("string:",string[word_start:word_end])
                        """
                        # add previous word
                        new_str = string[word_start:word_end]
                        parse.add_elem(new_str)
                        word_start = i+1
                        word_end = word_start
                        word_added = True
                        """
                        pass
                    else:
                        # move to next character, since white space
                        word_start += 1
                        word_end = word_start
                    #print("here")
                else:
                    has_char = True
                    
                    if not param_word:
                        #print("Adding operand:",string[word_start:word_end])
                        if word_start == word_end:
                            pass
                        else:
                            new_str = string[word_start:word_end]
                            parse.add_elem(new_str)
                        
                        param_word = True
                        word_start = i
                        word_end = word_start + 1
                        word_added = False
                    else:
                        word_end = i + 1
                    
                    

            i += 1
            prev_char = c
    
        if word_start != word_end:
            new_str = string[word_start:word_end]
            #print("new_str:",new_str)
            parse.add_elem(new_str)
        
        #print("P",parse, ":",string)
        return parse


    def construct_tree(self, parent_name:str):
        """
        Suppose 'self' is a correctly constructed parse maths list.
        Return a list
        
        Order of operations, (),^,*,/,+,-
        """
        #print()
        #print("Constructing tree1:",self, len(self))

        # helper function
        def construct_tree_subset(pointer, end_pointer=None, parent_name:str=""):
            
            # subhelper function
            def error_string(pointer, end):
                value_str = "'"+str(pointer.value)+"'"
                full_str = ""
                pointer = pointer.next
                cont = True
                while cont:
                    if pointer == end:
                        value_str = full_str
                    
                    if pointer == None:
                        cont = False
                    else:
                        full_str += " " + "'" + str(pointer.value) + "'"
                        pointer = pointer.next
                return value_str, full_str
        
            
            if pointer == None:
                raise TypeError("Error parsing Maths String: {0}".format(parent_name))
            
            elif pointer.next == end_pointer:
                val = pointer.value
                if isinstance(val, MathList):
                    sub_output = val.construct_tree(parent_name)
                    if len(sub_output) == 1:
                        return sub_output[0]
                    else:
                        return sub_output
                else:
                    return pointer.value

            elif pointer.next != None:
                if pointer.next.next == end_pointer:
                    #unary operation
                    left = None
                    right = None
                    
                    if isinstance(pointer.value, str):
                        left = pointer.value
                    else:
                        left = construct_tree_subset(pointer, pointer.next, parent_name)
                    if isinstance(pointer.next.value, str):
                        right = pointer.next.value
                    else:
                        right = construct_tree_subset(pointer.next, end_pointer, parent_name)
                    
                    return [left, right]
                    
            """
            # see if the first pointer is a lefthand function.
            if isinstance(pointer.value, str):
                if maths_1left_func(pointer.value):
                    right = construct_tree_subset(pointer.next, end_pointer, parent_name)
                    #print("here", pointer.value, right)
                    return [pointer.value, right]
            """
            
            # otherwise triple or more,

            output = [None]*3

            first_eq = None
            first_pow = None
            first_mult = None
            first_add = None
            
            sign = False

            left_elem = False

            cont = True
            p = pointer
            last_p = p
            while cont:
                if p == end_pointer:
                    cont = False
                else:
                    value = p.value
                    if value == '^':
                        left_elem = False
                        if first_pow == None:
                            first_pow = p
                        left_elem = False

                    elif value == '*' or value == '/':
                        left_elem = False
                        if first_mult == None:
                            first_mult = p
                        left_elem = False

                    elif value == '+' or value == '-':
                        if sign and left_elem:
                            # sign ==> form of -x, hence if x-y form take that over -x
                            first_add = p
                            sign = False
                        
                        elif first_add == None:
                            first_add = p
                            if left_elem:
                                pass
                            else:
                                sign = True
                        left_elem = False
                    
                    elif value == '<' or value == '>' or value == '<=' or value == '>=':
                        if first_eq == None:
                            first_eq = p
                        else:
                            value_str, full_str = error_string(pointer, end_pointer)
                            raise SyntaxError("\nStack Trace: {0}\nMultiple inequalities is unsupported.\n Section: '{1}'\n Full: '{2}'"\
                                              .format(parent_name, value_str, full_str))
                        left_elem = False
                            
                    else:
                        left_elem = True
                    last_p = p
                    p = p.next
                        
            func_p = None
            double_params = True
            
            if first_eq != None:
                func_p = first_eq
            elif first_add != None and not sign:
                func_p = first_add
            elif first_mult != None:
                func_p = first_mult
            elif first_pow != None:
                func_p = first_pow

            elif first_add and sign:
                #print("here", first_add.next.value, first_add.next.next.value)
                right = construct_tree_subset(first_add.next, end_pointer, parent_name)
                return [first_add.value, right]
            else:
                # get string representation of values
                value_str, full_str = error_string(pointer, end_pointer)
                
                raise ValueError("\nStack Trace: {0}\nMultiple parameters in parse string, however no valid function.\n Section: \"{1}\"\n Full: \"{2}\""\
                                 .format(parent_name, value_str, full_str))


            #### format tree

            output[0] = construct_tree_subset(pointer, func_p, parent_name)
            output[2] = construct_tree_subset(func_p.next, end_pointer, parent_name)
            output[1] = func_p.value

            return output
    
        output = construct_tree_subset(self.head, None, parent_name)
        if isinstance(output, list):
            pass # in desired output
        else:
            output = [output]
        return output



class LinearNode:
    def __init__(self, val):
        self.value = val
        self.next = None




class MathTree:
    def __init__(self, val=None):
        self.value = val
        self.left_child = None
        self.right_child = None
        self.function = None
        self.params = 0

    def __repr__(self):
        string = ""
        if self.function == None:
            string = str(self.value)
        else:
            left = str(self.left_child)
            right = str(self.right_child)
        
            if self.function == MathTree.add:
                string = left + " + " + right
            elif self.function == MathTree.sub:
                string = left + " - " + right
            elif self.function == MathTree.mult:
                string = left + " * " + right
            elif self.function == MathTree.div:
                string = left + " / " + right + ")"
            elif self.function == MathTree.pow:
                string = left + " ^ " + right + ")"
            elif self.function == MathTree.identity:
                string = "+" + left
            elif self.function == MathTree.negate:
                string = "-" + left
            elif self.function == MathTree.factorial:
                string = left + "!"
            elif self.function == MathTree._not:
                string = "~" + left
            elif self.function == MathTree.lesser:
                string = left + " < " + right
            elif self.function == MathTree.greater:
                string = left + ">" + right
            elif self.function == MathTree.leq:
                string = left + "<=" + right
            elif self.function == MathTree.geq:
                string = left + ">=" + right

        return "(" + string + ")"
    
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
    @staticmethod
    def negate(x):
        return -x
    @staticmethod
    def identity(x):
        return x
    @staticmethod
    def factorial(X):
        x = int(X)
    
        result = 1
        while x > 0:
            result = result * x
            x -= 1
        return result
    
    @staticmethod
    def _not(x):
        if x == 0:
            return 1
        else:
            return 0

    @staticmethod
    def leq(x,y):
        return x <= y
    @staticmethod
    def geq(x,y):
        return x >= y
    @staticmethod
    def greater(x,y):
        return x > y
    @staticmethod
    def lesser(x,y):
        return x < y



    def get_tree_value(self, parent_name:str):
        parse_error = False
        value = 0
        if self.params == 0:
            value =  self.value
        else:
            left_none = self.left_child  == None
            if left_none:
                parse_error = True
            else:
                x = self.left_child.get_tree_value(parent_name)
                if self.params == 1:
                    value = self.function(x)
                else:
                    right_none = self.right_child == None
                    if right_none:
                        parse_error = True
                    else:
                        y = self.right_child.get_tree_value(parent_name)
                        value =  self.function(x,y)
        
        if parse_error:
            #print(self.params, self.value, self.func)
            raise ValueError("Stack Trace: {0}\nMathTree result unbound, and MathTree incorrectly constructed.\n Left: {1}\n Right: {2}".format(parent_name, self.left_child, self.right_child))
        
        return value
            
        
        

    """
    @staticmethod
    def combine_elements(l_elem, func_elem, r_elem):
        # combine elements into higher tree.
        parent = MathTree(None)
        parent.function = func_elem
        parent.left_child = l_elem
        parent.right_child = r_elem
            
        return parent
    """
    
    @staticmethod
    def get_tree_leaf(string:str, parent_name:str, variables:dict):
        value = 0.0
        err = False
        try:
            value = float(string)
        except ValueError:
            # word may be a variable.
            try:
                value = variables[string]
            except KeyError:
                err = True
        if err:
            tmp_str = "Variable '{1}' is not initialised."
            tmp_str1 = "\nStack Trace: {0}\n" + tmp_str
            raise NameError(tmp_str1.format(parent_name, string))
            
        return MathTree(value)


    @staticmethod
    def construct_tree(string:str, parent_name:str, variables:dict):
        """
        Given a string, parse it up by parametres and operands. -> MathList.get_maths_list() function.
        Then divide it up into a valid MathTree object.
        
        :return: MathTree Objec
        """
        maths_list = MathList.get_maths_list(string, parent_name)
        list_tree = maths_list.construct_tree(parent_name)
        #print(maths_list)
        #print(list_tree)
        
        
        # everything is now nicely divided up. Turn into a tree.
        
        def treeify(maths_tree_list:list, parent_name:str):
            n = len(maths_tree_list)
            if n == 1:
                return MathTree.get_tree_leaf(maths_tree_list[0], parent_name, variables)
            elif n == 3:
                left = maths_tree_list[0]
                right = maths_tree_list[2]
            
                left_leaf = None
                right_leaf = None
                if isinstance(left, list):
                    left_leaf = treeify(left, parent_name)
                else:
                    left_leaf = MathTree.get_tree_leaf(left, parent_name, variables)
                
                if isinstance(right, list):
                    right_leaf = treeify(right, parent_name)
                else:
                    right_leaf = MathTree.get_tree_leaf(right, parent_name, variables)
                      
                operand = MathTree()
                operand.params = 2
                c = maths_tree_list[1]
                if c == '+':
                    operand.function = MathTree.add
                elif c == '-':
                    operand.function = MathTree.sub
                elif c == '*':
                    operand.function = MathTree.mult
                elif c == '/':
                    operand.function = MathTree.div
                elif c == '^':
                    operand.function = MathTree.pow
                elif c == '<':
                    operand.function = MathTree.lesser
                elif c == '>':
                    operand.function = MathTree.greater
                elif c == '<=':
                    operand.function = MathTree.leq
                elif c == '>=':
                    operand.function = MathTree.geq
                
                else:
                    raise ValueError("Stack Trace: {0}\nUnknown operand '{1}'".format(parent_name, c))
                        
                operand.left_child = left_leaf
                operand.right_child = right_leaf
                return operand
            
            
            elif n == 2:
                # unary operation
                left = maths_tree_list[0]
                right = maths_tree_list[1]
            
                leaf = None
            
                left_function = False
                right_function = False
                
                left_param = False
                right_param = False
            
                if isinstance(left, list):
                    leaf = treeify(left, parent_name)
                    left_param = True
                else:
                    if maths_1func(left):
                        left_function = True
                    else:
                        leaf = MathTree.get_tree_leaf(left, parent_name, variables)
                        left_param = True

                if isinstance(right, list):
                    leaf = treeify(right, parent_name)
                    right_param = True
                else:
                    if maths_1func(right):
                        right_function = True
                    else:
                        leaf = MathTree.get_tree_leaf(right, parent_name, variables)
                        right_param = True
                

                if (left_param and right_param) or (not left_param and not right_param):
                    raise ValueError("\nStack Trace: {0}\nTree incorrectly parsed, two parameters, no operand:\n '{1}' '{2}'"\
                                     .format(parent_name, left, right))
                else:
                    operand = MathTree()
                    operand.params = 1
                    c = ''
                    if not left_param:
                        c = left
                    elif not right_param:
                        c = right
                            
                    if c == '+':
                        operand.function = MathTree.identity
                    elif c == '-':
                        operand.function = MathTree.negate
                    elif c == '!':
                        operand.function = MathTree.factorial
                    elif c == '~':
                        operand.function = MathTree._not
                
                            
                    operand.left_child = leaf
                    #print("Leaf:",leaf)
                    return operand
                    
            
            else:
                raise ValueError("Stack Trace: {0}\nTree list Invalid length, '{1}'"\
                                 .format(parent_name, maths_tree_list))
        
        treeified = treeify(list_tree, parent_name)
        #input()
        return treeified






    """
    @staticmethod
    def construct_tree(string:str, parent_name:str):
        ###
        def get_value(word:str, l_elem, r_elem, parent_name:str):
            value = 0
            try:
                value = float(word)
            except ValueError:
                tmp_str = "Cannot connvert non-numeric string '{1}' into float expression."
                tmp_str1 = "\nFile Trace: {0}\n" + tmp_str
                raise ValueError(tmp_str1.format(parent_name, word))
                
            new_tree = MathTree(value)
            
            if l_elem == None:
                return new_tree,r_elem
            else:
                return l_elem, new_tree
        
        ###
        
        n = len(string)
        print(string)

        #left_elem = None
        #right_elem = None
        #func = None


        i = 0
        word_start = i
        while i < n:
            c = string[i]
            if maths_syntax(c):
                # turn word into a value
                if word_start == i:
                    pass # dont convert into word if there is no word
                else:
                    tmp_str = string[word_start:i]
                    print("1:", tmp_str)
                    left_elem, right_elem = get_value(tmp_str, left_elem, right_elem,
                                                      parent_name)
                
                if c == ')':
                    raise SyntaxError("\nStack Trace: {0}\nClose bracket has no opening bracket in '{1}'"\
                                      .format(parent_name, string))
                elif c == '(':
                    # Read opening bracket sub-syntax
                
                    open_brac_num = 1
                    j = i
                    while open_brac_num > 0 and j < n:
                        c = string[j]
                        if c == ')':
                            open_brac_num -= 1
                        else:
                            if c == '(':
                                open_brac_num += 1
                            j += 1
                            
                    if j == n:
                        raise SyntaxError("\nStack Trace: {0}\nNo closing bracket for '{1}'"\
                                          .format(parent_name, string))
                    else:
                        #new_string = string[i+1:j]
                        i = j
                    
                elif c == '+':
                    func = MathTree.add
                elif c == '-':
                    func = MathTree.sub
                elif c == '*':
                    func = MathTree.mult
                elif c == '/':
                    func = MathTree.div
                elif c == '^':
                    func = MathTree.pow
                else:
                    raise SyntaxError("\nStack Trace: {0}\nUnknown syntax element '{1}'"\
                                      .format(parent_name, string))
                word_start = i+1
                    
            else:
                # Not maths syntax.
                #scan through until reach next parsing element, i.e. function or number.
                pass
                
        
        
            i += 1
            if i == n and right_elem != None:
                tmp_str = string[word_start:i]
                print("2:", tmp_str)
                left_elem, right_elem = get_value(tmp_str, left_elem, right_elem, parent_name)

            if right_elem != None:
                left_elem,func,right_elem = combine_elems(left_elem, func, right_elem)
    
    
        ####  Exit While loop

        # finish parsing tree, make sure there are no syntax errors.
        if func != None:
            raise SyntaxError("\nStack Trace: {0}\nNo right hand parameter for function, {1}"\
                              .format(parent_name, string))
        else:
            return left_elem
    """




def parse_maths_string(string:str, parent_name:str, variables:dict):
    """
    If a string is written with numbers and numeric operations, get the computed float value.
    :input: maths string
    :return: float
    """
    if string == "":
        return None
    maths_tree = MathTree.construct_tree(string, parent_name, variables)
    
    val = maths_tree.get_tree_value(parent_name)
    #print("String:",string)
    #print("Maths Tree:", maths_tree)
    #print("result:",val)
    #print()
    
    return val



                                
                                
                                
def get_float_value(word:str, parent_name:str):
    value = 0
    try:
        value = float(word)
    except ValueError:
        tmp_str = "Cannot connvert non-numeric string '{1}' into float expression."
        tmp_str1 = "\nStack Trace: {0}\n" + tmp_str
        raise ValueError(tmp_str1.format(parent_name, word))
                                
    return value
