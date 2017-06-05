class Vec2(tuple):
    def __add__(self, v):
        return Vec2((self[0] + v[0], self[1] + v[1]))

class Body:
    '''
    Contains the properties of a single particle
    '''
    def __init__(self, mass, q, v):
        self.mass = mass
        self.q = q
        self.v = v
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
        offsets = [Vec2((x, y)) for x in [0, s] for y in [0, s]]
        return [Bounds(self.nw + offset, s) for offset in offsets]
