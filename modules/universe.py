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
from modules import vector, metrics
from modules import constants
from modules import colour

import math,sys



class Universe:
    def __init__(self, centre:vector.Vector, *bodies):
        self.bodies = list(bodies)
        self.resistance = False
        self.max_id = len(bodies)
        self.centre = centre
        self.conserve_energy = False
        
        self.display_trails = False
        self.trail_id = -1
    
        # not implemented
        self.max_speed = -1
        self.relativistic = False
    
        self._nlaw = 2
        self._nmetric = 2
    
    def __repr__(self):
        body_str = ""
        for bod in self.bodies:
            body_str += str(bod) + "\n"
        
        string = "universe {{\ncentre: vector {0}\nresistance: {1}\nconserveEnergy: {2}\n{3}}}"\
                .format(self.centre, self.resistance, self.conserve_energy, body_str)
        return string
    

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
            return weighted_centre /mass
        




    #####  FIELDS - for each body object.

    def net_gravity_field(self, body_id, X:vector.Vector, dist_error):
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
                        tmp_field = other_body.gravity_field(X, dist_error, (self._nlaw, self._nmetric))
                        field = tmp_field + field
                i += 1
        return field


    def net_electric_field(self, body_id, X:vector.Vector, dist_error):
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
                        tmp_field = other_body.electric_field(X, dist_error, (self._nlaw, self._nmetric))
                        field = tmp_field + field
                i += 1
        return field



    #####  FORCES

    def net_gravity_force(self, body_id:int, X:vector.Vector, dist_error):
        """
        Given a body, calculate the net gravity field
        """
        bod = self.get_body(body_id)
        if bod == None:
            raise TypeError("Error: Cannot compute gravity force for None Object.")

        return bod.mass * self.net_gravity_field(body_id, X, dist_error)


    def net_electric_force(self, body_id:int, X:vector.Vector, dist_error):
        """
        Given a body, calculate the net electric field
        """
        bod = self.get_body(body_id)
        if bod == None:
            raise TypeError("Error: Cannot compute gravity force for None Object.")
                        
        return bod.charge * self.net_electric_field(body_id, X, dist_error)



    def net_force(self, body_id, X:vector.Vector, V:vector.Vector, dist_error):
        """
        Given a body, find the total force it experiences.
        """
        bod = self.get_body(body_id)
        F = self.net_gravity_force(body_id, X, dist_error) + self.net_electric_force(body_id, X, dist_error)

        if self.resistance:
            F = F + bod.resistance_force(V, (self._nlaw, self._nmetric))
        return F



    def net_acceleration(self, obj:body.Body, X:vector.Vector, V:vector.Vector, dist_error, warning):
        if obj.mass == 0:
            return vector.Vector.zero_vector(len(self.centre))
        else:
            V = self.correct_velocity(V, warning)
            #print(V.norm(), self.max_speed)
            
            # NON-RELATIVISTIC FORCES
            F = self.net_force(obj.id, X, V, dist_error)

            if self.relativistic:
                return self.relativistic_acceleration(obj.mass, V, F, warning)
            else:
                return F * ( 1 / obj.mass)



    def runge_kutta_method(self, obj:body.Body, t:float, dist_error:float, warning:bool):
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
        #force = self.net_force(obj.id, obj.X, obj.V)
        #print("Inital Force:",force, obj.name)

        kv1 = self.net_acceleration(obj, obj.X, obj.V, dist_error, warning)
        kx1 = obj.V

        kv2 = self.net_acceleration(obj, obj.X + kx1*(t/2), obj.V + kv1*(t/2), dist_error, warning)
        kx2 = obj.V + (t/2) * kv1

        kv3 = self.net_acceleration(obj, obj.X + kx2*(t/2), obj.V + kv2*(t/2), dist_error, warning)
        kx3 = obj.V + (t/2) * kv2

        kv4 = self.net_acceleration(obj, obj.X + kx3*t, obj.V + kv3*t, dist_error, warning)
        kx4 = obj.V + kv3*t

        #new_v = obj.V + (t/6) * (kv1 + 2*kv2 + 2*kv3 + kv4)
        #new_x = obj.X + (t/6) * (kx1 + 2*kx2 + 2*kx3 + kx4)
        
        del_v = (t/6) * (kv1 + 2*kv2 + 2*kv3 + kv4)
        del_x = (t/6) * (kx1 + 2*kx2 + 2*kx3 + kx4)
        
        new_v = obj.V + del_v
        new_x = obj.X + del_x
        new_v = self.correct_velocity(new_v, warning)

        # Update Position and Velocity Vectors
        obj.X_prev = obj.X
        obj.V_prev = obj.V

        obj.X = new_x
        obj.V = new_v
        
        #print("Position:",obj.X, obj.X_prev, del_x)
        #print("Velocity:",obj.V, obj.V_prev, del_v)
        return None




    def update_all_bodies(self, t:float, dist_error:float, warning:bool):
        """
        Use numeric methods to update the velocities and positions of ALL of the Body objects.
        """
        N = len(self.bodies)
        i = 0
        while i < N:
            bod = self.bodies[i]
            
            if isinstance(bod, body.Body):
                
                # update only if non-anchor:
                if not bod.anchor:
                    # Apply numeric method
                    self.runge_kutta_method(bod, t, dist_error, warning)
                    
                    """
                    if self.display_trails:
                        trail = bod.trail_history
                        #X = bod.X - self.trail_centre  #looks so bad not even funny
                        trail.add_history(bod.X)
                    """
                
                    if self.conserve_energy:
                        """
                        Need to implement field potentials and kinetic enegy.
                        U+K = const, U potential, K kinetic
                        """
                        NotImplemented
            i += 1
        if self.display_trails:
            self.add_trails()
        return None
    
    
    def clear_trails(self):
        for bod in self.bodies:
            if isinstance(bod, body.Body):

                t = bod.trail_history
                t.num = 0
                t.head = None
                t.tail = None
        return


    def update_trail_track(self, track_id):
        self.trail_id = track_id
        return self.add_trails()


    def add_trails(self):
        #input()
        """
        Add trails, with track_id
        """
        id = self.trail_id
        
        trail_centre = self.centre
        if id == 0:
            trail_centre = self.get_centre_of_mass()
        elif id > 0:
            tmp_bod = self.get_body(id)
            if tmp_bod != None:
                trail_centre = tmp_bod.X
    
        for bod in self.bodies:
            if isinstance(bod, body.Body):
                
                t = bod.trail_history
                X = bod.X - trail_centre
                t.add_history(X)
                #print(X, bod.X, trail_centre, bod.name)
                #print(bod.name)
                #print()
        return




    # speed limit
    
    def correct_velocity(self, V, warning):
        # SOURCE OF POTENTIAL ERRORS: del_x may not correct in runge-kutta method.
        c = self.max_speed
        if self.max_speed >= 0:
            v = 0
            if self._nmetric == 2:
                v = V.norm()
            else:
                v = metrics.metric_norm(V,self._nmetric)
            if v > c:
                c_v = (c/v)
                if c_v * v > 1.0:
                    if warning:
                        print("WARNING: adjusted speed limit is still faster than light\n v={0}\n c={1}"
                              .format(v,c))
                    c_v = 0.99999999*c_v
                
                V = V * c_v
    
        return V





    # relativistic properties


    def lorentz_factor(self, v:vector.Vector) -> float:
        """
        Find the lorentz factor for a particular speed.
        y = 1/ sqrt{1-v^2/c^2}
        """
        if self.max_speed < 0:
            return 1  # symbolises infinite max speed.
        elif self.max_speed == 0:
            raise ValueError("\nCannot find lorentz factor for universe with Speed Limit of 0.")
        else:
            v_sqr = 0
            if self._nmetric == 2:
                v_sqr = vector.Vector.inner_product(v,v)
            else:
                v_sqr = metrics.metric_norm(v,self._nmetric) ** 2
            
            c_sqr = self.max_speed * self.max_speed
            if v_sqr > c_sqr:
                raise ValueError("\nVelocity faster than the Universal Speed limit.\n  Vector: {0}\n  Object Speed: {1}\n  Max Speed: {2}"\
                                 .format(v, math.sqrt(v_sqr), self.max_speed))
            elif v_sqr == c_sqr:
                return float(sys.maxsize)
            return 1 / math.sqrt(1 - v_sqr/c_sqr)


    def relativistic_acceleration(self, mass, V, force, warning):
        """
        See here for more information about relativistic forces:
        https://en.wikipedia.org/wiki/Relativistic_mechanics#Force
        """
        # SPECIAL RELATIVISTIC CALCULATIONS
        if self.max_speed > 0:
            mass = self.lorentz_factor(V) * mass
            c_sqr = self.max_speed * self.max_speed
            
            if self._nmetric != 2 and not warning:
                print("Warning: Inner product is ill defined for other non-euclidean metrics.")
            force = force - vector.Vector.inner_product(V,force)*V / (c_sqr)
        return force/mass



    def conform_body_speeds(self):
        c = self.max_speed
        if (c > 0 and self.relativistic) or (c >= 0 and not self.relativistic):
            for bod in self.bodies:
                v = 0
                if self._nmetric == 2:
                    v = bod.V.norm()
                else:
                    v = metrics.metric_norm(V,self._nmetric)

                if v > c:
                    name = ""
                    if bod.name != "":
                        name = bod.name
                    else:
                        name = "Body " + str(bod.id)
                    print("Warning: {0} has speed faster than Universal Speed limit c={1}\n V={2}, v={3}\n Adjusting speed..."\
                          .format(name, c, bod.V, v))

                    tmp_V = bod.V * (c/v)
                    bod.V = tmp_V
                    bod.V_prev = tmp_V
        elif self.relativistic:
            raise ValueError("\nUniverse set to relativistic, however, there exists no valid positive universal speed limit.")
        return









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

