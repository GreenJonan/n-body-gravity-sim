"""
This module outlines how bodies interact within a closed system.
Treat all the bodies as a universe. Have reference to each body.

For all bodies generated into the universe, they have an id number.
Every time a body is created, the max_id values increases.
"""
#import body
#import vector
#import constants
#import colour

from modules import body
from modules import vector
from modules import constants
from modules import colour



class Universe:
    def __init__(self, centre:vector.Vector, *bodies):
        self.bodies = list(bodies)
        self.resistance = False
        self.max_id = len(bodies)
        self.centre = centre
        self.conserve_energy = False
    

    def add_body(self, X0, V0, m=1, r=1, q=0, colour=colour.black, name=""):
        self.max_id += 1
        new_body = body.Body(self.max_id, X0, V0, m=m, r=r, q=q,
                             colour=colour, name=name)
        self.bodies.append(new_body)
        return new_body


    def get_body(self, body_id):
        return self.bodies[body_id-1]



    def turn_on_resistance(self):
        self.resistance = True
        self.conserve_energy = False
    
    def conserve_universe_energy(self):
        if self.resistance:
            raise ValueError("Error: Cannot conserve total energy while not-conservative forces are active.")
        self.conserve_energy = True



    #####  UNIVERSE VECTORS:
    
    def get_centre_of_mass(self):
        N = len(self.bodies)
        if N == 0:
            raise ValueError("Error: Unable to compute Centre of Mass, no Objects in Universe.")
    
        n = len(self.centre)
        weighted_centre = vector.Vector.zero_vector(n)
        mass = 0
            
        i = 0
        while i < N:
            bod = self.bodies[i]
            if isinstance(bod, body.Body):
                mass += bod.mass
                weighted_centre = weighted_centre + bod.mass * bod.X
            i += 1

        if mass == 0:
            return weighted_centre
        else:
            return weighted_centre * (1/mass)
        




    #####  FIELDS - for each body object.

    def net_gravity_field(self, body_id, X:vector.Vector):
        """
        Calculate the gravitational field at the location of the body.
        :input: id number for body
        :return: vector
        """

        bod = self.get_body(body_id)
        n = len(bod.X)
        field = vector.Vector.zero_vector(n)

        if bod.mass == 0:
            pass
        else:
            N = len(self.bodies)
            i = 0
            while i < N:
                other_body = self.bodies[i]
                
                if isinstance(other_body, body.Body):
                    if other_body.id == body_id:
                        pass # dont compute field between self
                    else:
                        tmp_field = other_body.gravity_field(X)
                        field = tmp_field + field
                i += 1
        return field


    def net_electric_field(self, body_id, X:vector.Vector):
        """
        Calculate the electric field at the location of the body.
        :input: id number for body
        :return: vector
        """

        bod = self.get_body(body_id)
        n = len(bod.X)
        field = vector.Vector.zero_vector(n)
        
        if bod.charge == 0:
            pass
        else:
            N = len(self.bodies)
            i = 0
            while i < N:
                other_body = self.bodies[i]
                
                if isinstance(other_body, body.Body):
                    if other_body.id == body_id:
                        pass # dont compute field between self
                    else:
                        tmp_field = other_body.electric_field(X)
                        field = tmp_field + field
                i += 1
        return field



    #####  FORCES

    def net_gravity_force(self, body_id:int, X:vector.Vector):
        """
        Given a body, calculate the net gravity field
        """
        bod = self.get_body(body_id)
        if bod == None:
            raise TypeError("Error: Cannot compute gravity force for None Object.")

        return bod.mass * self.net_gravity_field(body_id, X)


    def net_electric_force(self, body_id:int, X:vector.Vector):
        """
        Given a body, calculate the net electric field
        """
        bod = self.get_body(body_id)
        if bod == None:
            raise TypeError("Error: Cannot compute gravity force for None Object.")
                        
        return bod.charge * self.net_electric_field(body_id, X)



    def net_force(self, body_id, X:vector.Vector, V:vector.Vector):
        """
        Given a body, find the total force it experiences.
        """
        bod = self.get_body(body_id)
        F = self.net_gravity_force(body_id, X) + self.net_electric_force(body_id, X)

        if self.resistance:
            F = F + bod.resistance_force(V)
        return F




    def runge_kutta_method(self, obj:body.Body, t:float):
        """
        Update the position and velocity of the object.
            
        The method is taken directly from:
        http://spiff.rit.edu/richmond/nbody/OrbitRungeKutta4.pdf
        
        y'=f(y,t) y=y0
        y_{i+1} = y_{n} + h/6 (k1 + 2*k2 + 2*k3 + k4)
        
        where, k1 = f(y,t)   k2 = f(y+k1*h/2, t+h/2)   k3 = f(y+k2*h/2, t+h/2)   k4 = f(t+h, y+k4*h)
        
        y'=f(y,t) is interpreted as,
        v' = f(v,x), v=v0
        
        and, 
        x' = vt
        
        where of course v' = a = F/m
        
        :input:  Body object, and t - time step (h in above equations)
        :return: None, update body direction only
        """
        force = self.net_force(obj.id, obj.X, obj.V)
        #print("Inital Force:",force, obj.name)

        kv1 = force *( 1 / obj.mass)
        kx1 = obj.V

        kv2 = self.net_force(obj.id, obj.X + kx1*(t/2), obj.V + kv1*(t/2)) *( 1 / obj.mass)
        kx2 = obj.V + (t/2) * kv1

        kv3 = self.net_force(obj.id, obj.X + kx2*(t/2), obj.V + kv2*(t/2)) *( 1 / obj.mass)
        kx3 = obj.V + (t/2) * kv2

        kv4 = self.net_force(obj.id, obj.X + kx3*t, obj.V + kv3*t) *( 1 / obj.mass)
        kx4 = obj.V + kv3*t

        #new_v = obj.V + (t/6) * (kv1 + 2*kv2 + 2*kv3 + kv4)
        #new_x = obj.X + (t/6) * (kx1 + 2*kx2 + 2*kx3 + kx4)
        
        del_v = (t/6) * (kv1 + 2*kv2 + 2*kv3 + kv4)
        del_x = (t/6) * (kx1 + 2*kx2 + 2*kx3 + kx4)
        
        new_v = obj.V + del_v
        new_x = obj.X + del_x

        # Update Position and Velocity Vectors
        obj.X_prev = obj.X
        obj.V_prev = obj.V

        obj.X = new_x
        obj.V = new_v
        
        #print("Position:",obj.X, obj.X_prev, del_x)
        #print("Velocity:",obj.V, obj.V_prev, del_v)
        return None




    def update_all_bodies(self, t:float):
        """
        Use numeric methods to update the velocities and positions of ALL of the Body objects.
        """
        #print()
        N = len(self.bodies)
        i = 0
        while i < N:
            bod = self.bodies[i]
            if isinstance(bod, body.Body):
                # Apply numeric method
                self.runge_kutta_method(bod, t)
                
                if self.conserve_energy:
                    """
                    Need to implement field potentials and kinetic enegy.
                    U+K = const, U potential, K kinetic
                    
                    """
                    NotImplemented
            i += 1
        return None







if __name__ == "__main__":
    zero_vec = vector.Vector.zero_vector(2)
    v1 = vector.Vector([1,0])
    v2 = vector.Vector([-1,0])
    
    b1 = body.Body(1, v1, zero_vec)
    b2 = body.Body(2, v2, zero_vec)
    
    u = Universe(zero_vec, b1, b2)
    
    
    print(u.net_force(b1.id, b1.X, b1.V))
    i = 0
    while i < 20:
        u.runge_kutta_method(b1, 1)
        print(u.net_force(b1.id, b1.X, b1.V))
        i += 1

