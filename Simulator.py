from Quadtree import QTree

class Simulator:
    # abstract methods
    def __init__(self):
        raise NotImplementedError
    def step(self):
        raise NotImplementedError

class BarnesHut(Simulator):
    def __init__(self, bounds):
        self.bounds = bounds
        self.qtree = QTree(self.bounds)
        self.bodies = []
    def insert(self, body):
        self.bodies.append(body)
        self.qtree.insert(body)
    def step(self):
        self.qtree = qtree(self.bounds)
        for b in bodies:
            self.qtree.insert(body)
