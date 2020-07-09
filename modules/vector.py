"""
This module contains the vector object, as well as the metric function used to calculate distance.

Vectors have length in n-dimensions, and behave as expected.
"""

import math
import random as rnd
#import rnd_sphere
from modules import rnd_sphere


class Vector:
    def __init__(self, comps):
        if isinstance(comps, int) or isinstance(comps, float):
            self.components = tuple([comps])
        else:
            self.components = tuple(comps)


    def inner_product(self, other):
        """
           Compute the inner product between two vectors. Assert that both have the same length.
           By default, compute standard inner product, that is the dot product. 
           X*Y = x1*y1 + x2*y2 + ... + xn*yn
           
           :return: float or integer.
        """
        if not isinstance(other, Vector):
            raise ValueError("Error: {} is not a vector object, cannot compute inner product.".format(other))
        elif Vector.vector_len_error(self, other):
            pass
        else:
            # computation.
            
            result = 0
            n = len(self)
            i = 0
            while i < n:
                result += self.components[i] * other.components[i]
                i += 1
            return result


    def norm(self):
        return math.sqrt(Vector.inner_product(self, self))


    ####  Operation Overloading  ####

    def __len__(self):
        return len(self.components)

    def __abs__(self):
        return self.norm()

    def __add__(self, other):
        """
            Overload addition operation. Add two vectors together component wise.
        """
        if not isinstance(other, Vector):
            raise ValueError("Error: Cannot add {0} type to {1} type.".format(type(other), type(self)))
        elif Vector.vector_len_error(self, other):
            pass
        else:
            n = len(self)
            tmp = [0] * n
            i = 0
            while i < n:
                tmp[i] = self.components[i] + other.components[i]
                i += 1
            return Vector(tmp)


    def __sub__(self, other):
        return self + (-other)

    def __neg__(self):
        return -1 * self

    def __mul__(self, other):
        """
           Overload multiplication operation. Implement field multiplication with vector.
           Input: self * other
           :return: Vector
        """
        if isinstance(other, float) or isinstance(other, int):
            # Multiply all components by field element.
            
            n = len(self)
            tmp = [0] * n
            if other == 0:
                pass
            else:
                i = 0
                while i < n:
                    tmp[i] = other * self.components[i]
                    i += 1
            return Vector(tmp)

        else:
            raise ValueError("Error: cannot multiply {0} type and {1} type.".format(type(self), type(other)))

    def __rmul__(self, other):
        # other * self
        return self * other


    def __truediv__(self, other):
        return self * (1/other)
    
    def __truerdiv__(self, other):
        return self / other


    def __eq__(self, other):
        if isinstance(other, type(None)):
            return False
        
        if not isinstance(other, Vector):
            raise ValueError("Equality not defined between {0} type and {1} type."\
                             .format(type(self), type(other)))
        elif Vector.vector_len_error(self, other):
            pass
        else:
            n = len(self)
            i = 0
            while i < n:
                if self.components[i] != other.components[i]:
                    return False
                i += 1
            return True



    def __repr__(self):
        tmp_str = str(self.components)
        tmp_str= tmp_str.lstrip('(').rstrip(')')
        return '{' + tmp_str + '}'
    



    #####
    #####   SPECIAL FUNCTIONS
    #####

    #####   Generating special vectors
    
    @staticmethod
    def zero_vector(dim:int):
        if dim < 1:
            raise ValueError("Error: Vector dimension undefined for dim={0}".format(dim))
        return Vector([0] * dim)



    @staticmethod
    def polar_vector(radius:float, angles:list):
        """
        Given a radius component and a set of angles, return the relevant co-ordinate vector.
        """
        dim = len(angles) + 1
        sin_t = 1
        vecs = [0]*dim
    
        i = 0
        while i < dim:
            t = abs(angles[i])  #warning may be non float/int
            if i + 1 == dims:
                t = t % 2*math.pi
            else:
                t = t % math.pi
            vecs[i] = r * sint_t * math.cos(t)
            sint_t = sint_t * math.sin(t)
            i += 1
        return Vector(vecs)
    


    #####   Random vectors

    def random_float_vector(dim:int):
        """
        Generate a vector with dimension :dim: and components from [0,1]
        """
        if dim <= 0:
            raise ValueError("Error: Vector dimension not implemented for: dim = {0}".format(dim))
        else:
            vec = [0] * dim
            i = 0
            while i < n:
                vec[i] = rnd.random()
                i += 1
            return Vector(vec)


    @staticmethod
    def random_vector(dim:int,max_val:int):
        """
        Generate a random vector with vector elements from [0,max_val)
        """
        return Vector.random_float_vector(dim) * (max_val)



    """
    TO IMPLEMENT: Random circle/spherical vectors (max_length, not max_component)
    likewise for elliptical points.
    """

    @staticmethod
    def random_ball_vector(dim:int, max_radius):
        return Vector( rnd_sphere.muller_n_ball(dim, max_radius) )

    @staticmethod
    def random_sphere_vector(dim:int, r=1):
        return Vector( rnd_sphere.muller_n_sphere(dim, r) )




    #####   Errors:
    @staticmethod
    def vector_len_error(v1,v2):
        # assume inputs are vectors
        if len(v1) != len(v2):
            raise ValueError("Error: Vectors of different dimension cannot be added together; dim {0} and dim {1}".format(len(v1), len(v2)))
            return True
        else:
            return False










if __name__ == "__main__":
    #v1 = Vector([0,1,2,3,4])
    #v2 = Vector([1,3,6,2,5])
    
    r = 3
    v1 = Vector((-0.486*r, -0.874*r)) #Vector.random_sphere_vector(2)
    v2 = Vector((0.163*r, 0.987*r)) #Vector.random_sphere_vector(2)
    #print(v1, "+", v2, "=", v1+v2)
    print("distance:", Vector.distance(v1,v2))

    import matplotlib.pyplot as plt
    plt.figure()
    plt.plot(v1.components[0],v1.components[1], 'ro')
    plt.plot(v2.components[0],v2.components[1], 'go')
    
    plt.plot([-1*r,-1*r,1*r,1*r],[1*r,-1*r,-1*r,1*r],'k')

    plt.show()

