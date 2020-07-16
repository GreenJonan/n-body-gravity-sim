import pygame
pygame.init()
pygame.font.init()



from modules.parser import parser
from modules import colour, utility

#######


import sys
import random as rnd
import math


def copy_system_to_file(consts, uni, uniscreen, f_name):
    string = "root {{\n\n{0}\n\n{1}\n\n{2}\n}}".format(consts, uni, uniscreen)
    f = open(f_name, "x")
    f.write(string)
    f.close()


"""
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

"""








##############################

load_error = False
error_name = ""



args = sys.argv
file_name = ""
f = None


try:
    if len(args) > 1:
        file_name = args[1]
    else:
        file_name = utility.run_load_window()

    if file_name == "":
        sys.exit(0)
    else:
        f = open(file_name, "r")


except FileNotFoundError:
    load_error = True
    error_name = "File: '{0}' does not exist.".format(file_name)
except Exception as e:
    load_error = True
    error_name = "Unknown Error:\n" + str(e)




constants = None
universe = None
screen = None



variables = parser.default_variables
parse_tree = None
objects = None

if not load_error:
    try:
        parse_tree = parser.parse_file(f, file_name)
        objects = parse_tree.objectify(variables)

    except SyntaxError as e:
        load_error = True
        error_name = "SyntaxError:"+str(e)
    except NameError as n:
        load_error = True
        error_name = "VariableError:"+str(n)
    except TypeError as t:
        load_error = True
        error_name = "TypeError:"+str(t)
    except ValueError as v:
        load_error = True
        error_name = "ValueError:"+str(v)
    except Exception as e:
        load_error = True
        error_name = "Unknown Error:\n"+str(e)


if not load_error:
    constants = objects[0]
    universe = objects[1]
    screen = objects[2]

    if constants == None:
        error_name = "ERROR:\nNo Constants object given in\n'{0}'".format(file_name)
        load_error = True
    elif universe == None:
        error_name = "ERROR:\nNo Universe object given in\n'{0}'".format(file_name)
        load_error = True
    elif screen == None:
        error_name = "ERROR:\nNo Screen object given in\n'{0}'".format(file_name)
        load_error = True


if load_error:
    utility.error_window(error_name)
    sys.exit(0)



rnd.seed(constants.seed)
universe.conform_body_speeds()
dimension = len(universe.centre)


set_up_error = False
error_name = ""

if screen.scale < 0:
    # update scale based on max distance in constants object
    max_dist = constants.max_dist

    h,w = screen.dims
    length = h
    if w < length:
        length = w
    
    if length <= 0:
        set_up_error = True
        error_name = "Screen Dimensions are invalid: ({0},{1})".format(w,h)

    else:
        screen.scale = max_dist / (length)
        screen.default_scale = screen.scale



#copy_name = "new_file2.txt"
#copy_system_to_file(constants, universe, screen, copy_name)



# initialise projection screen of universe screen
try:
    screen.update_projection(universe, projection=(0,1))
    screen.update_tracking(universe)

    if universe.display_trails:
        universe.update_trail_track(screen.track_id)

except Exception as e:
    error_name = str(e)
    set_up_error = True


if set_up_error:
    utility.error_window(error_name)
    sys.exit(0)




#####
#####   Main run loop
#####


phys_consts = (constants.G, constants.E, constants.R)

help_comment = "Help:\n\nPress h to open/close help message.\n\nPress Spacebar to pause/unpause\n\nPress 'p' to pan the camera by clicking and dragging the screen.\n\nUse arrow keys to zoom/focus on a body.\n\nPress 'return' to restore default pan/zoom.\n\nPress 'z' to show zoom levels.\n\nPress 't' to activate/deactivate Trails if given in systems file.\n\nPress 'c' to control objects if given in systems file."


error = False
error_name = ""

start_screen = True
paused = False

help = False
control = False

vector_line = False
object = None

pan = False
x_prev,y_prev = 0,0
prev_offset = 0,0
clicked = False

