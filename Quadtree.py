class Vec2(tuple):
    def __add__(self, v):
        return Vec2((self[0] + v[0], self[1] + v[1]))

class Body:
    '''
    Contains the properties of a single particle
    '''
    def __init__(self, mass, position, velocity):
        self.mass     = mass
        self.position = position
        self.velocity = velocity
    def __repr__(self):
        return "Body: " + str(self.position)

class Bounds:
    '''
    Defines the coordinates of a square in space
    '''
    def __init__(self, nw, s):
        self.nw = nw # northwest corner coordinates
        self.s  = s  # side length
    def __repr__(self):
        return "Bounds: " + str(self.nw) + ", " + str(self.s)
    def contains(self, body):
        if type(body) is Body:
            b = body.position
        elif type(body) is tuple:
            b = Vec2(body)
        else:
            b = body
        return b[0] >= self.nw[0] and b[0] < self.nw[0] + self.s and \
               b[1] >= self.nw[1] and b[1] < self.nw[1] + self.s
    def subdivide(self):
        s = self.s / 2
        offsets = [Vec2((x, y)) for x in [0, s] for y in [0, s]]
        return [Bounds(self.nw + offset, s) for offset in offsets]

'''
Parent class for all quadtree structures

Each node may be either empty, contain a single particle,
or contain references to four child nodes.
'''
class Node:
    def __init__(self, bounds):
        self.bounds = bounds
    def contains(self, body):
        return self.bounds.contains(body)
    def traverse(self, f):
        f(self)

class Empty(Node):
    def insert(self, body):
        return Leaf(self.bounds, body)
    def traverse(self, f):
        f(self)

class Leaf(Node):
    def __init__(self, bounds, body):
        super().__init__(bounds)
        self.body = body
    def insert(self, body):
        branch = Branch(self.bounds, self.subdivide())
        for b in [body, self.body]:
            branch = branch.insert(b)
        return branch
    def subdivide(self):
        return [Empty(b) for b in self.bounds.subdivide()]

class Branch(Node):
    def __init__(self, bounds, children):
        super().__init__(bounds)
        assert children is not None
        self.children = children

    def insert(self, body):
        assert self.contains(body)
        new_children = []
        for c in self.children:
            if c.contains(body):
                new_children.append(c.insert(body))
            else:
                new_children.append(c)
        return Branch(self.bounds, new_children)

    def traverse(self, f):
        f(self)
        for c in self.children:
            c.traverse(f)

class QTree(Node):
    def __init__(self, bounds):
        self.root = Empty(bounds)
    def insert(self, body):
        self.root = self.root.insert(body)
    def traverse(self, f):
        self.root.traverse(f)
