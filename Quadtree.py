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
        self.children = children

    def insert(self, body):
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
        self.bounds = bounds
        self.root = Empty(bounds)
    def insert(self, body):
        assert self.contains(body)
        self.root = self.root.insert(body)
    def traverse(self, f):
        self.root.traverse(f)
