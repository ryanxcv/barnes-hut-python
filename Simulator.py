from Quadtree import QTree
from Util import Body

G = 1

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
    def step(self, dt=1e-3):
        new_bodies = []
        for body in self.bodies:
            v_new = body.v + G * dt * self.qtree.massmult(body)
            q_new = body.q + v_new * dt
            new_bodies.append(Body(body.m, q_new, v_new))
        self.bodies = new_bodies
        self.qtree = QTree(self.bounds)
        for body in self.bodies:
            self.qtree.insert(body)
