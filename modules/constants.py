"""
This module is just contains various constants
"""
import math

pi = math.pi
au_scale = 1.496e8*1000 #metres
scale = au_scale/300  # metres = 1pixel

G_const = 6.67430e-11 # Gravity constant

E_const = (1/(4*pi* 8.8541878128))*(10**12) # Electric constant

R_const = 1 # Resistance constant



sun_mass = 1.9884e30
earth_mass = 5.9722e24
moon_mass = 7.342e22

earth_speed = 29800
moon_speed = 1.022e3

moon_dist = 384402e3

sun_radius = 696342e3
earth_radius = 6371e3
moon_radius = 1737.4e3



screen_width = 1200
screen_height = 900

dist_error = 0.001
time_delay = int(1000/(40)) # how long to wait between each screen refresh in miliseconds
update_num = 4 # how many updates to compute before screen refresh


year = 60*60*24*365  #ideally 365, however accounting for lag
time_step = (year/60)*((time_delay)/1000)*((9*60+17)/(60*6*2) )  #*((9*60+15)/(60*6))
# expected to take two minutes to complete an orbit
