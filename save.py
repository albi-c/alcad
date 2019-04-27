import os
import json

from shapes import *

HOME = os.path.expanduser("~")

def mkdir(path):
    os.makedirs(path, exist_ok=True)

def config(config_):
    mkdir(os.path.join(HOME, ".alcad"))
    j = {}
    for key, val in config_.items():
        try:
            j[key] = val.export()
        except AttributeError:
            j[key] = val
    with open(os.path.join(HOME, ".alcad", "config.json"), "w+") as f:
        f.write(json.dumps(j))

def shapes(shapes_):
    mkdir(os.path.join(HOME, ".alcad"))
    j = []
    for s in shapes_:
        if type(s) != Circle or (type(s) == Circle and s.tmp == False):
            j.append(s.export())
    with open(os.path.join(HOME, ".alcad", "shapes.json"), "w+") as f:
        f.write(json.dumps(j))
