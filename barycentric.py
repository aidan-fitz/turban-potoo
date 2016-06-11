from linalg import *
from draw3d import surface_normal

'''
@param vertices: A matrix of (n+1) points representing the vertices of the n-simplex
@param point: The coordinates of the point we want to transform

Algorithm:
1. Project the point onto the line, plane, etc. of the simplex
2. Find the inverse of the vertex matrix
3. Multiply the matrix inverse by the projected point to get the barycentric coordinates
'''
def barycentric(vertices, point):
    # case 1: line segment
    # Using part of projection algorithm courtesy of Wikibooks:
    # https://en.wikibooks.org/wiki/Linear_Algebra/Orthogonal_Projection_Onto_a_Line
    if len(vertices) == 2:
        line_vector = subtract(vertices[1], vertices[0])
        point_vector = subtract(point, vertices[0])
        beta = dot(point_vector, line_vector) / dot(line_vector, line_vector)
        return [beta, 1 - beta]
    # case 2: triangle
    # algorithm courtesy of Maplesoft: https://www.maplesoft.com/support/help/maple/view.aspx?path=MathApps%2FProjectionOfVectorOntoPlane
    elif len(vertices) == 3:
        n = surface_normal(vertices, 0)
        proj = point - project(point, n)
    elif len(vertices) < 2:
        raise ValueError("I can't find the barycentric coordinates with a point!")
    else:
        raise ValueError("I'm too lazy to find barycentric coordinates with a %d-simplex!" % (len(vertices) - 1))