wait = False


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
        elif not error:
            if event.type == pygame.KEYDOWN:
                if start_screen:
                    if event.key == pygame.K_SPACE:
                        start_screen = False
                        wait = False
                elif help:
                    if event.key == pygame.K_h:
                        help = False
                        wait = False
                
                else:
                    if event.key == pygame.K_SPACE:
                        paused = not paused
                        wait = False
                
                        if control:
                            # Reset control selection.
                            object = None
                            vector_line = False
            

                    elif event.key == pygame.K_RIGHT:
                        wait = not screen.track_next_object(universe)
                    
                    elif event.key == pygame.K_LEFT:
                        wait = not screen.track_prev_object(universe)

                    elif event.key == pygame.K_UP:
                        if not (clicked and pan):
                            screen.scale = screen.scale / 2
                            x_off,y_off = screen.offset
                            screen.offset = (int(x_off*2), int(y_off*2))
                            wait = False

                    elif event.key == pygame.K_DOWN:
                        if not (clicked and pan):
                            screen.scale = screen.scale * 2
                            x_off,y_off = screen.offset
                            screen.offset = (int(x_off/2), int(y_off/2))
                            wait = False

                    elif event.key == pygame.K_RETURN:
                        screen.scale = screen.default_scale
                        if pan:
                            screen.offset = (0,0)
                        wait = False

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
                        help = True
                        wait = False

                    elif event.key == pygame.K_c:
                        if universe.can_control and not paused:
                            control = not control
                            if pan:
                                pan = not pan

                    elif event.key == pygame.K_p:
                        #if paused:
                        pan = not pan
                        if control:
                            control = not control
                        wait = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x,y = event.pos
            
                if event.button == 1:
                    clicked = True
                
                    if control and not paused:
                        object = screen.get_body_at_point((x,y), universe)
                        if object != None:
                            vector_line = True

                    elif pan:
                        x_prev,y_prev = x,y
                        #prev_centre = screen.screen_centre
                        prev_offset = screen.offset


            elif event.type == pygame.MOUSEBUTTONUP:
                x,y = event.pos
            
                if event.button == 1:
                    clicked = False
                
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

    
            elif event.type == pygame.MOUSEMOTION:
                if pan and clicked:
                    x,y = pygame.mouse.get_pos()
                    del_x = x - x_prev
                    del_y = y - y_prev
                    screen.offset = (del_x + prev_offset[0], del_y + prev_offset[1])



    ###  draw functions

    if not wait and not error:
        try:
            screen.update_origin_tracking(universe)
            screen.draw_2dprojection_universe(universe, grid=pan)
            screen.draw_tracking_label(universe)
            pause_drawn = True
        except Exception as e:
            error = True
            error_name = str(e)


    if not error and not wait:
        if start_screen:
            screen.write_title_message("Press SPACE to begin")
            wait = True
        
        elif paused:
            if pan:
                screen.write_label("PAN CAMERA", colour.rgb_inverse(screen.colour), True, (True,False))
            else:
                screen.write_label("Paused", colour.rgb_inverse(screen.colour), True, (True,True))
                wait = True

        elif help:
            wait = True
            screen.write_label(help_comment, colour.rgb_inverse(screen.colour), True, (False,True),
                               size=50, offset=(50,0))

        else:
            if control:
                screen.write_label("CONTROL", colour.rgb_inverse(screen.colour), True, (True,False))
            
                x,y = pygame.mouse.get_pos()
                if vector_line:
                    if object != None:
                        x0,y0 = screen.get_x_pix(object.X), screen.get_y_pix(object.X)
                        pygame.draw.line(screen.screen, colour.rgb_inverse(screen.colour), (x0,y0), (x,y),5)

            else:
                ###  Update functions
                try:
                    i = 0
                    while i < constants.update_number:
                        universe.update_all_bodies(constants.time_step / constants.update_number,
                                                   phys_consts, constants.distance_error, constants.warning)
                        i += 1
                except OverflowError:
                    error = True
                    error_name = "An Overflow Error occured.\nPlease quit."
                except Exception as e:
                    error = True
                    error_name = str(e)
  


    if error and not wait:
        screen.write_title_message(error_name)
        wait = True

    pygame.display.update()
    pygame.time.delay(constants.time_delay)


pygame.quit()
pygame.font.quit()

