import tkinter as tk
from tkinter import messagebox

from shapes import *
from tool import Tool
import save
import load

from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse

window = pyglet.window.Window(1280, 720)

shapes = load.shapes()
save.shapes(shapes)

config = load.config()
if config == None:
    config = {"tmp_dot_size": 4, "tmp_dot_color": Color(255, 0, 0), "tool": Tool("line", True)}
save.config(config)

def begin_shape(x, y):
    global config
    global shapes
    config["tool"].data["x"] = x
    config["tool"].data["y"] = y
    config["tool"].data["first"] = True
    shapes.append(Circle(x, y, config["tmp_dot_size"], True, config["tmp_dot_color"], True))

def finish_shape():
    global shapes
    global config
    for shape in shapes:
        if type(shape) == Circle:
            if shape.tmp == True:
                shape.draw_ = False

@window.event
def on_draw():
    global shapes
    global config
    window.clear()
    for shape in shapes:
        shape.draw()
    tool = config["tool"]
    toolt = tool.name
    if toolt == "line":
        ln = Line(10, window.height - 10, 110, window.height - 110, Color(0, 255, 255))
        ln.draw()
    elif toolt == "rect":
        re = Rect(10, window.height - 10, 110, window.height - 110, tool.fill, Color(0, 255, 255))
        re.draw()
    elif toolt == "circle":
        ci = Circle(65, window.height - 65, 50, tool.fill, Color(0, 255, 255))
        ci.draw()
    elif toolt == "polygon":
        l1 = Line(10, window.height - 10, 110, window.height - 10, Color(0, 255, 255))
        l2 = Line(110, window.height - 10, 10, window.height - 110, Color(0, 255, 255))
        l3 = Line(10, window.height - 110, 110, window.height - 65, Color(0, 255, 255))
        l4 = Line(110, window.height - 65, 10, window.height - 10, Color(0, 255, 255))
        l1.draw()
        l2.draw()
        l3.draw()
        l4.draw()

@window.event
def on_key_press(symbol, modifiers):
    global shapes
    if symbol == key.L:
        config["tool"] = Tool("line", config["tool"].fill)
    elif symbol == key.R:
        config["tool"] = Tool("rect", config["tool"].fill)
    elif symbol == key.C:
        config["tool"] = Tool("circle", config["tool"].fill)
    elif symbol == key.P:
        config["tool"] = Tool("polygon", config["tool"].fill)
    elif symbol == key.F:
        config["tool"].fill = not config["tool"].fill
    elif symbol == key.E:
        root = tk.Tk()
        root.withdraw()
        if messagebox.askyesno("Erasing shapes", "Do you want to erase all shapes?"):
            shapes = []
            save.shapes(shapes)
        root.destroy()

@window.event
def on_close():
    global config
    global shapes
    save.config(config)
    save.shapes(shapes)

@window.event
def on_mouse_press(x, y, button, modifiers):
    global tool
    global shapes
    if button == mouse.LEFT:
        if config["tool"].name == "line":
            if config["tool"].data["first"] == False:
                begin_shape(x, y)
            elif config["tool"].data["first"] == True:
                shapes.append(Line(config["tool"].data["x"], config["tool"].data["y"], x, y))
                config["tool"].data["first"] = False
                finish_shape()
        elif config["tool"].name == "rect":
            if config["tool"].data["first"] == False:
                begin_shape(x, y)
            elif config["tool"].data["first"] == True:
                shapes.append(Rect(config["tool"].data["x"], config["tool"].data["y"], x, y, filled=config["tool"].fill))
                config["tool"].data["first"] = False
                finish_shape()
        elif config["tool"].name == "circle":
            if config["tool"].data["first"] == False:
                begin_shape(x, y)
            elif config["tool"].data["first"] == True:
                shapes.append(Circle(config["tool"].data["x"], config["tool"].data["y"], distance(config["tool"].data["x"], config["tool"].data["y"], x, y), filled=config["tool"].fill))
                config["tool"].data["first"] = False
                finish_shape()
        if config["tool"].name == "polygon":
            if config["tool"].data["first"] == False:
                config["tool"].data["bx"] = x
                config["tool"].data["by"] = y
                begin_shape(x, y)
            elif config["tool"].data["first"] == True:
                shapes.append(Line(config["tool"].data["x"], config["tool"].data["y"], x, y))
                begin_shape(x, y)
    elif button == mouse.RIGHT:
        if config["tool"].name == "polygon":
            if config["tool"].data["first"] == True:
                shapes.append(Line(config["tool"].data["x"], config["tool"].data["y"], config["tool"].data["bx"],
                                   config["tool"].data["by"]))
                config["tool"].data["first"] = False
                finish_shape()
    save.shapes(shapes)

pyglet.app.run()
