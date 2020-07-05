from modules import body
from modules import constants
from modules import draw
from modules import universe
from modules import vector
from modules import colour

import random as rnd
import pygame
pygame.init()



dim = 2
max_radius = 800
max_mass = 10
max_charge = 0
max_size = 100

zero_vec = vector.Vector.zero_vector(2)


### Set up screen

screen_width = 1000
screen_height = 750

universe_scale = 10.0
background_colour = colour.white

uni_screen = draw.UniverseScreen(width=screen_width, height=screen_height,
                                 scale=universe_scale, colour=background_colour)


### Initialise universe
uni = universe.Universe(centre=zero_vec)
time_step = 1


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


# planet

#X = vector.Vector.random_sphere_vector(dim, max_radius)
#V = vector.Vector([X.components[0], -X.components[1]])
X = vector.Vector([universe_scale * 100, 0])
V = vector.Vector([0, universe_scale * 10])
m = 50000
#q = 2*(1 - (rnd.random())/2) * max_charge
q = 0
r = 100
    
uni.add_body(X,V, m=m, r=r, q=q, colour=colour.random_rgb())


# sun
uni.add_body(zero_vec,zero_vec, m=500*m, r=2*r, q=0, colour=colour.random_rgb())





# initialise projection screen of universe screen
uni_screen.update_projection(uni, projection=(0,1))




#####
#####   Main run loop
#####


run = True
while run:
    pygame.time.delay(constants.time_delay)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    uni_screen.draw_2dprojection_universe(uni)
    pygame.display.update()

    i = 0
    while i < constants.update_num:
        uni.update_all_bodies(time_step / constants.update_num)
        i += 1




