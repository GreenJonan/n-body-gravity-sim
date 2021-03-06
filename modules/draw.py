import sys
int_max = 2147483647
max_distance = 25000

import pygame

import modules.body as b
import modules.universe as u
import modules.vector as v
import modules.constants as c
import modules.colour as col
from modules import collision

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
    def __init__(self, width=800, height=600, scale=1., colour=col.white,
                 text_colour=col.black, label_size=50, title_size=100, msg=None):
        
        self.dims = (width,height)
        self.screen = pygame.display.set_mode(self.dims)
        pygame.display.set_caption("Simulation")
        
        self.colour = colour
        self.default_scale = scale
        self.scale = scale
        
        self.default_message = msg
        self.text_colour = text_colour
        self.label_size = label_size
        self.title_size = title_size
        
        
        self.screen_centre = self.default_centre()
        self.offset = (0,0)
        self.track_id = -1

        self.centre = None
        self.proj = None
    
        self.show_zoom = False
        self.updated_default_centre = False
    
        # update the screen to say 'loading'
        self.write_label("Loading...", col.rgb_inverse(self.colour), True, (True,True))
        pygame.display.update()
    
    
    
    
    def __repr__(self):
        string = "screen {{\nwidth: {0}\nheight:{1}\nbackground: colour {{{2}}}\ntextColour: colour {{{3}}}\nlabelSize:{4}\ntitleSize:{5}\ndefaultMessage: \"{6}\"\nscale: {7}\n}}"\
            .format(self.dims[0], self.dims[1], col.get_rgb_str(self.colour), col.get_rgb_str(self.text_colour), self.label_size, self.title_size, self.default_message, self.scale)
        return string
    
    
    
    def get_pixel(self, x):
        """
        scale is: scale unit = 1 pixel. Hence pixels = vals / scale
        """
        return int (x/self.scale)
    
    
    
    def default_centre(self):
        return (int(self.dims[0]/2), int(self.dims[1]/2))
    
    
    
    
    def get_body_at_point(self, point:tuple, U:u.Universe):
        """
        Given a point x,y in pixels, find the last body such that it intersects with this point.
        This means it is in the same order as the drawing of the objects on the screen.
        """
        result = None
    
        n = len(U.bodies)
        i = 0
        while i < n:
            body = U.bodies[i]
            if isinstance(body, b.Body):
                x_pix = self.get_x_pix(body.X)
                y_pix = self.get_y_pix(body.X)
                r = math.ceil(body.radius / self.scale)
            
                if collision.particle_circle_collide((x_pix,y_pix), r, point):
                    result = body
            i += 1
        return result
    
    
    
    def update_projection(self, U:u.Universe, projection=(0,1)):
        """
        Given a particular plane of projection, update the projection tuple and associated centre.
        
        The projection takes the proj[0] and proj[1] part of X, for the position of bodies.
        Take possible projections as planes formed by the standard basis vectors.
        """
        
        if len(projection) != 2:
            raise ValueError("Error: Length of projection values is {0}, not 2.".format(len(projection)))
        proj_x = projection[0]
        proj_y = projection[1]
            
        if proj_x < 0 or proj_x >= len(U.centre):
            raise ValueError("Invalid vector component: {0}".format(proj_x))
        if proj_y < 0 or proj_y >= len(U.centre):
            raise ValueError("Invalid vector component: {0}".format(proj_y))

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
            raise ValueError("UniverseScreen projection axes not updated.")
        
        proj_x = self.proj[0]
        proj_y = self.proj[1]
        
        c_x = v.components[proj_x]
        c_y = v.components[proj_y]
            
        return (c_x, c_y)
    
    
    
    def update_origin_tracking(self, U:u.Universe, force_update=False):
        """
        Given the current object being track, self.track_id, update the pixel centre.
        """
    
        origin = None
        if self.track_id < 0:
            """
            if force_update or not self.updated_default_centre:
                origin = self.get_origin(U.centre)
                self.updated_default_centre = True
            else:
            """
            return
        
        elif self.track_id == 0:
            origin = self.get_origin(U.get_centre_of_mass())
    
        else:
            body = U.get_body(self.track_id)
            origin = self.get_origin(body.X)
                
        self.update_centre(origin)



    ####   TRACKING FUNCTIONS

    def track_universe_origin(self, U:u.Universe):
        self.track_id = -1
        self.centre = self.get_origin(U.centre)

    def track_centre_of_mass(self, U:u.Universe):
        self.track_id = 0
        self.update_origin_tracking(U)

    def track_body(self, U:u.Universe, id):
        self.track_id = id
        self.update_origin_tracking(U)



    def update_tracking(self, U:u.Universe, id:int=-1):
        if id < 0:
            self.track_universe_origin(U)
        elif id == 0:
            self.track_centre_of_mass(U)
        else:
            self.track_body(U, id)



    def track_next_object(self, U:u.Universe):
        """
        Track the next object in the universe
        """

        if self.track_id == U.max_id:
            return False
        else:
            new_track = self.track_id +1
            self.update_tracking(U, new_track)
            return True


    def track_prev_object(self, U:u.Universe):
        """
        Track the previous object in the universe.
        """

        if self.track_id < 0:
            return False
        else:
            new_track = self.track_id -1
            self.update_tracking(U, new_track)
            return True



    ####   DRAW TRACKING:

    def draw_tracking_label(self, U:u.Universe):
        """
        Draw a label for what body is currently being tracked.
        If the body has a name, use that instead of the id.
        """
        
        msg = ""
        colour = None
    
        if self.track_id < 0:
            ## dont draw a label
            if self.default_message == None:
                pass
            else:
                msg = self.default_message
            colour = col.rgb_inverse(self.colour)
                
        elif self.track_id == 0:
            msg = "Centre of Mass"
            colour = col.rgb_inverse(self.colour)
        
        else:
            body = U.get_body(self.track_id)
            msg = body.get_name()

            colour = body.colour
                
        if self.show_zoom:
            zoom = self.default_scale/ self.scale
            if zoom != 1.0:
                if len(msg) != 0:
                    msg += ",   " + "Zoom: x" + str(zoom)
                else:
                    msg = "Zoom: x" + str(zoom)
        
        self.write_label(msg, colour)
    

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
        width,height = self.dims

        r = math.ceil(body.radius / self.scale)

        x_px = self.get_x_pix(X)
        y_px = self.get_y_pix(X)

        self.draw_ball((x_px,y_px), r, body.colour, body.get_name())




    def draw_general_2d_projection_body(self, body:b.Body, proj_vec1:v.Vector, proj_vec2:v.Vector):
        return NotImplemented




    def draw_ball(self, centre, radius, colour, name="", fill=True):
        """
        Given a ball with centre and radius (in pixels), draw it on the screen.
        
        When the radius is too large, if not fill, represent the ball as a single pixel.
        """
        
        # note that centre has already been adjusted based on the screen offset, so no need to include it here
        
        x_px,y_px = centre
        on_screen = self.body_on_screen(centre, radius)
    
        if on_screen:
            del_x = x_px - self.screen_centre[0]# - self.offset[0]
            del_y = y_px - self.screen_centre[1]# - self.offset[0]
            centre_diff = math.sqrt((del_x)**2 + (del_y)**2)
            
            far_away = centre_diff >= max_distance
            inside_screen = collision.circle_inside_rectangle((0,0), self.dims, centre, radius)
            
        
            if not far_away:
                if radius > int_max:
                    # int Overflow error, integer greater than standard c integer max_size.
                    if fill:
                        self.screen.fill(colour)
                        return
                    else:
                        radius = 0
                
                pygame.draw.circle(self.screen, colour, centre, radius)
        
            else:
                # When the radius is too large, the circle is no longer drawn correctly.
                # hence draw an approximate polygon and fill the area.
                
                if inside_screen:
                    self.screen.fill(colour)
                
                else:
                    points = collision.get_rectangle_circle_outline((0,0), self.dims, centre, radius)
                    
                    if len(points) > 2:
                        pygame.draw.polygon(self.screen, colour, points)
                    elif len(points) == 2:
                        pygame.draw.line(self.screen, colour, points[0], points[1], 1)
                    
                    elif len(points) == 1:
                        # only one point intersects so, draw the single point
                        pygame.draw.circle(self.screen, colour, (x_px,y_px),0)
                
                    else:
                        raise ValueError("Invalid length of points: {0}, to draw object '{1}'"\
                                         .format(points, name))






    @staticmethod
    def point_in_range(min,max, val):
        return min <= val < max
    
    
    def body_on_screen(self, centre, radius):
        return collision.rectangle_circle_collide((0,0), self.dims, centre, radius)

    
    
    def get_x_pix(self, X):
        #print(X)
        tmp_x = self.get_pixel(X.components[self.proj[0]] - self.centre[0])
        return tmp_x + self.screen_centre[0] + self.offset[0]
    def get_y_pix(self, X):
        tmp_y = self.get_pixel(X.components[self.proj[1]] - self.centre[1])
        return -tmp_y + self.screen_centre[1] + self.offset[1]
    
    
    ####################################
    # used to draw trails for objects
    # assume the vector is relative to the position of the object required.
    # move it relative to the current position of the vector
    # then centre it relative to the current position of the object
    # then centre it relative to the centre of the screen such that the object is at the centre.
    
    
    def get_x_pix_offset(self,X,Y):
        tmp_x = X.components[self.proj[0]] + Y.components[self.proj[0]]
        tmp_x = tmp_x - self.centre[0] # centre at current position of object.
        tmp_x = self.get_pixel(tmp_x)
        return tmp_x + self.screen_centre[0] + self.offset[0]
    
    def get_y_pix_offset(self, X,Y):
        tmp_y = X.components[self.proj[1]] + Y.components[self.proj[1]]
        tmp_y = tmp_y - self.centre[1] # centre at current position of object.
        tmp_y = self.get_pixel(tmp_y)
        return -tmp_y + self.screen_centre[1] + self.offset[1]


    #####  UNIVERSE

    def draw_2dprojection_universe(self, U:u.Universe, grid=False):
        """
        Given a universe object, draw all possible objects on the screen.
        This is done by calling draw_2dprojection_body object for each body object.
        """
        
        if U.wall != None:
            self.screen.fill(col.rgb_inverse(self.colour))
            
            w,h = self.dims
            x_min = self.offset[0]
            y_min = self.offset[1]
            x_max = x_min + w
            y_max = y_min + h
            
            #rt ==> top tight
            xrt = self.get_x_pix(U.wall)
            yrt = self.get_y_pix(U.wall)
        
            other_side = -U.wall
            #lb ==> bottom left
            xlb = self.get_x_pix(other_side)
            ylb = self.get_y_pix(other_side)
        
        
            if xrt > x_max:
                xrt = w
            if yrt < y_min:
                yrt = 0
            if xlb < x_min:
                xlb = 0
            if ylb > y_max:
                ylb = h

            pygame.draw.polygon(self.screen, self.colour, [(xlb,ylb),(xlb,yrt),(xrt,yrt),(xrt,ylb)])
        
        else:
            self.screen.fill(self.colour)
        
        self.draw_trails(U)
        
        for body in U.bodies:
            if isinstance(body, b.Body):
                self.draw_2dprojection_body(body)

        if grid:
            line_colour = col.rgb_inverse(self.colour)
            centre = self.default_centre()
            w,h = self.dims
            
            pygame.draw.line(self.screen, line_colour, (centre[0], 0),(centre[0], h-1), 2)
            pygame.draw.line(self.screen, line_colour, (0, centre[1]),(w-1, centre[1]), 2)




    #####  Trails

    def draw_trails(self, U:u.Universe):
        """
        Draw object path centre trails.
        """
        if U.display_trails:
        
            centre = U.centre
            if U.trail_id == 0:
                centre = U.get_centre_of_mass()
            elif U.trail_id > 0:
                tmp_bod = U.get_body(U.trail_id)
                if tmp_bod != None:
                    centre = tmp_bod.X
            
            
            for bod in U.bodies:
                
                tmp_trail = bod.trail_history
                trails = tmp_trail.get_history()
                
                colour = tmp_trail.colour

                i = 0
                n = len(trails)
                if n > 1:
                    old = trails[i]
                    if old == None:
                        raise TypeError("\nCannot Draw lines with None-type object.\n  '{0}'"\
                                        .format(trails))
                    
                    
                    old_x = self.get_x_pix_offset(old, centre)
                    old_y = self.get_y_pix_offset(old, centre)
                    
                    w = self.dims[0]
                    h = self.dims[1]
                    old_range = self.point_in_range(0, w, old_x) and self.point_in_range(0,h,old_y)
                    i += 1
    
                    while i < n:
                        #print(bod.name, old_x, old_y)
                        new = trails[i]
                        
                        if new == None:
                            raise TypeError("\nCannot Draw lines with None-type object.\n  '{0}'"\
                                            .format(trails))
                    
                        nx = self.get_x_pix_offset(new, centre)
                        ny = self.get_y_pix_offset(new, centre)
                        new_range = self.point_in_range(0, w, nx) and self.point_in_range(0,h,ny)
                        #print(new_range, (old_x,old_y),(nx,ny), bod.name)
                    
                        if old_range and new_range:
                            #print("DRAWING", (old_x,old_y),(nx,ny))
                            pygame.draw.line(self.screen, colour, (old_x,old_y),(nx,ny), 1)
                        i += 1

                        old_x,old_y = nx, ny
                        old_range = new_range



    #####  Message Function

    def message(self, text:str, font_size:int=18, colour:tuple=col.black, background_colour=None):
        default_font = pygame.font.get_default_font()
        font = pygame.font.SysFont(default_font, font_size)
        
        antialising = False
        text_screen = font.render(text, antialising, colour, background_colour)
        return text_screen


    def write_message(self, text:str, font_size:int=12, centre=(True,True),
                      text_colour:tuple=col.black, background_colour=None, second_size=None, offset=(0,0)):
        
        phrases = text.split("\n")
        
        
        tmp_screen = self.message("", font_size, text_colour, None)
        template_height = tmp_screen.get_height()
        
        total_height = template_height + offset[1]
        
        if second_size != None:
            tmp_screen = self.message("", second_size, text_colour, None)
            template_height = tmp_screen.get_height()
        
        total_height += template_height * (len(phrases)-1)
        
        screen_x, screen_y = self.screen_centre
        centre_x, centre_y = centre
        
        y = 0
        if centre_y:
            y = int(screen_y - total_height/2)
        
        i = 0
        while i < len(phrases):
            phrase = phrases[i]
            
            text_screen = self.message(phrase, font_size, text_colour, background_colour)

            text_width = text_screen.get_width()
            text_height = text_screen.get_height()
        
            x=offset[0]
            if centre_x:
                x += int(screen_x - (text_width/2))
            

            self.screen.blit(text_screen, (x,y))
            y += int(text_height)

            if i == 0:
                if second_size != None:
                    font_size = second_size
            i += 1
        return



    def write_label(self, text:str, colour=None, titleSize=False, centre=(False,False), size=-1, offset=(0,0)):
        textsize = self.label_size
        second_size = None
        
        if size > 0:
            second_size = size
        if titleSize:
            textsize = self.title_size
    
        if colour == None:
            colour = self.text_colour
        
        self.write_message(text, textsize, centre=centre, text_colour=colour,
                           background_colour=self.colour, second_size=second_size, offset=offset)


    def write_title_message(self, text:str, background=True, offset=(0,0)):
        back_colour = None
        if background:
            back_colour = col.rgb_inverse(self.text_colour)

        self.write_message(text, font_size=self.title_size, centre=(True,True), text_colour=self.text_colour,
                           background_colour=back_colour, offset=offset)






    ####### Pixels to vectors/points
    def get_x_pos(self, x):
        """
        pixel = x_pos /scale ==> x_pos = pixel*scale
        Centre has been shifted by centre[0]
        """
        relative_x = x# - self.screen_centre[0]# - self.offset[0]
        # no need for secondary part since find difference.
        return relative_x*self.scale + self.centre[0]

    def get_y_pos(self, y):
        """
        pixel = y_pos /scale ==> y_pos = pixel*scale
        """
        relative_y = -y# - self.screen_centre[1]# - self.offset[1]
        return relative_y*self.scale + self.centre[1]


    def get_pos_vector(self, pos, n):
        # n is the dimension of the vector
        x,y = pos
        
        vec = [0]*n
        x_pos = self.get_x_pos(x)
        y_pos = self.get_y_pos(y)

        vec[self.proj[0]] = x_pos
        vec[self.proj[1]] = y_pos

        return v.Vector(vec)


    def get_delta_pos_vector(self, pos1, pos2, n):
        x1,y1 = pos1
        x2,y2 = pos2

        vec = [0]*n
        x_pos1 = self.get_x_pos(x1)
        y_pos1 = self.get_y_pos(y1)
        x_pos2 = self.get_x_pos(x2)
        y_pos2 = self.get_y_pos(y2)
        
        vec[self.proj[0]] = x_pos2 - x_pos1
        vec[self.proj[1]] = y_pos2 - y_pos1

        return v.Vector(vec)





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

