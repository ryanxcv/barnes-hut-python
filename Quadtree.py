from numpy import array
from Util import Bounds, distance

# softening
a = 0.1

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
    def insert(self, body):
        raise NotImplementedError
    def traverse(self, f):
        f(self)

class Empty(Node):
    def insert(self, body):
        return Leaf(self.bounds, body)
    def massmult(self, body, theta):
        return 0

class Leaf(Node):
    def __init__(self, bounds, body):
        super().__init__(bounds)
        self.body = body
        # stored properties
        self.m = body.m
        self.q = body.q
    def insert(self, body):
        # subdivide the region
        branch = Branch(self.bounds, self.subdivide())
        # add bodies
        branch = branch.insert(self.body)
        branch = branch.insert(     body)
        return branch
    def subdivide(self):
        return [Empty(b) for b in self.bounds.subdivide()]
    def massmult(self, body, theta):
        if self.body is body:
            return 0
        i = body
        j = self.body
        d = distance(i.q, j.q)
        # return j.m * (j.q - i.q) / d ** 3
        return j.m * (j.q - i.q) / (d * (d + a) ** 2)

class Branch(Node):
    def __init__(self, bounds, children):
        super().__init__(bounds)
        self.children = children
    def calcProps(self):
        # calculate mass and position of center of mass
        self.m = sum(c.m       for c in self.children if type(c) is not Empty)
        self.q = sum(c.m * c.q for c in self.children if type(c) is not Empty) / self.m
    def insert(self, body):
        assert self.contains(body)
        new_children = []
        for c in self.children:
            if c.contains(body):
                new_children.append(c.insert(body))
            else:
                new_children.append(c)
        result = Branch(self.bounds, new_children)
        result.calcProps()
        return result
    def traverse(self, f):
        f(self)
        for c in self.children:
            c.traverse(f)
    def massmult(self, body, theta):
        if not self.contains(body) and self.bounds.s / distance(self.q, body.q) < theta:
            d = distance(self.q, body.q)
            # return self.m * (self.q - body.q) / d ** 3
            return self.m * (self.q - body.q) / (d * (d + a) ** 2)
        else:
            return sum(c.massmult(body, theta) for c in self.children)

class QTree(Node):
    def __init__(self, bounds):
        self.bounds = bounds
        self.root = Empty(bounds)
    def insert(self, body):
        assert self.contains(body)
        self.root = self.root.insert(body)
    def traverse(self, f):
        self.root.traverse(f)
    def massmult(self, body, theta=0.5):
        return self.root.massmult(body, theta)

bounds = Bounds(array((0, 0)), 1)
q = QTree(bounds)
e = Empty(bounds)
