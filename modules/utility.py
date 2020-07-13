import random

def knuth_shuffle(array:list):
    """
    Shuffle an array in place
    """
    n = len(array)

    i = 0
    while i < n-1:
        j = random.randint(i, n-1)
        
        tmp = array[i]
        array[i] = array[j]
        array[j] = tmp

        i += 1

    return array


def get_range(start,stop):
    n = stop-start + 1
    i = 0
    array = [0]*n
    while i < n:
        array[i] = start + i
        i += 1
    return array


def shuffle_index(n):
    array = get_range(0,n-1)
    return knuth_shuffle(array)
