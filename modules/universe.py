"""
This module outlines how bodies interact within a closed system.
Treat all the bodies as a universe. Have reference to each body.

For all bodies generated into the universe, they have an id number.
Every time a body is created, the max_id values increases.
"""
import body
import vector
import constants



class Universe:
    def __init__(self, scale, centre:vector.Vector, *bodies):
        self.bodies = list(bodies)
        self.resistance = False
        self.max_id = len(bodies)
        self.scale = scale
        self.centre = centre
    

    def add_body(self, X0, V0, m=1, r=1, q=0):
        self.max_id += 1
        new_body = body.Body(self.max_id, X0, V0, m, r, q)
        self.bodies.append(new_body)
        return new_body


    def get_body(self, body_id):
        return self.bodies[body_id-1]





    #####  FIELDS - for each body object.

    def gravity_field(self, body_id):
        """
        Calculate the gravitational force an object experiences.
        That is, find the field at the position given by 'body_id'
        """

        body = self.get_body(body_id)
        n = len(body.X)
        field = vector.Vector([0] * n)

        if body.mass == 0:
            pass
        else:
            N = len(self.bodies)
            i = 0
            while i < N:
                other_body = self.bodies[i]
                if other_body == None:
                    pass # body removed
                elif other_body.id == body_id:
                    pass # dont compute field between self
                else:
                    tmp_field = other_body.gravity_field(body.X)
                    field = tmp_field + field
                i += 1
        return field


    def electric_field(self, body_id):
        """
        Not implemented.
        """

        body = self.get_body(body_id)
        n = len(body.X)
        field = vector.Vector( [0] * n )
        return field
