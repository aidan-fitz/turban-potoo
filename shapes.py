from display import *
from matrix import *
from math import *

def add_circle(points, cx, cy, cz, r, step):
    # Find the first point
    x0 = cx + r
    y0 = cy
    t = 0

    tau = 2 * pi
    while t < 1 + step:
        # Find the next point
        x1 = cx + r * cos(t * tau)
        y1 = cy + r * sin(t * tau)
        # Add the edge (x0, y0) => (x1, y1)
        add_edge(points, x0, y0, cz, x1, y1, cz)
        # Advance the point-er
        t += step
        x0 = x1
        y0 = y1

HERMITE = 0
BEZIER = 1

def add_curve(points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type):
    # Find the first point
    xi = x0
    yi = y0

    # Generate curve coefficients
    coeffx = generate_curve_coeffs(x0, x1, x2, x3, curve_type)
    coeffy = generate_curve_coeffs(y0, y1, y2, y3, curve_type)

    # Iterate
    t = 0
    while t < 1 + step:
        # Find the next point
        xf = eval_poly(coeffx, t)
        yf = eval_poly(coeffy, t)
        # Add the edge (xi, yi) => (xf, yf)
        add_edge(points, xi, yi, 0, xf, yf, 0)
        print 't: ', t, '\tx: ', xi, xf, '\ty: ', yi, yf
        # Advance the point-er
        t += step
        xi = xf
        yi = yf

# Routines for working with edge matrices

def add_edge(matrix, x0, y0, z0, x1, y1, z1):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)

def add_point(matrix, x, y, z=0):
    matrix.append([x, y, z, 1])



from draw import *
from math import ceil, sqrt
from linalg import *

class BoxVertices:
    def __init__(self, x, y, z, width, height, depth):
        self.i = 0
        # (x, y, z) is the top left front corner (point 6)
        self.x0 = x
        self.y0 = y - height
        self.z0 = z - depth
        self.x1 = x + width
        self.y1 = y
        self.z1 = z

    def __iter__(self):
        return self

    def next(self):
        if self.i > 7:
            raise StopIteration
        else:
            L = []
            L.append(self.x1 if self.i & 1 else self.x0)
            L.append(self.y1 if self.i & 2 else self.y0)
            L.append(self.z1 if self.i & 4 else self.z0)
            self.i += 1
            return tuple(L)

def add_box(points, x, y, z, width, height, depth):
    vertices = list(BoxVertices(x, y, z, width, height, depth))

    # indices of faces
    back = [2, 3, 1, 0]
    front = [i + 4 for i in back[::-1]]
    bottom = [0, 1, 5, 4]
    top = [(i + 6) % 8 for i in bottom]
    left = [0, 4, 6, 2]
    right = [i + 1 for i in left[::-1]]

    faces = [front, back, left, right, top, bottom]

    for face in faces:
        x0, y0, z0 = vertices[face[0]]
        x1, y1, z1 = vertices[face[1]]
        x2, y2, z2 = vertices[face[2]]
        x3, y3, z3 = vertices[face[3]]
        add_quad(points, x0, y0, z0, x1, y1, z1, x2, y2, z2, x3, y3, z3)

# 'step' == number of steps (# points per ring)

# Generates 'step' rows and 'step' columns of shapes
# * 1 top row of triangles
# * 'step - 2' middle rows of quadrilaterals
# * 1 bottom row of triangles
def add_sphere(points, cx, cy, cz, r, step):
    columns = generate_sphere(cx, cy, cz, r, step)

    for row, col in [(r, c) for r in range(step) for c in range(step)]:
        row1p = row + 1
        col1p = (col + 1) % step

        # Top row of triangles
        if row == 0:
            x0, y0, z0 = columns[col][row]
            x1, y1, z1 = columns[col][row1p]
            x2, y2, z2 = columns[col1p][row1p]
            add_triangle(points, x0, y0, z0, x1, y1, z1, x2, y2, z2)

        # Middle row
        elif row < step - 1:
            x0, y0, z0 = columns[col][row]
            x1, y1, z1 = columns[col][row1p]
            x2, y2, z2 = columns[col1p][row1p]
            x3, y3, z3 = columns[col1p][row]
            add_quad(points, x0, y0, z0, x1, y1, z1, x2, y2, z2, x3, y3, z3)

        # Bottom row
        else:
            x0, y0, z0 = columns[col][row]
            x1, y1, z1 = columns[col][row1p]
            x2, y2, z2 = columns[col1p][row]
            add_triangle(points, x0, y0, z0, x1, y1, z1, x2, y2, z2)

# Generates 'step + 1' rows and 'step' columns of points (an array of 'step' columns)
# Each column is a semicircle
# Each row is a circle
def generate_sphere(cx, cy, cz, r, step):
    points = []
    # cache tau
    tau = 2 * pi
    # then start with theta and phi
    d_phi = tau / step
    d_theta = pi / step
    phi = 0

    while phi < tau:
        # templates for x, y
        tx = r * cos(phi)
        ty = r * sin(phi)
        # Need to reset theta
        theta = 0

        col = []
        while theta <= pi:
            w = sin(theta)
            x = tx * w
            y = ty * w
            z = r * cos(theta)
            col.append((x + cx, y + cy, z + cz))
            theta += d_theta
        points.append(col)

        phi += d_phi
    return points


# Generates 'step' rows and 'step' columns of quadrilaterals
def add_torus(points, cx, cy, cz, r, R, step):
    rows = generate_torus(cx, cy, cz, r, R, step)

    for row, col in [(r, c) for r in range(step) for c in range(step)]:
        row1p = (row + 1) % step
        col1p = (col + 1) % step

        # Pray to None that this is counterclockwise
        x0, y0, z0 = rows[row][col]
        x1, y1, z1 = rows[row1p][col]
        x2, y2, z2 = rows[row1p][col1p]
        x3, y3, z3 = rows[row][col1p]
        add_quad(points, x0, y0, z0, x1, y1, z1, x2, y2, z2, x3, y3, z3)

# Generates 'step' rows and 'step' columns of points (an array of 'step' rows)
# Each column is a "small" circle
# Each row is a "big" circle in the yz plane
def generate_torus(cx, cy, cz, r, R, step):
    points = []
    # cache tau
    tau = 2 * pi
    # start with theta and phi
    dt = tau / step
    theta = 0

    while theta < tau:
        # cache cos and sin while the same theta is in use
        y = r * cos(theta)
        w = r * sin(theta) + R
        # Need to reset phi
        phi = 0

        row = []
        while phi < tau:
            #print theta, phi
            x = w * cos(phi)
            z = w * sin(phi)
            row.append((x + cx, y + cy, z + cz))
            phi += dt
        points.append(row)

        theta += dt
    return points

# Routines for polygon matrices

def add_triangle(matrix, x0, y0, z0, x1, y1, z1, x2, y2, z2):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)
    add_point(matrix, x2, y2, z2)

def add_quad(matrix, x0, y0, z0, x1, y1, z1, x2, y2, z2, x3, y3, z3):
    add_triangle(matrix, x0, y0, z0, x1, y1, z1, x2, y2, z2)
    add_triangle(matrix, x2, y2, z2, x3, y3, z3, x0, y0, z0)
