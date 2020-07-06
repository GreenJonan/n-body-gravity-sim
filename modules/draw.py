import pygame
import modules.body as b, modules.universe as u, modules.vector as v,\
    modules.constants as c, modules.colour as col
#import body as b, universe as u, vector as v, constants as c, colour as col
import math

"""
This module draws the objects.

track_id refers to the body id that the universe screen will track as the centre of the screen.

 - id < 0 ==> standard (0,0)
 - id = 0 ==> centre of mass
 - id > 0 ==> body with body_id id
"""



class UniverseScreen:
    def __init__(self, width=800, height=600, scale=1., colour=col.white):
        self.dims = (width,height)
        self.screen = pygame.display.set_mode(self.dims)
        self.colour = colour
        self.default_scale = scale
        self.scale = scale
        self.default_message = None
        
        self.screen_centre = (int(width/2), int(height/2))
        self.track_id = -1

        self.centre = None
        self.proj = None
    
    
    def get_pixel(self, x):
        """
        scale is: scale unit = 1 pixel. Hence pixels = vals / scale
        """
        return  int (x/self.scale)
    
    
    def update_projection(self, U:u.Universe, projection=(0,1)):
        """
        Given a particular plane of projection, update the projection tuple and associated centre.
        
        The projection takes the proj[0] and proj[1] part of X, for the position of bodies.
        Take possible projections as planes formed by the standard basis vectors.
        """
        
        if len(projection) != 2:
            raise ValueError("Error: Length of projection values is not 2, instead {0}".format(len(projection)))
        proj_x = projection[0]
        proj_y = projection[1]
            
        if proj_x < 0 or proj_x >= len(U.centre):
            raise ValueError("Error: Invalid vector component: {0}".format(proj_x))
        if proj_y < 0 or proj_y >= len(U.centre):
            raise ValueError("Error: Invalid vector component: {0}".format(proj_y))

        self.proj = (proj_x,proj_y)
        return self.proj


    def update_centre(self, centre=(0,0)):
        """
        Given the centre of the universe, find the pixel off set such that 
        it corresponds to the centre of the screen.
        """
        """
        p_x = self.get_pixel(centre[0])
        p_y = self.get_pixel(centre[1])
            
        zero_x = math.ceil(self.dims[0] / 2)
        zero_y = math.ceil(self.dims[1] / 2)
            
        self.centre = ( zero_x - p_x, zero_y - p_y)
        return self.centre
        """
        self.centre = centre


    def get_origin(self, v:v.Vector):
        """
        Given a vector, find the
        """
        if self.proj == None:
            raise ValueError("Error: UniverseScreen projection axes not updated.")
        
        proj_x = self.proj[0]
        proj_y = self.proj[1]
        
        c_x = v.components[proj_x]
        c_y = v.components[proj_y]
            
        return (c_x, c_y)
    
    
    
    def update_origin_tracking(self, U:u.Universe):
        """
        Given the current object being track, self.track_id, update the pixel centre.
        """
    
        origin = None
        if self.track_id < 0:
            return
        
        elif self.track_id == 0:
            origin = self.get_origin(U.get_centre_of_mass())
    
        else:
            body = U.get_body(self.track_id)
            origin = self.get_origin(body.X)
                
        self.update_centre(origin)



    ####   TRACKING FUNCTIONS

    def track_origin(self):
        self.track_id = -1
        self.centre = (0,0)

    def track_centre_of_mass(self, U:u.Universe):
        self.track_id = 0
        self.update_origin_tracking(U)

    def track_body(self, U:u.Universe, id):
        self.track_id = id
        self.update_origin_tracking(U)



    def update_tracking(self, U:u.Universe, id:int=-1):
        if id < 0:
            self.track_origin()
        elif id == 0:
            self.track_centre_of_mass(U)
        else:
            self.track_body(U, id)



    def track_next_object(self, U:u.Universe):
        """
        Track the next object in the universe
        """

        if self.track_id == U.max_id:
            pass
        else:
            new_track = self.track_id +1
            self.update_tracking(U, new_track)


    def track_prev_object(self, U:u.Universe):
        """
        Track the previous object in the universe.
        """

        if self.track_id < 0:
            pass
        else:
            new_track = self.track_id -1
            self.update_tracking(U, new_track)



    ####   DRAW TRACKING:

    def draw_tracking_label(self, U:u.Universe, text_size=20):
        """
        Draw a label for what body is currently being tracked.
        If the body has a name, use that instead of the id.
        """
    
        if self.track_id < 0:
            ## dont draw a label
            if self.default_message == None:
                pass
            else:
                self.write_message(self.default_message, text_size, centre=False,
                               text_colour=col.white, background_colour=None)
        elif self.track_id == 0:
            self.write_message("Centre of Mass", text_size, centre=False,
                               text_colour=col.white, background_colour=None)
        
        else:
            body = U.get_body(self.track_id)
            string = body.name
            
            if string == "":
                string = "Body " + str(self.track_id)
     
            self.write_message(string, text_size, centre=False,
                   text_colour=body.colour, background_colour=None)
    
    

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

        x = self.get_pixel(X.components[self.proj[0]] - self.centre[0])
        y = self.get_pixel(X.components[self.proj[1]] - self.centre[1])
        r = math.ceil(body.radius / self.scale)

        pix_centre = (x + self.screen_centre[0], -y + self.screen_centre[1])

        pygame.draw.circle(self.screen, body.colour, pix_centre, r)



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




    #####  Message Function

    def message(self, text:str, font_size:int=18, colour:tuple=col.black, background_colour=None):
        default_font = pygame.font.get_default_font()
        font = pygame.font.SysFont(default_font, font_size)
        
        antialising = False
        text_screen = font.render(text, antialising, colour, background_colour)
        return text_screen


    def write_message(self, text:str, font_size:int=12, centre=True,
                      text_colour:tuple=col.black, background_colour=col.white):
        
        text_screen = self.message(text, font_size, text_colour, background_colour)

        text_width = text_screen.get_width()
        text_height = text_screen.get_height()
        
        x,y = 0,0
        if centre:
            x = int(self.screen_centre[0] - (text_width/2))
            y = int(self.screen_centre[1] - (text_height/2))
        
        self.screen.blit(text_screen, (x,y))





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

