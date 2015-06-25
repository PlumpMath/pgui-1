from .putil import *
from bgl import *

def drawLine(x1, y1, x2, y2, color=(1, 1, 1, 1), width=1):
    glLineWidth(width)
    h_draw_line(x1, y1, x2, y2, color)
    glLineWidth(1)

def drawCircle(x, y, radius, color=(1, 1, 1, 1), fillcolor=(1, 1, 1, 1), swidth=1, fill=False):
    if fill:
        h_draw_circle(x, y, radius, fillcolor, segs=32)    
    glColor4f(*color)
    glLineWidth(swidth)
    h_draw_circle_wire(x, y, radius, segs=32)
    glLineWidth(1)

def drawRect(bounds, color=(1, 1, 1, 1), fillcolor=(1, 1, 1, 1), swidth=1, fill=False):
    if fill:
        glColor4f(*fillcolor)
        h_draw_rect(bounds)
    glColor4f(*color)
    glLineWidth(swidth)
    h_draw_quad_wire(bounds)
    glLineWidth(1)

def drawDot(x, y, color=(1, 1, 1, 1), swidth=1):
    glColor4f(*color)
    glPointSize(swidth)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()
    glPointSize(1)