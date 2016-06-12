from display import *
from matrix import *
from math import *

from linalg import *

def draw_line(screen, x0, y0, z0, x1, y1, z1, color):
    plotxyz = lambda x, y, z: plot(screen, color, x, y, z)
    bresenham(x0, y0, z0, x1, y1, z1, plotxyz)

def generate_line(x0, y0, z0, x1, y1, z1, L = []):
    f = lambda x, y, z: L.append( (x, y, z) )
    bresenham(x0, y0, z0, x1, y1, z1, f)
    return L

def bresenham(x0, y0, z0, x1, y1, z1, do_something):
    dx = x1 - x0
    dy = y1 - y0

    if dx + dy < 0:
        bresenham(x1, y1, z1, x0, y0, z0, do_something)
        return

    def z(x, y):
        if (x0, y0) == (x1, y1):
            return max(z0, z1)
        else:
            return dot_product([z0, z1], barycentric([[x0, y0], [x1, y1]], [x, y]))

    do_xy = lambda x, y: do_something(x, y, z(x, y))

    if dx == 0:
        y = y0
        while y <= y1:
            do_xy(x0, y)
            y += 1
    elif dy == 0:
        x = x0
        while x <= x1:
            do_xy(x, y0)
            x += 1
    elif dy < 0:
        d = 0
        x = x0
        y = y0
        while x <= x1:
            do_xy(x, y)
            if d > 0:
                y -= 1
                d -= dx
            x += 1
            d -= dy
    elif dx < 0:
        d = 0
        x = x0
        y = y0
        while y <= y1:
            do_xy(x, y)
            if d > 0:
                x -= 1
                d -= dy
            y += 1
            d -= dx
    elif dx > dy:
        d = 0
        x = x0
        y = y0
        while x <= x1:
            do_xy(x, y)
            if d > 0:
                y += 1
                d -= dx
            x += 1
            d += dy
    else:
        d = 0
        x = x0
        y = y0
        while y <= y1:
            do_xy(x, y)
            if d > 0:
                x += 1
                d -= dy
            y += 1
            d += dx


def draw_lines( matrix, screen, color ):
    if len(matrix) == 0:
        return

    if len(matrix) % 2:
        raise ValueError("Need at least 2 points to draw a line")

    p = 0
    while p < len( matrix ) - 1:
        draw_line( screen, matrix[p][0], matrix[p][1], matrix[p][2],
                   matrix[p+1][0], matrix[p+1][1], matrix[p+1][2], color )
        p += 2

def draw_polygons(matrix, screen, color):
    if len(matrix) == 0:
        return

    if len(matrix) % 3:
        raise ValueError("Need 3 points to draw a triangle")

    for p in range(0, len(matrix), 3):
        draw_triangle(matrix, p, screen, color, fill=True)

def draw_triangle(matrix, index, screen, color, fill=False):
    # Shorthand for the three vertices
    p0 = matrix[index]
    p1 = matrix[index + 1]
    p2 = matrix[index + 2]

    normal = surface_normal(matrix, index)

    # default is [0, 0, 1]
    view = [0, 0, 1]

    edges = [p0, p1, p1, p2, p2, p0]

    frontness = dot_product(view, normal)

    # Front faces
    if frontness > 0:
        # Fill the triangle
        if fill:
            # sort vertices by y-coordinate so we can scanline bottom to top
            vertices = sorted([p0, p1, p2], key = lambda p: p[1])
            bottom = vertices[0]
            middle = vertices[1]
            top    = vertices[2]

            # Initial x-coordinates
            x0 = bottom[0]
            # If there are two bottom vertices, x1 is the other one
            if bottom[1] == middle[1]:
                x1 = middle[0]
            else:
                x1 = bottom[0]

            # calculate dx's
            dx = lambda p0, p1: float(p0[0] - p1[0]) / (p0[1] - p1[1]) if p0[1] != p1[1] else 0
            dx0       = dx(bottom, top)
            dx1_lower = dx(bottom, middle)
            dx1_upper = dx(middle, top)

            fill_color = [e/2 for e in color]

            # Temporary: Use z-coordinate of centroid for z-buffering
            z = centroid(matrix, index)[2]

            # draw horizontal line segments
            for y in range(int(bottom[1]), int(top[1])):
                draw_line(screen, x0, y, z, x1, y, z, fill_color)
                x0 += dx0
                x1 += dx1_lower if y < middle[1] else dx1_upper
        # Draw the borders last
        draw_lines(edges, screen, color)


def centroid(matrix, index):
    # Shorthand for the three vertices
    p0 = matrix[index]
    p1 = matrix[index + 1]
    p2 = matrix[index + 2]

    # Average of the 3 points
    return [(p0[i] + p1[i] + p2[i])/3 for i in range(len(p0))]

def surface_normal(matrix, index):
    # Shorthand for the three vertices
    p0 = matrix[index]
    p1 = matrix[index + 1]
    p2 = matrix[index + 2]

    # the 2 edge vectors
    a = [p1[i] - p0[i] for i in range(3)]
    b = [p2[i] - p0[i] for i in range(3)]

    # Area of triangle is half the cross product
    #return [c / 2 for c in cross_product(a, b)]
    # But to keep it simple, we'll return the cross product
    return cross_product(a, b)

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
        beta = dot_product(point_vector, line_vector) / dot_product(line_vector, line_vector)
        return [1 - beta, beta]
    # case 2: triangle
    # algorithm courtesy of Maplesoft: https://www.maplesoft.com/support/help/maple/view.aspx?path=MathApps%2FProjectionOfVectorOntoPlane
    elif len(vertices) == 3:
        n = surface_normal(vertices, 0)
        proj = point - project(point, n)
    elif len(vertices) < 2:
        raise ValueError("I can't find the barycentric coordinates with a point!")
    else:
        raise ValueError("I'm too lazy to find barycentric coordinates with a %d-simplex!" % (len(vertices) - 1))

'''
Converts an edge or polygon matrix to a list of tuples to be used as set elements or dict keys.
'''
def as_tuples(matrix):
    return [tuple(p[:3]) for p in matrix]

'''
Creates a sparse list (dict) of polygon matrix indices and their surface normals.
'''
def surface_normals(polygons):
    return {i: surface_normal(polygons, i) for i in range(0, len(polygons), 3)}

'''
Converts a polygon matrix to a dict of points (as tuples) and their vertex normals.
'''
def vertex_normals(polygons):
    # First, convert the points to tuples
    points_list = as_tuples(polygons)
    points = set(points_list)

    # Next, map the points to the indices of triangles in which they appear
    points_triangles = {p: [i - (i % 3) for i, s in enumerate(points_list) if s == p] for p in points}

    # Then, transform the dict by converting each value (list of indices) to the sum of the surface normals
    surface_normals = surface_normals(polygons)

    # Map triangle indices to their surface normals and sum them
    return {p: vector_sum( [surface_normals[i] for i in points_triangles[p]] ) for p in points]}
