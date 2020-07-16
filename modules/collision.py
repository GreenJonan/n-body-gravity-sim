from modules import metrics
from modules import vector
import math



def particle_circle_collide(centreA, radius, point):
    """
    Assume all the measurements are in pixels. Return if point collides with circle A
    """

    return (centreA[0] - point[0])**2 + (centreA[1] - point[1])**2 <= radius**2



def n_sphere_collide(centreA, radiusA, centreB, radiusB, nmetric=2):
    """
    Find whether two spheres intersect.
    Also consider convex and concave p-spheres.
    """
    distance = metrics.general_n_euclid_metric(centreA, centreB, nmetric)
        
    collision = distance < radiusA + radiusB
            
            
    # for convex objects, collision occurs when the distance
    if nmetric >= 1:
        # convex
        pass # collision test already done
        
    else:
        # concave
                        
        # for concave objects, need to check all the corners.
        #                                                   ^
        # Rotation is simple, always orientated like this  < >
        #                                                   v
        cont = not collision
        n = len(centreA)
        corner_ls = list(centreA.components)
        i = 0
            
        while cont:
            if i == n:
                cont = False
            else:
                corner_ls[i] = corner_ls[i] + radiusA
                corner_vec = vector.Vector(corner_ls)
                
                collision = metrics.general_n_euclid_metric(corner_vec, centreB, nmetric) < radiusB
                cont = not collision
                                                                                    
                corner_ls[i] = corner_ls[i] - radiusA
                                    
                if cont:
                    corner_ls[i] = corner_ls[i] - radiusA
                    corner_vec = vector.Vector(corner_ls)
                    
                    collision = metrics.general_n_euclid_metric(corner_vec, centreB, nmetric) < radiusB
                    cont = not collision
                        
                    corner_ls[i] = corner_ls[i] + radiusA
                    i += 1

    return collision



def rectangle_circle_collide(corner_rec:tuple, dims:tuple, centre_circ:tuple, radius):
    """
    Given a rectangle and a circle, find if they overlap in anyway.
    Co-ordinate system is assumed to be parallel to the sides of the rectangle.
    Results taken from:
    https://yal.cc/rectangle-circle-intersection-test/
    
    Let the corner be the bottom left, ie.e one at the origin.
    """
    
    if circle_inside_rectangle(corner_rec,dims,centre_circ,radius):
        return True
    else:
         return rectangle_circle_intersect(corner_rec, dims, centre_circ, radius)




def circle_inside_rectangle(corner_rec:tuple, dims:tuple, centre_circ:tuple, readius:float):
    w,h = dims
    r_x,r_y = corner_rec
    c_x,c_y = centre_circ
    
    # check if circle inside rectangle
    if r_x <= c_x < r_x+w and r_y <= c_y < r_y+h:
        return True
    else:
        return False



def rectangle_circle_intersect(corner_rec:tuple, dims:tuple, centre_circ:tuple, radius):
    """
    Find if the boundaries of either shape intersect
    """

    nearest_x,nearest_y = get_rectangle_nearest_circle(corner_rec, dims, centre_circ)
    
    c_x,c_y = centre_circ
    
    del_x = c_x - nearest_x
    del_y = c_y - nearest_y
    return del_x**2 + del_y**2 < radius**2




def get_rectangle_nearest_circle(corner_rec:tuple, dims:tuple, centre_circ:tuple):
    """
    Get the points on the rectangle closest to the centre of the circle.
    """
    w,h = dims
    r_x,r_y = corner_rec
    c_x,c_y = centre_circ
    
    nearest_x = max(r_x, min(c_x, r_x+w))
    nearest_y = max(r_y, min(c_y, r_y+h))
    return nearest_x, nearest_y






def get_rectangle_circle_outline(corner_rec:tuple, dims:tuple, centre_circ:tuple, radius):
    """
    Given a circle that is sufficiently far away from the screen and large enough that it still intersects,
    find the polygon points that represent an approximation.
    """
    c_x,c_y = centre_circ
    r_x,r_y = corner_rec
    w,h = dims
    
    rx_max = r_x + w-1
    rx_min = r_x
    ry_max = r_y + h-1
    ry_min = r_y
    
    rt_dist = (rx_max - c_x)**2 + (ry_max - c_y)**2
    rb_dist = (rx_max - c_x)**2 + (ry_min - c_y)**2
    lt_dist = (rx_min - c_x)**2 + (ry_max - c_y)**2
    lb_dist = (rx_min - c_x)**2 + (ry_min - c_y)**2
    r_sqr = radius**2
    
    if rt_dist <= r_sqr and rb_dist <= r_sqr and lt_dist <= r_sqr and lb_dist <= r_sqr:
        # screen inside circle.
        return (rx_min, ry_min), (rx_min, ry_max), (rx_max, ry_max), (rx_max, ry_min)

    return get_rectangle_circle_intersection_points(corner_rec, dims, centre_circ, radius)





