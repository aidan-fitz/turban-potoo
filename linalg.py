
def add(a, b):
    return [a[i] + b[i] for i in range(len(a))]

def vector_sum(L):
    return reduce(add, L)

def neg(a):
    return [-x for x in a]

def subtract(a, b):
    return add(a, neg(b))

def dot_product(a, b):
    if len(a) == len(b):
        return sum([a[i] * b[i] for i in range(len(a))])
    else:
        raise ValueError("Dot product defined only for vectors of same dimension")

def cross_product(a, b):
    if len(a) == len(b) == 3:
        return [a[(i+1) % 3] * b[(i+2) % 3] - a[(i+2) % 3] * b[(i+1) % 3] for i in range(3)]
    else:
        # Technically, cross product is also defined for 7-D vectors, but we're not working in 7-D are we?
        raise ValueError("Cross product defined only for vectors of dimension 3")

def scalar_triple_product(a, b, c):
    return dot_product(a, cross_product(b, c))

def magnitude(a):
    return sqrt(dot_product(a, a))

def normalize(a):
    mag = magnitude(a)
    return [x/mag for x in a]

'''
Returns the projection of a onto b
'''
def project(a, b):
    f = dot_product(a, b) / dot_product(b, b)
    return [x * f for x in b]
