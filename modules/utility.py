import random,pygame, os, math
from modules import colour

pygame.init()

def knuth_shuffle(array:list):
    """
    Shuffle an array in place
    """
    n = len(array)

    i = 0
    while i < n-1:
        j = random.randint(i, n-1)
        
        tmp = array[i]
        array[i] = array[j]
        array[j] = tmp

        i += 1

    return array


def get_range(start,stop):
    n = stop-start + 1
    i = 0
    array = [0]*n
    while i < n:
        array[i] = start + i
        i += 1
    return array


def shuffle_index(n):
    array = get_range(0,n-1)
    return knuth_shuffle(array)






###########  error screen

def error_window(text, buffer=(20,20),size=40):
    
    text_screens, w, h = get_text_screens(text, pos=buffer, size=size)
    error_screen = pygame.display.set_mode((w+2*buffer[0], h+2*buffer[1]))
    pygame.display.set_caption("Error Window")
    
    error_screen.fill(colour.white)
    
    x,y = buffer
    
    for sub_screen, del_y in text_screens:
        error_screen.blit(sub_screen, (x,y))
        y += del_y
    pygame.display.update()
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    return






######################   Screen text

def get_text_screens(text:str, pos=(0,0), col=colour.black, size=50, background=None):
    default_font = pygame.font.get_default_font()
    font = pygame.font.SysFont(default_font, size)
    
    antialising = False
    phrases = text.split("\n")
    
    text_screens = []
    max_width,total_height = 0,0
    
    
    for phrase in phrases:
        text_screen = font.render(phrase, antialising, col, background)
        
        text_width = text_screen.get_width()
        text_height = text_screen.get_height()
        
        if text_width > max_width:
            max_width = text_width
        total_height += text_height
        
        text_screens.append((text_screen, text_height))
    
    return text_screens, max_width, total_height



def print_screen_text(screen, text, pos=(0,0), col=colour.black, size=50, background=None, centre=False):
    text_screens, max_width, total_height = get_text_screens(text, pos, col, size, background)
    
    w,h = screen.get_width(), screen.get_height()
    x,y = pos
    
    if centre:
        x += int((w-max_width)/2)
        y += int((h-total_height)/2)
    
    
    for sub_screen, del_y in text_screens:
        
        screen.blit(sub_screen, (x,y))
        y += del_y
    
    return max_width, total_height



#### Text shapes




def draw_triangle(screen, height:int, offset=(0,0), col=colour.black, down=True):
    x_left_offset = 30
    x,y = offset
    
    scale = 0.5
    new_height = int(scale*height)
    side_length = int( 2 * new_height/ math.sqrt(3))
    
    y_offset = int((height-new_height)/2)
    p1,p2,p3 = None,None,None
    
    
    x_left = offset[0] + x_left_offset
    x_right = x_left + side_length
    x_mid = x_left + int(side_length/2)
    y_top = offset[1] + y_offset
    y_bottom = y_top + new_height
    
    if down:
        p1 = (x_left,y_top)
        p2 = (x_right, y_top)
        p3 = (x_mid, y_bottom)
    else:
        p1 = (x_left, y_bottom)
        p2 = (x_mid, y_top)
        p3 = (x_right, y_bottom)
    
    pygame.draw.polygon(screen, col, [p1,p2,p3])
    return




###### Directory and file formatting helpers

def get_prev_dir(path:str):
    if len(path) <= 1:
        return "/"
    else:
        string = ""
        paths = path.split("/")
        n = len(paths)
        
        i = 0
        while i < n-1:
            string += paths[i]
            i += 1
            if i != n-1:
                string += "/"

        if len(string) == 0:
            string = "/"
        return string