def get_rectangle_circle_intersection_points(corner_rec:tuple, dims:tuple, centre_circ:tuple, radius:float):
    """
    Suppose the boundary of the circle intersects with the boundary of the rectangle,
    find the two points that it intersects with.
    """
    
    def get_point(ls,side):
        # given a side, find the first point.
        # 0,1,2,3 ==> left,right,top,bottom
        p1 = ls[2*side]
        if p1 == None:
            return ls[2*side+1]
        else:
            return p1
                

    #side 1 (s), side 2 (t)
    s = (0,0)
    t = (0,0)
    
    c_x,c_y = centre_circ
    r_x,r_y = corner_rec
    w,h = dims


    # everything ordered left,right,top,bottom

    #points,sides = get_side_points(corner_rec, dims, centre_circ, radius)
    points = rectangle_circle_intersection(corner_rec, dims, centre_circ, radius)
    
    circle_left, circle_right,circle_above,circle_below = False, False, False, False
    
    
    rx_max = r_x + w-1
    rx_min = r_x
    ry_max = r_y + h-1
    ry_min = r_y
    
    if c_x <= rx_min:
        circle_left = True
    elif c_x >= rx_max:
        circle_right = True

    if c_y >= ry_min:
        circle_above = True
    elif c_y <= ry_max:
        circle_below = True

    left_side = points[0] != None or points[1] != None
    right_side = points[2] != None or points[3] != None
    top_side = points[4] != None or points[5] != None
    bottom_side = points[6] != None or points[7] != None


    # test to make sure at most two sides comply:
    val = 0
    if left_side: val += 1
    if right_side: val += 1
    if top_side: val += 1
    if bottom_side: val += 1

    if val > 2:
        raise ValueError("Circle approximation intersects with more than two sides of screen.")
    else:
        if val == 1:
            # Maximum two points of intersection.
            p1 = None
            p2 = None
            found = False
            
            i = 0
            while i < 8 and not found:
                tmp = points[i]
                
                if p1 != None:
                    found = True
                    if tmp != None:
                        p2 = tmp
        
                else:
                    if tmp != None:
                        p1 = tmp
                i += 1
            
            if p2 != None:
                return (p1,p2)
            elif p1 != None:
                return tuple(p1)
            else:
                raise ValueError("Single line of rectangle intersects with circle, however, no points on the line intersect.")

        elif val == 2:
            
            if left_side and right_side:
                left = get_point(points,0)
                right = get_point(points,1)

                if circle_below:
                    return left, right, (rx_max,ry_min), (rx_min,ry_min)
                else:
                    return right,left, (rx_min,ry_max), (rx_max,ry_max)
                
                
            elif left_side and top_side:
                left = get_point(points,0)
                top = get_point(points,2)
                    
                if not circle_below and not circle_right:
                    return left, (rx_min,ry_max), top
                else:
                    return left, top,(rx_max,ry_max), (rx_max,ry_min), (rx_min,ry_min)
                        
            
            elif left_side and bottom_side:
                left = get_point(points,0)
                bottom = get_point(points,3)
                    
                if not circle_right and not circle_above:
                    return left, bottom, (rx_min,ry_min)
                else:
                    return bottom, left, (rx_min,ry_max), (rx_max,ry_max), (rx_max,ry_min)
                        
                        
            elif right_side and top_side:
                right = get_point(points,1)
                top = get_point(points,2)
            
                if not circle_left and not circle_below:
                    return right, top, (rx_max,ry_max)
                else:
                    return top, right, (rx_max,ry_min), (rx_min,ry_min), (rx_min,ry_max)
                    

            elif right_side and bottom_side:
                right = get_point(points,1)
                bottom = get_point(points,3)

                if not circle_left and not circle_above:
                    return bottom, right, (rx_max,ry_min)
                else:

                    return right, bottom, (rx_min, ry_min),(rx_min,ry_max), (rx_max,ry_max)

            elif top_side and bottom_side:
                top = get_point(points,2)
                bottom = get_point(points,3)

                if circle_left:
                    return top, bottom, (rx_min,ry_min), (rx_min,ry_max)
                else:
                    return bottom, top, (rx_max,ry_max), (rx_max,ry_min)
    
            else:
                raise ValueError("Unknown side combinations for Circle Approximation")


        elif val == 0:
            raise ValueError("Circle approximation intersects with no sides of the screen.")
        else:
            raise ValueError("Circle approximation intersects with too many sides of the screen.\n side number = {0}"\
                             .format(val))





