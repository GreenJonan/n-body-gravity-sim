import pygame
import modules.body as b, modules.universe as u, modules.vector as v,\
    modules.constants as c, modules.colour as col
#import body as b, universe as u, vector as v, constants as c, colour as col
import math

"""
This module draws the objects.
"""



class UniverseScreen:
    def __init__(self, width=800, height=600, scale=1., colour=c.white):
        self.dims = (width,height)
        self.screen = pygame.display.set_mode(self.dims)
        self.colour = colour
        self.scale = scale

        self.centre = None
        self.proj = None
    
    
    def get_pixel(self, x):
        return  int (x/self.scale)
    
    
    def update_projection(self, U:u.Universe, projection=(0,1)):
        """
        Given a particular plane of projection, update the projection tuple and associated centre.
        
        The projection takes the proj[0] and proj[1] part of X, for the position of bodies.
        Take possible projections as planes formed by the standard basis vectors.
        
        Centre is given as offset in pixels such that the x,y vector corresponds to the centre of the screen.
        
        scale is: scale unit = 1 pixel. Hence pixels = vals / scale
        """
        
        C = U.centre
    
        if len(projection) != 2:
            raise ValueError("Error: Length of projection values is not 2, instead {0}".format(len(projection)))
        proj_x = projection[0]
        proj_y = projection[1]
            
        if proj_x < 0 or proj_x >= len(C):
            raise ValueError("Error: Invalid vector component: {0}".format(proj_x))
        if proj_y < 0 or proj_y >= len(C):
            raise ValueError("Error: Invalid vector component: {0}".format(proj_y))

        self.proj = (proj_x,proj_y)

        c_x = C.components[proj_x]
        c_y = C.components[proj_y]
            
        p_x = self.get_pixel(c_x)
        p_y = self.get_pixel(c_y)
            
        zero_x = math.ceil(self.dims[0] / 2)
        zero_y = math.ceil(self.dims[1] / 2)
            
        self.centre = ( zero_x - p_x, zero_y - p_y)
        return self.centre
            
            

    #####   DRAW PROJECTIONS
    #####


    ####  BODY

    def draw_2dprojection_body(self, body:b.Body):
        """
        Draw a body on a 2d plane by projecting its vector components onto two of the standard axes.
        The planes are given by self.proj = (x_proj, y_proj)
        
        Shift position of body to centre of the screen, 
        & use -y so that decreasing numbers go down the page.
        :input: Body object
        :return: None - but draw object
        """
        
        X = body.X
        x,y=0,0

        x = self.get_pixel(X.components[self.proj[0]])
        y = self.get_pixel(X.components[self.proj[1]])
        r = math.ceil(body.radius / self.scale)

        pygame.draw.circle(self.screen, body.colour, (x + self.centre[0], -y + self.centre[1]), r)



    def draw_general_2d_projection_body(self, body:b.Body, proj_vec1:v.Vector, proj_vec2:v.Vector):
        return NotImplemented





    #####  UNIVERSE

    def draw_2dprojection_universe(self, U:u.Universe):
        """
        Given a universe object, draw all possible objects on the screen.
        This is done by calling draw_2dprojection_body object for each body object.
        """
        
        self.screen.fill(self.colour)
        
        for body in U.bodies:
            if isinstance(body, b.Body):
                self.draw_2dprojection_body(body)




if __name__ == "__main__":
    pygame.init()
    UScreen = UniverseScreen()

    #bod = b.Body()
    zero2 = v.Vector.zero_vector(2)
    uni = u.Universe(zero2 )
    uni.add_body(zero2, zero2, r=20, colour=col.green)
    uni.add_body(v.Vector([100,-50]), zero2, r=20, colour=col.blue)

    UScreen.update_projection(uni)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        UScreen.draw_2dprojection_universe(uni)

        pygame.display.update()

    pygame.quit()

