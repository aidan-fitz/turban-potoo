from matrix import matrix_mult as mmult
from matrix import *

class Stack:
    def __init__(self):
        self.stack = []
        I = new_matrix()
        ident(I)
        self.stack.append(I)

    def push(self):
        clone = [row[:] for row in self.peek()[:]]
        self.stack.append(clone)

    def pop(self):
        if len(self.stack) > 1:
            self.stack.pop()

    def peek(self):
        return self.stack[-1]

    def mult(self, matrix):
        #mmult(matrix, self.peek())
        # We be multiplying them backward
        mmult(self.peek(), matrix)
        self.stack[-1] = matrix


    def transform_points(self, points):
        mmult(self.peek(), points)
