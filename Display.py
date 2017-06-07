#!/bin/python3
from OpenGL.GL   import *
from OpenGL.GLU  import *
from OpenGL.GLUT import *
# from PIL import Image
from matplotlib import pyplot
from numpy import array
import sys

from Util import Bounds, Body
from Quadtree import Leaf
from Simulator import BarnesHut

# screen width/height
res = 1000

# simulator properties
sim = BarnesHut(initn=100)

# toggles
render_quads = True
running = False

def keyhandler(*args):
    key = args[0]
    global running
    # single step
    if key == b's' and not running:
        sim.step()
        display()
    # toggle quad rendering
    elif key == b'q':
        global render_quads
        render_quads = not render_quads
        display()
    # play/pause toggle
    elif key == b'p':
        running = not running
        if running:
            display()

def mousehandler(button, state, x, y):
    if state == GLUT_DOWN and button == GLUT_LEFT_BUTTON:
        q = array([x / res, y / res])
        new_body = Body(1, q, array((0, 0)))
        sim.insert(new_body)
        display()

def initialize():
    # Set up GLUT window parameters and associated functions
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(res, res)
    glutCreateWindow("N-Body Simulator")
    glutDisplayFunc(display)
    glutKeyboardFunc(keyhandler)
    glutMouseFunc(mousehandler)

    # Set up orthogonal viewing parameters for 2D display
    glViewport(0, 0, res, res)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, 1, -1, -1, 1)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    if running:
        sim.step()

    def drawNode(n):
        if type(n) is Leaf:
            # draw the particle
            glBegin(GL_POINTS)
            glVertex2f(*n.body.q)
            glEnd()

    def drawQuad(n):
        # draw the boundary
        b = n.bounds
        glBegin(GL_LINE_LOOP)
        glVertex2f(*b.nw)
        glVertex2f(b.nw[0], b.nw[1] + b.s)
        glVertex2f(b.nw[0] + b.s, b.nw[1] + b.s)
        glVertex2f(b.nw[0] + b.s, b.nw[1])
        glEnd()

    sim.qtree.traverse(drawNode)
    if render_quads:
        sim.qtree.traverse(drawQuad)

    # Update the display
    glutSwapBuffers()
    if running:
        glutPostRedisplay()

def main():
    initialize()
    glutMainLoop()

if __name__ == '__main__':
    main()
