import os
import json

from shapes import *
from tool import *

HOME = os.path.expanduser("~")

def exists(path):
    return os.path.exists(path)

def makeobjects(shps):
    i = 0
    for x in shps:
        if x["type"] == "dot":
            shps[i] = Dot.load(x)
        elif x["type"] == "line":
            shps[i] = Line.load(x)
        elif x["type"] == "rect":
            shps[i] = Rect.load(x)
        elif x["type"] == "circle":
            shps[i] = Circle.load(x)
        elif x["type"] == "polygon":
            shps[i] = Polygon.load(x)
        i += 1
    return shps

def config():
    if exists(os.path.join(HOME, ".alcad", "config.json")):
        with open(os.path.join(HOME, ".alcad", "config.json")) as f:
            out = json.loads(f.read())
            for key, val in out.items():
                if type(val) == dict:
                    if val["type"] == "color":
                        out[key] = Color.load(val["color"])
                    elif val["type"] == "tool":
                        out[key] = Tool.load(val)
            return out
    else:
        return None

def shapes():
    if exists(os.path.join(HOME, ".alcad", "shapes.json")):
        with open(os.path.join(HOME, ".alcad", "shapes.json")) as f:
            out = json.loads(f.read())
            return makeobjects(out)
    else:
        return []
