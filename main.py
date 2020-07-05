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


### Set up bodies
# let position be random, but inital velocity be zero

N = 10
bodies = [None] * N
i = 0
while i < N:
    X = vector.Vector.random_ball_vector(dim, max_radius)
    m = rnd.random() * max_mass
    q = 2*(1 - (rnd.random())/2) * max_charge
    r = rnd.random() * max_size

    uni.add_body(X,zero_vec, m=m, r=r, q=q, colour=colour.random_rgb())

    i += 1


# initialise projection screen of universe screen
uni_screen.update_projection(uni, projection=(0,1))



### Main run loop

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    uni_screen.draw_2dprojection_universe(uni)
    pygame.display.update()
