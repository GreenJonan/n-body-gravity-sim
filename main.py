from modules import body
from modules import constants
from modules import draw
from modules import universe
from modules import vector
from modules import colour

import random as rnd
import pygame
pygame.init()
pygame.font.init()



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

"""
N = 10
i = 0
while i < N:
    X = vector.Vector.random_ball_vector(dim, max_radius)
    m = rnd.random() * max_mass
    q = 2*(1 - (rnd.random())/2) * max_charge
    r = rnd.random() * max_size

    uni.add_body(X,zero_vec, m=m, r=r, q=q, colour=colour.random_rgb())

    i += 1
"""

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






# initialise projection screen of universe screen
uni_screen.update_projection(uni, projection=(0,1))
uni_screen.update_tracking(uni)



#####
#####   Main run loop
#####


loops = -1

start_screen = True
paused = False
text_size = 100
label_size = 50

uni_screen.default_message = "Default: Object Radius x16"


run = True
while run:
    #input("Next:")
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
                    uni_screen.track_next_object(uni)
                elif event.key == pygame.K_LEFT:
                    uni_screen.track_prev_object(uni)

                elif event.key == pygame.K_UP:
                    uni_screen.scale = uni_screen.scale / 2
                elif event.key == pygame.K_DOWN:
                    uni_screen.scale = uni_screen.scale * 2
                elif event.key == pygame.K_RETURN:
                    uni_screen.scale = uni_screen.default_scale

    ###  draw functions

    uni_screen.update_origin_tracking(uni)
    uni_screen.draw_2dprojection_universe(uni)
    uni_screen.draw_tracking_label(uni, label_size)


    ###  Update functions

    if not start_screen and not paused:
        earth = uni.bodies[1]
        
        i = 0
        while i < constants.update_num:
            uni.update_all_bodies(time_step / constants.update_num)
            
            """
            pass_start = earth.X.components[1] >= 0 >= earth.X_prev.components[1]\
                and earth.X.components[0] > 0
            if pass_start:
                loops += 1
            """
            i += 1

        
    elif paused:
        uni_screen.write_message("Paused", text_size, centre=True,
                                 text_colour=colour.white, background_colour=None)
    else:
        uni_screen.write_message("Press SPACE to begin", text_size, centre=True)


    pygame.display.update()
    pygame.time.delay(constants.time_delay)


#print("Loops:", loops)

pygame.quit()
pygame.font.quit()

