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
from modules import collision as Collide
from modules import utility

import math,sys



class Universe:
    def __init__(self, centre:vector.Vector, *bodies):
        self.bodies = list(bodies)
        self.resistance = False
        self.max_id = len(bodies)
        self.conserve_energy = False  #not implemented
        
        self.centre = centre
        self.wall = None
        self.elasticity = 1
        self.all_wall_collide = True
        
        self.display_trails = False
        self.trail_id = -1
    
        # not implemented
        self.max_speed = -1
        self.relativistic = False
    
        self._nlaw = 2
        self._nmetric = 2
    
        self.assertion = False
        self.random = False
        self.shuffle = False
    
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

    def get_max_speed(self):
        if max_speed < 0:
            return sys.max_size
        else:
            return self.max_speed



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

    def net_gravity_field(self, body_id, X:vector.Vector, g_const, dist_error):
        """
        Calculate the gravitational field at the location of the body.
        :input: id number for body
        :return: vector
        """
        
        bod = self.get_body(body_id)
        n = len(bod.X)
        field = vector.Vector.zero_vector(n)

        if bod.mass == 0 or g_const == 0:
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
                        tmp_field = other_body.gravity_field(X, g_const, dist_error, (self._nlaw, self._nmetric))
                        field = tmp_field + field
                i += 1
        return field


    def net_electric_field(self, body_id, X:vector.Vector, e_const, dist_error):
        """
        Calculate the electric field at the location of the body.
        :input: id number for body
        :return: vector
        """

        bod = self.get_body(body_id)
        n = len(bod.X)
        field = vector.Vector.zero_vector(n)
        
        if bod.charge == 0 or e_const == 0:
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
                        tmp_field = other_body.electric_field(X, e_const, dist_error, (self._nlaw, self._nmetric))
                        field = tmp_field + field
                i += 1
        return field



    #####  FORCES

    def net_gravity_force(self, body_id:int, X:vector.Vector, g_const, dist_error):
        """
        Given a body, calculate the net gravity field
        """
        bod = self.get_body(body_id)
        if bod == None:
            raise TypeError("Error: Cannot compute gravity force for None Object.")

        return bod.mass * self.net_gravity_field(body_id, X, g_const, dist_error)


    def net_electric_force(self, body_id:int, X:vector.Vector, e_const, dist_error):
        """
        Given a body, calculate the net electric field
        """
        bod = self.get_body(body_id)
        if bod == None:
            raise TypeError("Error: Cannot compute gravity force for None Object.")
                        
        return bod.charge * self.net_electric_field(body_id, X, e_const, dist_error)



    def net_force(self, body_id, X:vector.Vector, V:vector.Vector, consts:tuple, dist_error):
        """
        Given a body, find the total force it experiences.
        """
        bod = self.get_body(body_id)
        F_G = self.net_gravity_force(body_id, X, consts[0], dist_error)
        F_E = self.net_electric_force(body_id, X, consts[1], dist_error)
        F = F_G + F_E

        if self.resistance or bod.drag:
            F = F + bod.resistance_force(V, consts[2], (self._nlaw, self._nmetric))
        return F



    def net_acceleration(self, obj:body.Body, X:vector.Vector, V:vector.Vector, consts, dist_error, warning):
        if obj.mass == 0:
            return vector.Vector.zero_vector(len(self.centre))
        else:
            V = self.correct_velocity(V, warning)
            #print(V.norm(), self.max_speed)
            
            # NON-RELATIVISTIC FORCES
            F = self.net_force(obj.id, X, V, consts, dist_error)

            if self.relativistic:
                return self.relativistic_acceleration(obj.mass, V, F, warning)
            else:
                return F * ( 1 / obj.mass)



    def runge_kutta_method(self, obj:body.Body, t:float, phys_consts:tuple, dist_error:float, warning:bool):
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
        #Updated maximum speed such that it is within bounds.
        # NOTE::: This means that conservation of momentum no longer applies if max_speed > 1
        # and non-relativistic.
        obj.V = self.correct_velocity(obj.V, warning)
        
        
        #force = self.net_force(obj.id, obj.X, obj.V)
        #print("Inital Force:",force, obj.name)

        kv1 = self.net_acceleration(obj, obj.X, obj.V, phys_consts, dist_error, warning)
        kx1 = obj.V

        kv2 = self.net_acceleration(obj, obj.X + kx1*(t/2), obj.V + kv1*(t/2), phys_consts, dist_error, warning)
        kx2 = obj.V + (t/2) * kv1

        kv3 = self.net_acceleration(obj, obj.X + kx2*(t/2), obj.V + kv2*(t/2), phys_consts, dist_error, warning)
        kx3 = obj.V + (t/2) * kv2

        kv4 = self.net_acceleration(obj, obj.X + kx3*t, obj.V + kv3*t, phys_consts, dist_error, warning)
        kx4 = obj.V + kv3*t

        #new_v = obj.V + (t/6) * (kv1 + 2*kv2 + 2*kv3 + kv4)
        #new_x = obj.X + (t/6) * (kx1 + 2*kx2 + 2*kx3 + kx4)
        
        del_v = (t/6) * (kv1 + 2*kv2 + 2*kv3 + kv4)
        del_x = (t/6) * (kx1 + 2*kx2 + 2*kx3 + kx4)
        
        new_v = obj.V + del_v
        new_x = obj.X + del_x
        new_v = self.correct_velocity(new_v, warning)

        # Update Position and Velocity Vectors
        #obj.X_prev = obj.X
        #obj.V_prev = obj.V
        
        obj.V = new_v
        # note should velocity be updated if it previously collided
        
        # see if body collides with other bodies
        collision, other_bodies = self.check_collision(obj, del_x)


        if collision:
            self.multi_momentum_collision(obj, other_bodies, random=self.random)
        else:
            wall_collision, normal, updated_del_x = self.check_wall_collision(obj, del_x)
            # updated_del_x is the del_x such that the object now lies on the wall.
            
            if wall_collision:
                obj.X = obj.X + updated_del_x
                self.wall_momentum_collision(obj, normal)
            
                # TO DO: apply multinary collision detection with other bodies and wall and so on etc.
                """
                # now move object again.
                remainder = metrics.metric_norm(del_x, self._nmetric) - metrics.metric_norm(updated_del_x, self._nmetric)
            
                if remainder > dist_error:
                    new_del_x = metrics.unit_vector(obj.V, self._nmetric) * remainder
                    second_collision, other_bodies = self.check_collision(obj, new_del_x)
        
                    if second_collision:
                        self.multi_momentum_collision(obj, other_bodies, random=self.random)
                """
                            
            else:
                obj.X = new_x
        
        
        
        
        #print("Position:",obj.X, obj.X_prev, del_x)
        #print("Velocity:",obj.V, obj.V_prev, del_v)
        return None




    def update_all_bodies(self, t:float, phys_consts:tuple, dist_error:float, warning:bool):
        """
        Use numeric methods to update the velocities and positions of ALL of the Body objects.
        """
        N = len(self.bodies)
        if self.shuffle:
            utility.knuth_shuffle(self.bodies)
        
        i = 0
        while i < N:
            bod = self.bodies[i]
            
            if isinstance(bod, body.Body):
                
                # update only if non-anchor:
                if not bod.anchor:
                    # Apply numeric method
                    self.runge_kutta_method(bod, t, phys_consts, dist_error, warning)
                    
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
                    name = bod.get_name()
                    print("Warning: {0} has speed faster than Universal Speed limit c={1}\n V={2}, v={3}\n Adjusting speed..."\
                          .format(name, c, bod.V, v))

                    tmp_V = bod.V * (c/v)
                    bod.V = tmp_V
                    bod.V_prev = tmp_V
        elif self.relativistic:
            raise ValueError("\nUniverse set to relativistic, however, there exists no valid positive universal speed limit.")
        return





    ######  Body collisions.
    
    def get_momentum(self):
        sum = vector.Vector.zero_vector(len(self.centre))
        for bod in self.bodies:
            if isinstance(bod,body.Body):
                sum += bod.mass * bod.V
        return sum


    
    """
    def naive_momentum_collision(self, bodA:body.Body, bodB:body.Body):
        ###
        Given two objects, suppose they collided, now find their final velocities.
        https://en.wikipedia.org/wiki/Coefficient_of_restitution
        
        This method is naive since u,v should be scalars and only the velcity perpendicular to the plane
        of intersectio  should be modified.
        ###

        if self.relativistic:
            print("Momentum collision NOT IMPLEMENTED for relativistic systems.")
            return

        # for newtonian mechanics:
        # if vA, vB final velocities, and uA, uB initial velocities, and mA, mB masses,
        # r coefficient of restitution,

        # vA = ((mA-mB*r)uA + mB(r+1)uB) / (mA + mB)
        # vB = ((mB-mA*r)uB + mA(r+1)uA) / (mA + mB)


        r = body.Body.get_coeff_restitution(bodA, bodB)
        uA = bodA.V
        uB = bodB.V
        mA = bodA.mass
        mB = bodB.mass
        
        if mA + mB == 0:
            print("Momentum collision NOT IMPLEMENTED for objects with net-zero mass.")
            return

        vA = ((mA-mB*r)*uA + mB*(r+1)*uB) / (mA + mB)
        vB = ((mB-mA*r)*uB + mA*(r+1)*uA) / (mA + mB)

        bodA.V = vA
        bodB.V = vB
        return
    """

    def momentum_collision(self, bodA:body.Body, bodB:body.Body):
        """
        Given two objects, suppose they collided, now find their final velocities.
        https://en.wikipedia.org/wiki/Coefficient_of_restitution
        
        The velocity along the plane of intersection is unchanged, but the perpendicular component is adjusted
        by the following:
        """
        metric = self._nmetric # 2
        
        if self.relativistic:
            #for relativistic systems, unknown.
            
            print("Momentum collision NOT IMPLEMENTED for relativistic systems.")
            return None,None


        else:
            #for newtonian mechanics:
            
            # if vA, vB final speed, and uA, uB initial speed, and mA, mB masses,
            # (along perpendicular component)
            # r coefficient of restitution,
        
            # vA = ((mA-mB*r)uA + mB(r+1)uB) / (mA + mB)
            # vB = ((mB-mA*r)uB + mA(r+1)uA) / (mA + mB)
            
            mA = bodA.mass
            mB = bodB.mass
            
            if mA + mB == 0:
                print("Momentum collision NOT IMPLEMENTED for objects with net-zero mass.")
                return None,None
            
            
            A_to_B = bodB.X - bodA.X
            
            d = metrics.metric_norm(A_to_B, metric)
            if d == 0:
                return None,None
        
            A_to_B_unit = A_to_B / d
            # this is the normal vector for the plane of intersection.

            # vector decomposition.
            projA = vector.Vector.inner_product(bodA.V, A_to_B_unit)
            projB = vector.Vector.inner_product(bodB.V, A_to_B_unit)
            vA_normal = projA * A_to_B_unit
            vB_normal = projB * A_to_B_unit

            vA_plane = bodA.V - vA_normal
            vB_plane = bodB.V - vB_normal


            # main calculation:
            uA = sign(projA) * metrics.metric_norm(vA_normal, metric)
            uB = sign(projB) * metrics.metric_norm(vB_normal, metric)

            r = body.Body.get_coeff_restitution(bodA, bodB)
            vA = ((mA-mB*r)*uA + mB*(r+1)*uB) / (mA + mB)
            vB = ((mB-mA*r)*uB + mA*(r+1)*uA) / (mA + mB)
            
            #new_vA_normal = (vA/uA)*vA_normal  #neg if swaps sign, pos if same sign as original
            #new_vB_normal = (vB/uB)*vB_normal
            
            new_vA_normal = vA * A_to_B_unit
            new_vB_normal = vB * A_to_B_unit
        
            VA = new_vA_normal + vA_plane
            VB = new_vB_normal + vB_plane


            # this is the maximum error allowed in terms of the ratio of the momenta before to after
            err = 6e-16

            if self.assertion:
                momenta_inital = mA*bodA.V + mB*bodB.V
                momenta_final  = mA*VA + mB*VB
                
                delta_momenta = momenta_final - momenta_inital
                
                delta_norm = delta_momenta.norm()
                inital_norm = momenta_inital.norm()
                final_norm = momenta_final.norm()
                
                
                
                if inital_norm == 0 and final_norm == 0:
                    pass
                else:
                    ratio = 0
                    if initial_norm > 0:
                        ratio = delta_norm / inital_norm
                    else:
                        ratio = delta_norm / final_norm
                
                    if ratio > err:
                        print(final_norm / inital_norm)
                        momenta_str = "Momenta before: {0}\nMomenta after:  {1}"\
                                      .format(momenta_inital, momenta_final)
                        momentaA_str = "Momenta A: {0}\n           {1}".format(mA*bodA.V, mA*VA)
                        momentaB_str = "Momenta B: {0}\n           {1}".format(mB*bodB.V, mB*VB)
                        warning_str = "MOMENTUM IS NOT CONSERVED\n ratio {0}, delta p = {1}"\
                                      .format(ratio, delta_norm)

                        assert ratio <= err, warning_str + "\n\n" + momenta_str + "\n\n" + momentaA_str + "\n\n" + momentaB_str
            
            return VA,VB



    def multi_momentum_collision(self, bod:body.Body, other_bodies:list, random=False):
        """
        let object 0 be bod, and object i be the i-th body in other_bodies.
        Suppose object i has a_i amount of it's initial momentum, 
        then vi = ai * vi', where vi' is the velocity returned from 'momentum_collision' function.
        
        Also:
        v0 = u0 + m1/m0 (u1-v1) + ... + mn/m0 (un-vn)
        Hence, function is undefined if mass of particle is zero.
        
        Defintion for m=0:
            velocity is the sum of velocities returned from 'momentum_collision' for self, but scaled such
            that it's velocity is max velocity.
        """
        if self.relativistic:
            print("Momentum collision NOT IMPLEMENTED for relativistic systems.")
            return
    
        #before = self.get_momentum()
    
        #net_vel = bod.V
        i = 0
        n = len(other_bodies)
        #body_num = 0
        
        
        #momentum_sum = vector.Vector.zero_vector(len(self.centre))
        #results = [None] * n
        
        index_array = None
        if random:
            index_array = utility.shuffle_index(n)
        
        # find all the velocities such that not None and hence find bodies in system to compute new momentum.
        while i < n:
            j = i
            if random:
                j = index_array[i]
            
            v0,vi = self.momentum_collision(bod, other_bodies[j])
            
            if v0 != None:
                #momentum_sum += vi*other_bodies[i].mass
                
                #body_num += 1
                #results[i] = (v0,vi)
                bod.V = v0
                other_bodies[j].V = vi
            i += 1
                
        return
        #new_momentum = self.get_momentum() - momentum_sum/body_num
        
        
        # THE CODE BELOW IS COMPLETELY PHYSICALLY WRONG!!!!!!
        # experimentally it appears that the naive method is actually the correct method
        # that is, update the velocities one by one with every object the object collides with.
        
        # the reason for this is the fact that conservation of momentum is equivalent to the idea that we
        # cannot distinguish between any frame of reference.
        # However, using the method below you can distinguish.
        # the results for multi-collisions are likely less accurate, however, they retain this key property.
        
        """
        i = 0
        j = 0
        # do proper update.
        while i < n:
            vels = results[i]
            if vels != None:
                bi = other_bodies[i]
                j += 1
                # this means the velocity was sucessfully calculated.
                
                scale_i = 0
                ###
                if random:
                    if j == body_num:
                        scale_i = sum
                    else:
                        scale_i = rnd.random() * sum
                    sum -= scale_i
                else:
                    scale_i = 1/body_num
                    #scale_i = 1
                ###
                    

                v0,vi = vels
                tmp_delta0 = bod.mass * (v0 - bod.V) + bi.mass * (vi - bi.V)
                tmp_norm = tmp_delta0.norm()
                
                Vi = scale_i * vi

                delta_vel = None

                # update v0
                if bod.mass != 0:
                    delta_vel = (bi.mass / bod.mass) * (bi.V - Vi)
                else:
                    delta_vel = v0
                 
                net_vel += delta_vel
                bi.V = Vi
            i += 1
        

        # final adjustments if object has zero mass.

        if bod.mass == 0:
            v = metrics.metric_norm(net_vel, self._nmetric)
            if v != 0:
                net_vel = (self.get_max_speed()/v) * net_vel

        bod.V = net_vel
        """

        #after = self.get_momentum()
        #delta = after-before
        #name0 = bod.get_name()

        #print(name0 + ".", "change in momentum:", delta.norm())
        #print()
        #return








    def check_collision(self, bod:body.Body, del_x:vector.Vector):
        """
        Check whether any objects collide.
        """
        
        collided = False
        min_length = -1
        results = []
        
        msg = ""
        
        for other_body in self.bodies:
            collision = False
            
            if isinstance(other_body, body.Body):
                if other_body.id != bod.id:
                    if other_body.can_collide and bod.can_collide:
                
                        # see if the two bodies will collide.
                        # if so, change the positions & velocities.
                
                        # collision can only occur if the object is travelling towards 'other_body'
                        # diff means difference.
                        # can't tell whether moving towards or away, so treat all cases equally
                
                        # consider del_x, moving to if ||del_x|| <= d(x1,x2)
                
                        # multiple collisions may occur, find the one such that the other_body has the
                        # shortest distance from the bod, this means it will collide first.
                        
                        
                        # distance between other_body and bod
                        d_original = metrics.general_n_euclid_metric(bod.X, other_body.X, self._nmetric)
                        
                        
                        if not collided or d_original <= min_length:
                            
                            d_new = metrics.metric_norm(del_x, self._nmetric)
                        
                            tmp_del_x = del_x
                            if d_original < d_new:
                                tmp_del_x = tmp_del_x * (d_original/d_new)

                            # now check if collision occurs,
                            new_x = bod.X + tmp_del_x
                            collision = Collide.n_sphere_collide(new_x, bod.radius, other_body.X,
                                                                   other_body.radius, self._nmetric)

                        if collision:
                            
                            if d_original < min_length or not collided:
                                msg = ""
                                min_length = d_original
                                results = [other_body]
                            else:
                                msg += ", and "
                                # this means the object has collided with multiple bodies, same distance away
                                results.append(other_body)

                            msg += bod.name + " collided with " +  other_body.name
                            if not collided:
                                collided = True

        #print(msg)
        return collided, results




    def check_wall_collision(self, bod:body.Body, del_x:vector.Vector):
        """
        Given the new point a ball will be, find if it collides with the boundary wall/box.
        Return whether collision occured, the normal vector to the wall, and the new_delta_x value.
        
        new_delta_x is the delta_x such that when updated, the body lies touching the wall.
        """
        collision = False
        vec = None
        new_del_x = None

        if self.wall == None:
            pass
        elif bod.can_collide or self.all_wall_collide:
            
            n = len(self.wall)
            vec_components = [0] * n
            r = bod.radius
            
            new_x = bod.X + del_x
            component_length = 1
            new_component_length = 1

            i = 0
            while i < n:
                xi = new_x.components[i]
                abs_wall = abs(self.wall.components[i])
                
                xi_distance = abs_wall - r - abs(xi)
                
                if xi_distance >= 0:
                    pass # no collision
                else:
                    component_length = abs(del_x.components[i])
                    new_component_length = component_length + xi_distance

                    # collision occured, update normal vector.
                    collision = True
                    if xi >= 0:
                        vec_components[i] = -1
                    else:
                        vec_components[i] = 1
                i += 1
                    
            tmp_vec = vector.Vector(vec_components)
            vec = metrics.unit_vector(tmp_vec, self._nmetric)
            
            if collision:
                if component_length == 0:
                    new_del_x = vector.Vector.zero_vector(n)
                else:
                    new_del_x = (new_component_length / component_length) * del_x

        return collision, vec, new_del_x



    def wall_momentum_collision(self, bod:body.Body, wall_normal:vector.Vector):
        """
        Compute new momentum using the equations for body-body momentum collision.
        However, let mass of wall -> infinity and initial velocity be zero.
        
        This gives, if A == bod, and B == Wall
        
        vA = ub + r*(uB-uA) =   -r*uA
        vB = ub = 0
        """
        # let wall_normal be a unit vector

        # vector decomposition.
        projA = vector.Vector.inner_product(bod.V, wall_normal)
            
        vA_normal = projA * wall_normal
        vA_plane = bod.V - vA_normal

        # main calculation:
        uA = sign(projA) * metrics.metric_norm(vA_normal, self._nmetric)

            
        r = self.get_wall_restitution_coefficient(bod)
        vA = -r*uA
        
        new_vA_normal = vA * wall_normal
        VA = new_vA_normal + vA_plane

        bod.V = VA
        return

    def get_wall_restitution_coefficient(self, bod:body.Body):
        """
        Get coefficient of restitution given elasticity.
        """
        return math.sqrt(self.elasticity * bod.elasticity)





#####  Extra

def sign(x):
    if x < 0:
        return -1
    else:
        return 1



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