def get_files(path:str):
    children = os.listdir(path)
    
    files = []
    directories = []
    for child in children:
        child_path = path +"/" + child
        
        if os.path.isfile(child_path):
            files.append(child)
        elif os.path.isdir(child_path):
            directories.append(child)
    
    output = []
    for dir in directories:
        if len(dir) > 0:
            if dir[0] == '.':
                pass #hidden folder
            else:
                output.append(dir + "/")

    for file in files:
        if len(file) > 0:
            if file[0] == '.':
                pass # hidden file
            else:
                # check to see whether the file is the required type
                names = file.split(".")
                if names[-1] == file_extension:
                    
                    # update file name by striping the file extnesion.
                    new_name = ""
                    
                    i = 0
                    n = len(names)
                    while i < n-1:
                        new_name += names[i]
                        i +=1
                        if i != n-1:
                            new_name += "."
                    
                    output.append(new_name)

    return output



def get_folder_name(path:str):
    names = path.split("/")
    return names[-1] + "/"







####################     LOAD WINDOW

### Update as needed

file_extension = "sys"



def run_load_window():
    # loading window
    file_name = ""
    
    name_size = 40
    title_size = 50
    width,height = 800,600
    gap = 10
    offcentre = (10,10)
    
    window = pygame.display.set_mode((width,height))
    pygame.display.set_caption("File Selection")
    
    
    x,y = print_screen_text(window, "", size=name_size)
    name_height = y
    
    x,y = print_screen_text(window, "", size=title_size)
    title_height = y
    
    name_space = height - gap - title_height - offcentre[1]
    space = name_space//name_height
    
    
    #path = os.getcwd()
    path = os.path.expanduser("~")
    folder_name= get_folder_name(path)
    files = get_files(path)
    
    file_num = 0
    top_num = 0
    screen_height = 0
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    
                    if file_num < n:
                        file_num += 1
                    
                    if file_num != n:
                        if file_num - top_num >= space-1:
                            top_num += 1
    
                elif event.key == pygame.K_UP:
                    if file_num > 0:
                        file_num -= 1
                    
                        if file_num != 0:
                            if file_num <= top_num:
                                top_num -= 1
            
                elif event.key == pygame.K_RETURN:
                    if file_num == 0:
                        # go up a directory
                        path = get_prev_dir(path)
                        files = get_files(path)
                        folder_name = get_folder_name(path)
                
                    else:
                        sub_name = files[file_num-1]
                        
                        if len(sub_name) > 0:
                            if sub_name[-1] == '/':
                                # is directory
                                folder_name = sub_name
                                
                                tmp_path = path + "/" + sub_name
                                path = tmp_path[0:len(tmp_path)-1]
                                
                                files = get_files(path)
                            
                            else:
                                file_name = path + "/" + sub_name + "." + file_extension
                                run = False

                    top_num = 0
                    file_num = 0
                    
                    
        window.fill(colour.white)
        n = len(files)
                            
        x, y = print_screen_text(window, "Folder:  " + folder_name,
                                 pos=(offcentre[0],offcentre[1]+screen_height),size=title_size)
                                
        screen_height += y + gap + offcentre[1]
        distance = height - screen_height
                                        
        down_arrow = False
        up_arrow = False
                                                
        i = 0
        while i < min(space,n+1):
            index = i + top_num
                                                            
            name = ""
            text_colour = colour.black
            if index == file_num:
                text_colour = colour.red
                                                                            
            if index == 0:
                name = "BACK"
            else:
                if index == top_num:
                    up_arrow  = True
                elif top_num+space-1 == index and index != n:
                    down_arrow = True
                else:
                    name = files[index-1]
                                                                                                                            
            if up_arrow:
                draw_triangle(window, name_size, offset=(offcentre[0],screen_height), down=False)
                up_arrow = False
                screen_height += name_height
            elif down_arrow:
                draw_triangle(window, name_size, offset=(offcentre[0],screen_height), down=True)
                down_arrow = False
                screen_height += name_height

            else:
                x, y = print_screen_text(window, name, pos=(offcentre[0],offcentre[1]+screen_height),
                                         col=text_colour, size=name_size)
                screen_height += y

            i += 1

        pygame.display.update()
        screen_height = 0
    return file_name


