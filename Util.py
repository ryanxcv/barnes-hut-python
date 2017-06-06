from math import sqrt
from numpy import array

def distance(p1, p2):
    diff = p1 - p2
    return sqrt(diff.dot(diff))

class Body:
    '''
    Contains the properties of a single particle
    '''
    def __init__(self, m, q, v):
        self.m = m # mass (scalar)
        self.q = q # position
        self.v = v # velocity
    def __repr__(self):
        return "Body: " + str(self.q)

class Bounds:
    '''
    Defines the coordinates of a square in space
    '''
    def __init__(self, nw, s):
        self.nw = nw # northwest corner coordinates
        self.s  = s  # side length
    def __repr__(self):
        return "Bounds: " + str(self.nw) + ", " + str(self.
s)
    def contains(self, body):
        assert type(body) is Body
        q = body.q
        return q[0] >= self.nw[0] and q[0] < self.nw[0] + self.s and \
               q[1] >= self.nw[1] and q[1] < self.nw[1] + self.s
    def subdivide(self):
        s = self.s / 2
        offsets = [array((x, y)) for x in [0, s] for y in [0, s]]
        return [Bounds(self.nw + offset, s) for offset in offsets]
