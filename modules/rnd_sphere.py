import random as rnd
import math

"""
IMPORTANT, READ ME:
    spherical and ball sampling appears to work correctly, 
        however I'm uncertain whether the elliptical sampling is correct.
    I think it is not uniform over the area and more points are generated over the shorter axii
        then the longer axii. However, they do form an ellipse.
"""



"""
The first method is technically not correct.
Look at: http://extremelearning.com.au/how-to-generate-uniformly-random-points-on-n-spheres-and-n-balls/


The reason why it doesn't work is the fact that the surface is stretched out around the poles and squished around the equators. Hence, the angles need to be modified by a cummalative density function and inverse transform sampling. Howevever, I don't know what I need for the angles.
For the radius, the inverse transform sampling gives the radius, r in u[0,1] to be r^1/n
"""


"""

def gen_rnd_angles(dim:int=2):
    ###
    Given a particular dimension, generate random point on the surface of a unit sphere.
    Represent the co-ordinate system as spherical co-ordinates
    Let Radius be +1 or -1.
    Generate angle between 0 and pi for first angle, and -pi/2 and +pi/2 for remaining angles.
    ###
    
    if dim <= 0:
        raise ValueError("Error: Dimension undefined: {0}".format(dim))
    
    pi = math.pi
    sign = 1

    p = rnd.random()
    if p < 1/2:
        sign = -1

    angles = [0] * (dim-1)
    i = 0
    while i < dim - 1:
        if i == 0:
            angles[i] = rnd.random() * pi
        else:
            angles[i] = (rnd.random() - 0.5) * pi
        i += 1

    return angles,sign


def gen_unit_sphere_coords(dim:int=2):
    ###
    Suppose have angles, p1,p2,..,pn-1
    
    Then,
    x1 = cos(p1)
    x2 = sin(p1)cos(p2)
    x3 = sin(p1)sin(p2)cos(p3)
    ...
    xn = sin(p1)sin(p2)...sin(pn-1)
    ###

    if dim <= 0:
        raise ValueError("Error: Dimension undefined: {0}".format(dim))

    angles, sign = gen_rnd_angles(dim)
    #print(angles)

    if dim == 1:
        return [sign]
    else:
        # Only modify the first angle
        # restricts
        angles[0] = sign * angles[0]

        sin_vals = 1
        results = [0] * dim
        i = 0
        while i < dim:
            if i+1 != dim:
                results[i] = sin_vals * math.cos(angles[i])
                sin_vals = sin_vals * math.sin(angles[i])
            else:
                results[i] = sin_vals
            i += 1
        return results


def gen_ball_coords(dim:int=2, radius:float=1.0):
    if radius < 0:
        raise ValueError("Error: Radius must be postiive")
    sphere = gen_unit_sphere_coords(dim)
    r = radius * ( rnd.random() ** (1/dim))
    i = 0
    while i < dim:
        sphere[i] = sphere[i] * r
        i += 1
    return sphere
"""




"""
This function appears to produce far less clumping than the previous method.
I don't understand why but it appears to work.
"""

def muller_n_sphere(dim:int=2, r=1):
    # this is form Method 19 of the link above.
    if dim <= 0:
        raise ValueError("Error: Dimension undefined: {0}".format(dim))

    vec = [0] * dim
    d = 0
    i = 0
    while i < dim:
        vec[i] += rnd.gauss(0,1)
        d += vec[i]*vec[i]
        i += 1
    d = d**(1/2)

    i = 0
    while i < dim:
        vec[i] = r*vec[i] / d
        i += 1
    return vec


def muller_n_ball(dim:int=2, radius:float=1.0):
    if radius < 0:
        raise ValueError("Error: Radius must be postiive")

    sphere = muller_n_sphere(dim)
    r = radius * ( rnd.random() ** (1/dim))
    i = 0
    while i < dim:
        sphere[i] = sphere[i] * r
        i += 1
    return sphere



def muller_n_ellipse(dim:int, radii:list):
    if len(radii) != dim:
        raise ValueError("Error: Number of ellipse radii, {0}, do not match dimension of vector, {1}".format(len(radii), dim))
    sphere = muller_n_sphere(dim)
    R = rnd.random() ** (1/dim)
    i = 0
    while i < dim:
        Rad = radii[i]
        if Rad < 0:
            raise ValueError("Error: Radius must be positive; {0}".format(Rad))
        # scale radius by ellipse radius
        r = R * Rad
        sphere[i] = sphere[i] * r
        i += 1
    return sphere





if __name__ == "__main__":
    N = 500
    
    import matplotlib.pyplot as plt
    
    """
    fig = plt.figure()
    ax = fig.add_subplot(111,projection="3d")
    
    i = 0
    while i < N:
        #v = gen_unit_sphere_coords(3)
        v = gen_ball_coords(3)
        #print(v)
        ax.scatter(v[0], v[1], v[2])
        i += 1
    #plt.axis('scaled')
    """

    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111,projection="3d")
    #ax2 = fig2.add_subplot(111)
    i = 0
    while i < N:
        v = muller_n_sphere(3)
        #v = muller_n_ball(3)
        #v = muller_n_ellipse(3, [5,2.5,3])
        ax2.scatter(v[0], v[1],v[2])
        i += 1
    #plt.axis('scaled')

    plt.show()

