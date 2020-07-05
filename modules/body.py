"""
This module outlines the 'body' object. These objects are the particles of the simulation.
Forces act on these objects, and they generate a field around them.
"""
import vector
import metrics
import constants



class Body:
    def __init__(self, id, X0, V0, m=1, r=1, q=0, colour=constants.black):
        """
        Construct the body object.
        :X0: gives the intial position of the object
        :V0: gives the inital velocity of the object
        :m: - inertial and gravitational mass. Recall F=ma
        :r: - radius of the object, assume sphere
        :q: - charge of the object, used to give secondary force, independent of inertial mass.
        :id: - identification number for object.
        """

        if isinstance(X0, vector.Vector):
            self.X = X0
        else:
            self.X = vector.Vector(X0)
        if isinstance(V0, vector.Vector):
            self.V = V0
        else:
            self.V = vector.Vector(V0)

        self.mass = m
        self.radius = r
        self.charge = q
        self.id = id
        self.colour = colour



    #####  FIELD GENERATED BY SELF
    
    def gravity_field(self, X):
        """
        Return the gravity field value at position X, as a result of body: self
        
        F = - G*m1*m2 / r^2  * r_unit  ==>  C = - G*m/r^2  * r_unit
        if r_unit is not unit vector, then take r^3 instead of r^2
        """
        return constants.G_const * self.mass * metrics.inverse_square_law(X,self.X)
    
    
    def electric_field(self, X):
        """
        Return the gravity field value at position X, as a result of body: self
            
        Like with gravitational field, V = E * q / r^2  * r_unit
        """
        return constants.E_const * self.charge * metrics.inverse_square_law(self.X,X)



    #####  GENERAL FORCES
    
    def gravity_force(self, t, universe):
        """
        Find gravity force at time t.
        
        F = mC, where C is the gravitational field.
        """
        return #universe.
    
    def electric_force(self, t):
        """
        Find electric force at time t.
        """
        return
    
    def resistance_force(self, vel:vector.Vector):
        # F = -R*A*v^2
        area = self.radius * self.radius * math.pi
        return  - R_const * area * vel.norm() * vel