def rectangle_circle_intersection(rect_corner, dims, centre_circ, radius):
    """
    Suppose you have a rectangle, botom left corner given by rect_corner & width,height by dims.
    Consider the boundary points in which it intersects with a circle centred at centre_circ with radius radius.
    
    Return these boundary points.
    """
    
    r_x,r_y = rect_corner
    w,h = dims
    c_x,c_y = centre_circ
    
    x_min = r_x
    x_max = r_x+w-1
    y_min = r_y
    y_max = r_y+h-1
    
    
    left = line_circle_intersection(0,x_min, c_x,c_y,radius, vertical=True)
    right = line_circle_intersection(0,x_max, c_x,c_y,radius, vertical=True)
    top = line_circle_intersection(0,y_max, c_x,c_y,radius, vertical=False)
    bottom = line_circle_intersection(0,y_min, c_x,c_y,radius, vertical=False)

    
    # the two values are the points of intersection
    # Consider line segments, left,right,top, bottom, in which the circle intersects.
    
    # at most 8 points can intersect with the circle on the rectangle.
    intersection_points = [None] * 8
    
    #consider left
    # these are points on the vertical line at rx_min and bounded by ry_max <= y <= ry_max
    point1,point2 = left
    
    # both are none or neither or none
    
    if point1 != None:
        x1,y1 = point1
        x2,y2 = point2
    
        #assert x1 == x2 and x1 == x_min, "x points on the left side should correspond to the left.\n Expected: x = {0}\n Received: x = {1}, {2}".format(x_min,x1,x2)
    
        if y_min <= y1 <= y_max:
            intersection_points[0] = point1
        if y_min <= y2 <= y_max:
            intersection_points[1] = point2


    # likewise, consider right points
    point1,point2 = right

    if point1 != None:
        x1,y1 = point1
        x2,y2 = point2
        
        #assert x1 == x2 and x1 == x_max, "x points on the right side should correspond to the right.\n Expected: x = {0}\n Received: x = {1}, {2}".format(x_max,x1,x2)
        
        if y_min <= y1 <= y_max:
            intersection_points[2] = point1
        if y_min <= y2 <= y_max:
            intersection_points[3] = point2



    ###  top and bottom:
    
    # top
    point1,point2 = top
    
    if point1 != None:
        x1,y1 = point1
        x2,y2 = point2
        
        #assert y1 == y2 and y1 == y_max, "y points on the top side should correspond to the top.\n Expected: y = {0}\n Received: y = {1}, {2}".format(y_max,y1,y2)
        
        if x_min <= x1 <= x_max:
            intersection_points[4] = point1
        if x_min <= x2 <= x_max:
            intersection_points[5] = point2


    # bottom
    point1,point2 = bottom
    
    if point1 != None:
        x1,y1 = point1
        x2,y2 = point2
        
        #assert y1 == y2 and y1 == y_min, "y points on the bottom side should correspond to the bottom.\n Expected: y = {0}\n Received: y = {1}, {2}".format(y_min,y1,y2)
        
        if x_min <= x1 <= x_max:
            intersection_points[6] = point1
        if x_min <= x2 <= x_max:
            intersection_points[7] = point2


    return intersection_points


    """
    p1,p2 = line_circle_intersection(m,b, w,h,r, vertical)
    
    print(p1,p2)

    r_x,r_y = rect_corner
    width,height = dims
    
    give_p1 = True
    give_p2 = True

    if vertical:
        # then left or right wall
        # check that y is within bounds.
        y1,y2 = p1[1],p2[1]
                
        if r_y <= y1 < r_y + height:
            pass
        else:
            give_p1 = False
                    
        if r_y <= y2 < r_y + height:
            pass
        else:
            give_p2 = False
                    
    else:
        # horizontal
        # check x within bounds.
        x1,x2 = p1[0],p2[0]
    
        if r_x <= x1 < r_x + height:
            pass
        else:
            give_p1 = False

        if r_x <= x2 < r_x + height:
            pass
        else:
            give_p2 = False

    if give_p1 and give_p2:
        return p1,p2
    elif give_p1:
        return p1,None
    elif give_p2:
        return p2,None
    else:
        return None,None
"""


def line_circle_intersection(m,d, w,h,r, vertical=False):
    # Case 1
    # line:   y = mx+d
    # circle: (x-w)^2 + (y-h)^2 = r^2
    # solution: (m^2+1)x^2 + 2(m(d-h)-w)x + (w^2+(d-h)^2 - r^2) = 0, y = mx+b

    # or Case 2
    # line: x = a
    # solution (y-h)^2 = r^2 - (a-w)^2

    if not vertical:
        # case 1

        # ax^2 + bx + c = 0   ==> x = {}/2a
        # a != 0 so all good, need to check discriminant

        a = m*m + 1
        b = 2* (m * (d-h) - w)
        c = w**2 + (d-h)**2 - r**2
        
        discriminant = b*b - 4*a*c
        if discriminant < 0:
            return None,None
        else:
            x1,x2 = (-b - math.sqrt(discriminant))/(2*a), (-b + math.sqrt(discriminant))/(2*a)

            y1 = m*x1+d
            y2 = m*x2+d

            return (x1,y1), (x2,y2)

    else:
        a = d
        discriminant = r**2 - (a-w)**2
        if discriminant < 0:
            return None, None
        else:
            y1,y2 = h - math.sqrt(discriminant), h + math.sqrt(discriminant)

            return (a,y1), (a,y2)
