from modules.parser import parser
from modules import colour

import sys
import random as rnd
import pygame
pygame.init()
pygame.font.init()



def copy_system_to_file(consts, uni, uniscreen, f_name):
    string = "root {{\n\n{0}\n\n{1}\n\n{2}\n}}".format(consts, uni, uniscreen)
    f = open(f_name, "x")
    f.write(string)
    f.close()



def read_file():
    file_name = ""
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


f, file_name = read_file()
if f == None:
    sys.exit(0)

#file_name = "new_file.txt"
#f = open(file_name, "r")
parse_tree = parser.parse_file(f, file_name)

objects = parse_tree.objectify()



constants = objects[0]
universe = objects[1]
screen = objects[2]




if screen.scale < 0:
    # update scale based on max distance in constants object
    max_dist = constants.max_dist

    h,w = screen.dims
    length = h
    if w < length:
        length = w

    screen.scale = max_dist / (length * 2)
    screen.default_scale = screen.scale



#copy_name = "new_file2.txt"
#copy_system_to_file(constants, universe, screen, copy_name)

"""
au_scale = 1.496e8*1000 #metres
scale = au_scale/400  # metres = 1pixel
print("SCALE:",scale, screen.scale, scale/screen.scale)

sys.exit()
"""


"""

dim = 2
max_radius = 800
max_mass = 10
max_charge = 0
max_size = 100

zero_vec = vector.Vector.zero_vector(2)


### Set up screen

screen_width = constants.screen_width
screen_height = constants.screen_height

universe_scale = constants.scale
background_colour = colour.black

uni_screen = draw.UniverseScreen(width=screen_width, height=screen_height,
                                 scale=universe_scale, colour=background_colour)


### Initialise universe
uni = universe.Universe(centre=zero_vec)
time_step = constants.time_step


### Set up bodies
# let position be random, but inital velocity be zero

#####
N = 10
i = 0
while i < N:
    X = vector.Vector.random_ball_vector(dim, max_radius)
    m = rnd.random() * max_mass
    q = 2*(1 - (rnd.random())/2) * max_charge
    r = rnd.random() * max_size

    uni.add_body(X,zero_vec, m=m, r=r, q=q, colour=colour.random_rgb())

    i += 1
####

rad = 2*constants.scale
q = 0

# sun
sun_r = 15*rad
uni.add_body(zero_vec,zero_vec, m=constants.sun_mass, r=constants.sun_radius*16,
             q=0, colour=colour.orange, name="Sun")

# moon

X = vector.Vector([constants.au_scale + constants.moon_dist, 0])
V = vector.Vector([0, constants.moon_speed + constants.earth_speed])

uni.add_body(X,V, m=constants.moon_mass, r=constants.moon_radius*16,
             q=q, colour=colour.grey, name="Moon")



# planet

X = vector.Vector([constants.au_scale, 0])
V = vector.Vector([0, constants.earth_speed])

planet_r = 2*rad
uni.add_body(X,V, m=constants.earth_mass, r=constants.earth_radius*16,
             q=q, colour=colour.turquoise, name="Earth")

"""




# initialise projection screen of universe screen
screen.update_projection(universe, projection=(0,1))
screen.update_tracking(universe)



#####
#####   Main run loop
#####
"""
print()
for body in universe.bodies:
    print(body.name, body.X)
"""



loops = -1

start_screen = True
paused = False


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

    ###  draw functions

    screen.update_origin_tracking(universe)
    screen.draw_2dprojection_universe(universe)
    screen.draw_tracking_label(universe)


    ###  Update functions

    if not start_screen and not paused:
        #earth = universe.bodies[2]
        
        i = 0
        while i < constants.update_number:
            universe.update_all_bodies(constants.time_step / constants.update_number)
            
            """
            pass_start = earth.X.components[1] >= 0 >= earth.X_prev.components[1]\
                and earth.X.components[0] > 0
            if pass_start:
                loops += 1
            """
            """
            print()
            for body in universe.bodies:
                print(body.name, body.X)
            """
            i += 1

        
    elif paused:
        #uni_screen.write_message("Paused", text_size, centre=True,
        #                         text_colour=colour.white, background_colour=None)

        screen.write_label("Paused", colour.rgb_inverse(screen.colour), True, True)
    else:
        screen.write_title_message("Press SPACE to begin")
        #uni_screen.write_message("Press SPACE to begin", text_size, centre=True)


    pygame.display.update()
    pygame.time.delay(constants.time_delay)


#print("Loops:", loops)

pygame.quit()
pygame.font.quit()

