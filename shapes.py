from pyglet.gl import *
from pyglet.graphics import *
from math import *

class Color:
    def __init__(self, r, g, b):
        self.clrs = [r, g, b]
        self.r = r
        self.g = g
        self.b = b
    def makelist(self, count):
        out = []
        for x in range(count):
            for c in self.clrs:
                out.append(c)
        return out
    def export(self):
        return {"type": "color", "color": [self.r, self.g, self.b]}
    def load(d):
        return Color(d[0], d[1], d[2])

class Dot:
    def __init__(self, x, y, color=Color(255, 255, 255)):
        self.vertices = vertex_list(1, ("v2i", [x, y]), ("c3B", color.makelist(1)))
        self.c = color
        self.x = x
        self.y = y
    def draw(self):
        self.vertices.draw(GL_POINTS)
    def export(self):
        return {"type": "dot", "x": self.x, "y": self.y, "color": [self.c.r, self.c.g, self.c.b]}
    def load(d):
        return Dot(d["x"], d["y"], Color.load(d["color"]))

class Line:
    def __init__(self, x1, y1, x2, y2, color=Color(255, 255, 255)):
        self.vertices = vertex_list(2, ("v2i", [x1,y1, x2,y2]), ("c3B", color.makelist(2)))
        self.c = color
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    def draw(self):
        self.vertices.draw(GL_LINES)
    def export(self):
        return {"type": "line", "x1": self.x1, "y1": self.y1, "x2": self.x2, "y2": self.y2, "color": [self.c.r, self.c.g, self.c.b]}
    def load(d):
        return Line(d["x1"], d["y1"], d["x2"], d["y2"], Color.load(d["color"]))

class Rect:
    def __init__(self, x1, y1, x2, y2, filled=True, color=Color(255, 255, 255)):
        if filled:
            self.vertices = vertex_list(4, ("v2i", [x1,y1, x2,y1, x2,y2, x1,y2]), ("c3B", color.makelist(4)))
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.c = color
        self.filled = filled
    def draw(self):
        if self.filled:
            self.vertices.draw(GL_QUADS)
        else:
            x1 = self.x1
            y1 = self.y1
            x2 = self.x2
            y2 = self.y2
            c = self.c
            l1 = Line(x1, y1, x2, y1, c)
            l2 = Line(x2, y1, x2, y2, c)
            l3 = Line(x2, y2, x1, y2, c)
            l4 = Line(x1, y2, x1, y1, c)
            l1.draw()
            l2.draw()
            l3.draw()
            l4.draw()
    def export(self):
        return {"type": "rect", "filled": self.filled, "x1": self.x1, "y1": self.y1, "x2": self.x2, "y2": self.y2, "color": [self.c.r, self.c.g, self.c.b]}
    def load(d):
        return Rect(d["x1"], d["y1"], d["x2"], d["y2"], d["filled"], Color.load(d["color"]))

class Circle:
    def __init__(self, x, y, r, filled=True, color=Color(255, 255, 255), tmp=False):
        self.filled = filled
        p = 1000
        deg = 360 / p
        deg = (deg/180)*pi
        if filled:
            P = x, y
        else:
            P = []
        for i in range(p + 1):
            n = deg * i
            P += int(r * cos(n)) + x, int(r * sin(n)) + y
        self.vertices = vertex_list(p + 2 if filled else p + 1, ('v2i', P), ('c3B', color.makelist(p + 2 if filled else p + 1)))
        self.tmp = tmp
        self.draw_ = True
        self.c = color
        self.x = x
        self.y = y
        self.r = r
    def draw(self):
        if self.filled and self.draw_:
            self.vertices.draw(GL_TRIANGLE_FAN)
        elif not self.filled and self.draw_:
            self.vertices.draw(GL_LINE_LOOP)
    def export(self):
        return {"type": "circle", "x": self.x, "y": self.y, "r": self.r, "color": [self.c.r, self.c.g, self.c.b],
                "tmp": self.tmp, "draw_": self.draw_, "filled": self.filled}
    def load(d):
        c = Circle(d["x"], d["y"], d["r"], d["filled"], Color.load(d["color"]), d["tmp"])
        c.draw_ = d["draw_"]
        return c

def distance(x1, y1, x2, y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
