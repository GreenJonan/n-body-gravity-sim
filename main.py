import pygame
pygame.init()
pygame.font.init()



from modules.parser import parser
from modules import colour

########

### Update as needed

file_extension = "sys"

#######


import sys
import random as rnd
import math
import os


def copy_system_to_file(consts, uni, uniscreen, f_name):
    string = "root {{\n\n{0}\n\n{1}\n\n{2}\n}}".format(consts, uni, uniscreen)
    f = open(f_name, "x")
    f.write(string)
    f.close()



def read_file(file_name=""):
    while file_name == "":
        file_name = input("Enter a filename: ")
    if file_name == "quit" or file_name == "--q":
        return None
    f = None
    try:
        f = open(parser.directory + file_name, "r")
    except FileNotFoundError:
        print("File: '{0}' does not exist.".format(file_name))
        f, file_name = read_file()
    return f, file_name



def print_screen_text(screen, text, pos=(0,0), col=colour.black, size=50, background=None):
    default_font = pygame.font.get_default_font()
    font = pygame.font.SysFont(default_font, size)
        
    antialising = False
    text_screen = font.render(text, antialising, col, background)

    text_width = text_screen.get_width()
    text_height = text_screen.get_height()
    
    screen.blit(text_screen, pos)
    return text_width, text_height



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
                name = ".."
            else:
                if index == top_num:
                    up_arrow  = True
                elif top_num+space-1 == index and index != n:
                    down_arrow = True
                else:
                    name = files[index-1]
                
            if not down_arrow and not up_arrow:
                x, y = print_screen_text(window, name, pos=(offcentre[0],offcentre[1]+screen_height),
                                            col=text_colour, size=name_size)
                screen_height += y
                        
            elif up_arrow:
                draw_triangle(window, name_size, offset=(offcentre[0],screen_height), down=False)
                up_arrow = False
                screen_height += name_size
            elif down_arrow:
                draw_triangle(window, name_size, offset=(offcentre[0],screen_height), down=True)
                down_arrow = False
                screen_height += name_size
                        

            i += 1
        
        pygame.display.update()
        screen_height = 0
    return file_name




args = sys.argv
file_name = ""
f = None

if len(args) > 1:
    file_name = args[1]
    try:
        f = open(file_name, "r")
    except FileNotFoundError:
        print("File: '{0}' does not exist.".format(file_name))
else:
    file_name = run_load_window()
    if file_name != "":
        
        try:
            print(file_name)
            f = open(file_name, "r")
        except FileNotFoundError:
            print("File: '{0}' does not exist.".format(file_name))

if f == None:
    sys.exit(0)


#file_name = "new_file.txt"
#f = open(file_name, "r")

parse_tree = parser.parse_file(f, file_name)

variables = parser.default_variables

objects = parse_tree.objectify(variables)


constants = objects[0]
universe = objects[1]
screen = objects[2]




if constants == None:
    print("ERROR:\nNo Constants object given in '{0}'".format(file_name))
    sys.exit()
if universe == None:
    print("ERROR:\nNo Universe object given in '{0}'".format(file_name))
    sys.exit()
if screen == None:
    print("ERROR:\nNo Screen object given in '{0}'".format(file_name))
    sys.exit()



rnd.seed(constants.seed)
universe.conform_body_speeds()
dimension = len(universe.centre)


if screen.scale < 0:
    # update scale based on max distance in constants object
    max_dist = constants.max_dist

    h,w = screen.dims
    length = h
    if w < length:
        length = w

    screen.scale = max_dist / (length)
    screen.default_scale = screen.scale



#copy_name = "new_file2.txt"
#copy_system_to_file(constants, universe, screen, copy_name)



# initialise projection screen of universe screen
screen.update_projection(universe, projection=(0,1))
screen.update_tracking(universe)


if universe.display_trails:
    universe.update_trail_track(screen.track_id)


#####
#####   Main run loop
#####
"""
print()
for body in universe.bodies:
    print(body.name, body.X)
"""


phys_consts = (constants.G, constants.E, constants.R)


loops = -1

start_screen = True
paused = False

help = False
control = False

vector_line = False
object = None



run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        elif event.type == pygame.KEYDOWN:
            if start_screen:
                if event.key == pygame.K_SPACE:
                    start_screen = False
            else:
                if event.key == pygame.K_SPACE:
                    paused = not paused

                elif event.key == pygame.K_RIGHT:
                    screen.track_next_object(universe)
                elif event.key == pygame.K_LEFT:
                    screen.track_prev_object(universe)

                elif event.key == pygame.K_UP:
                    screen.scale = screen.scale / 2
                elif event.key == pygame.K_DOWN:
                    screen.scale = screen.scale * 2
                elif event.key == pygame.K_RETURN:
                    screen.scale = screen.default_scale

                elif event.key == pygame.K_z:
                    screen.show_zoom = not screen.show_zoom

                elif event.key == pygame.K_w:
                    if constants.warning_possible:
                        constants.warning = not constants.warning
                            
                elif event.key == pygame.K_t:
                    universe.display_trails = not universe.display_trails
                        
                    if universe.display_trails:
                        universe.update_trail_track(screen.track_id)
                    else:
                        universe.clear_trails()

                elif event.key == pygame.K_h:
                    print("TODO: help message")

                elif event.key == pygame.K_c:
                    if universe.can_control:
                        control = not control

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x,y = event.pos
            
            if event.button == 1:
                
                if control:
                    object = screen.get_body_at_point((x,y), universe)
                    if object != None:
                        vector_line = True

        elif event.type == pygame.MOUSEBUTTONUP:
            x,y = event.pos
            
            if event.button == 1:
                if vector_line:
                    vector_line = False
                
                    x0,y0 = screen.get_x_pix(object.X), screen.get_y_pix(object.X)
                    delta_x = screen.get_delta_pos_vector((x0,y0),(x,y), dimension)
                
                    momenta = delta_x * constants.control_scale
                    if object.mass != 0:
    
                        momenta = momenta * (constants.max_dist/object.mass)
                    object.V = momenta
                
                    object = None
                    control = False
    



    ###  draw functions

    screen.update_origin_tracking(universe)
    screen.draw_2dprojection_universe(universe)
    screen.draw_tracking_label(universe)

    if not start_screen and not paused:
        if control:
            screen.write_label("CONTROL", colour.rgb_inverse(screen.colour), True, (True,False))
            
            x,y = pygame.mouse.get_pos()
            if vector_line:
                if object != None:
                    x0,y0 = screen.get_x_pix(object.X), screen.get_y_pix(object.X)
                    pygame.draw.line(screen.screen, colour.rgb_inverse(screen.colour), (x0,y0), (x,y),5)

        else:
            ###  Update functions
        
            i = 0
            while i < constants.update_number:
                universe.update_all_bodies(constants.time_step / constants.update_number,
                                           phys_consts, constants.distance_error, constants.warning)
                i += 1

        
    elif paused:
        screen.write_label("Paused", colour.rgb_inverse(screen.colour), True, (True,True))
    else:
        screen.write_title_message("Press SPACE to begin")

    pygame.display.update()
    pygame.time.delay(constants.time_delay)


pygame.quit()
pygame.font.quit()

