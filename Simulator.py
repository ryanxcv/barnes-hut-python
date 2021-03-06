from numpy import array, random
from Quadtree import QTree
from Util import Body, Bounds, randVec2d

G = 1
epsilon = 1e-10

class Simulator:
    # abstract methods
    def __init__(self):
        raise NotImplementedError
    def step(self):
        raise NotImplementedError

defaultbounds = Bounds(array((-1, -1)), 2)
class BarnesHut(Simulator):
    def __init__(self, initbounds=defaultbounds, initn=0):
        self.bounds = initbounds
        self.qtree = QTree(self.bounds)
        self.bodies = []
        for i in range(initn):
            radius = 1
            maxv = 1
            q = radius * random.rand() ** (1/2) * randVec2d()
            v = maxv * randVec2d()
            self.insert(Body(1.0, q, v))
    def rebuild(self):
        # calculate bounds
        min_x = min(body.q[0] for body in self.bodies)
        min_y = min(body.q[1] for body in self.bodies)
        max_x = max(body.q[0] for body in self.bodies)
        max_y = max(body.q[1] for body in self.bodies)
        s = max(max_x - min_x, max_y - min_y) + epsilon
        self.bounds = Bounds(array((min_x, min_y)), s)
        # reconstruct quadtree
        self.qtree = QTree(self.bounds)
        for body in self.bodies:
            self.qtree.insert(body)
    def insert(self, body):
        self.bodies.append(body)
        if not self.qtree.contains(body):
            self.rebuild()
        else:
            self.qtree.insert(body)
    def step(self, dt=1e-3):
        if len(self.bodies) == 0:
            return
        # calculate forces
        new_bodies = []
        for body in self.bodies:
            v_new = body.v + G * dt * self.qtree.massmult(body)
            q_new = body.q + v_new * dt
            new_bodies.append(Body(body.m, q_new, v_new))
        self.bodies = new_bodies
        self.rebuild()
