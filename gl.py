import render
import math
from material import *
from textures import *

r = None


def glInit():
    pass


def glCreateWindow(width, height):
    global r

    w = width % 4
    adjusted_width = width

    if w != 0:
        adjusted_width = width + width % 4

    r = render.Render(adjusted_width, height)


def glViewPort(x, y, width, height):
    global r

    r.viewport = {
        "x": x,
        "y": y,
        "width": width if width < r.width else r.width - x - 1,
        "height": height if height < r.height else r.height - y - 1
    }


def glClear():
    global r
    r.clear()


def glClearColor(red, green, blue):
    global r
    r.set_clear_color(red, green, blue)


def glVertex(x, y):
    global r

    r.point(* r.convert_coordinates(x, y))


def glLine(x0, y0, x1, y1):
    global r

    r.line(
        * r.convert_coordinates(x0, y0),
        * r.convert_coordinates(x1, y1)
    )


def glColor(red, green, blue):
    global r
    r.set_current_color(red, green, blue)


def glFinish(name):
    global r
    r.write(name)


def glFinishZ(name):
    global r
    r.write_z('zBuffer-SR4.bmp')


def glPoint(x, y):
    global r
    r.point(x, y)


def glRenderObj(name, scale_factor, translate_factor):
    global r
    r.generar_3d(name, scale_factor, translate_factor)


def glScale(c, cord, factor):
    return (((cord - c) * factor) + c)


def glTexture(texture):
    global r
    r.texture = Texture(texture)


def glMaterial(material):
    global r
    r.material = Material(material)
