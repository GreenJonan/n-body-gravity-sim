"""
Metric functions given a vector space.

Note:
    The key two functions are the euclid metric function, which defines distance, 
    and the inverse square law function, which returns a vector given a metric function.
    
    I have also added generalised versions of the euclidean metric and the inverse square law.
    However, they are not currently used in the main program.
"""



import vector as v
import constants
Vec = v.Vector

    
#####   Metric and Distance functions.

def euclid_metric(vec1:Vec, vec2:Vec):
    """
    Standard Euclidean metric.
    <V,U> = ||V - U|| = || (v1-u1)^2 + (v2-u2)^2 + ... + (vn-un)^2||
    """
    V2 = vec1 - vec2
    return V2.norm()


def manhattan_metric(vec1:Vec, vec2:Vec):
    """
    <V,U> = |v1-u1| + |v2-u2| + ... + |vn-un|
    """
    val = 0
    n = len(vec1)
    i = 0
    while i < n:
        val += abs(vec1.components[i] - vec2.components[i])
        i += 1
    return val
    

def general_n_euclid_metric(vec1:Vec, vec2:Vec, N:int):
    """
    <V,U> = n_root( |v1-u1|^n + |v2-u2|^n + ... + |vn-un|^n )
            
    Notice that this is the generalised form of the euclid and manhattan metric functions.
    Interesting property: as N->infty it appears the metric approach some value.
    """
    val = 0
    n = len(vec1)
    i = 0
    while i < n:
        val += abs(vec1.components[i] - vec2.components[i]) ** N
        i += 1
    return val **(1.0/N)
    
    
    
def metric(vec1:Vec, vec2:Vec):
    """
    Find the distance metric between two vectors.
    """
    if v.Vector.vector_len_error(vec1, vec2):
        pass
    else:
        # default metric.
        return euclid_metric(vec1,vec2)

        #return general_n_euclid_metric(vec1,vec2,250)



def distance(v1:Vec, v2:Vec):
    return metric(v1,v2)




##### Physical laws

def inverse_square_law(v1:Vec, v2:Vec):
    """
    :input: Two vectors
    :return: Vector, r_unit / r^2, where r = v2-v1
    """
    return inverse_n_law(v1,v2)


def inverse_n_law(v1:Vec, v2:Vec, n:int=2):
    """
    Similar to the inverse square law, except the power in the denominator is n
    Inverse square law: Given two vectors, find r_unit * 1/r^2  ==>  r * 1/r^3
    ==> r* 1/r^(n+1)
        
    :return: Vector
    """
    D = distance(v1, v2)
    if D <= constants.dist_error:
        # Return Zero vector
        return v.Vector.zero_vector(len(v1))
    R = v2 - v1
    return (1/D**(n+1)) * R


def general_inverse_n_law(v1:Vec,v2:Vec, n:int=2, N:int=2):
    """
    Generalised form of inverse n-law. That is r_unit / ||r||^n,
    where ||r|| is the generalised N euclid metric.
    :input: Vector x 2, int=n, int=N
    """
    
    D = general_n_euclid_metric(v1, v2, N)
    if D <= constants.dist_error:
        # Return Zero vector
        return v.Vector.zero_vector(len(v1))
    R = v2 - v1
    return (1/D**(n+1)) * R




