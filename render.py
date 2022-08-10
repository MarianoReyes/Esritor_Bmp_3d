import struct
from obj import Obj
from vector import *
from writeutilities import *


def color(r, g, b):
    return bytes([b, g, r])


# ===============================================================
# Constants
# ===============================================================

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)


# ===============================================================
# Renders a BMP file
# ===============================================================

class Render(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.current_color = WHITE
        self.clear()

    def clear(self):
        self.pixels = [
            [BLACK for x in range(self.width)]
            for y in range(self.height)
        ]

    def write(self, filename):
        f = open(filename, 'bw')

        # File header (14 bytes)
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        # Image header (40 bytes)
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        # Pixel data (width x height x 3 pixels)
        for x in range(self.height):
            for y in range(self.width):
                f.write(self.pixels[x][y])

        f.close()

    def display(self, filename='out.bmp'):
        self.write(filename)

    def set_color(self, color):
        self.current_color = color

    def point(self, x, y, color=None):
        # 0,0 was intentionally left in the bottom left corner to mimic opengl
        try:
            self.pixels[y][x] = color or self.current_color
        except:
            # To avoid index out of range exceptions
            pass

    def line(self, x1, y1, x2, y2, color=None):
        """
        Draws a line in the screen.
        Input: 
        start: size 2 array with x,y coordinates
        end: size 2 array with x,y coordinates
        """
        x1 = x1
        y1 = y1
        x2 = x2
        y2 = y2

        dy = abs(y2 - y1)
        dx = abs(x2 - x1)
        steep = dy > dx

        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        dy = abs(y2 - y1)
        dx = abs(x2 - x1)

        offset = 0
        threshold = dx

        y = y1
        for x in range(x1, x2 + 1):
            if steep:
                self.point(y, x, color)
            else:
                self.point(x, y, color)

            offset += dy * 2
            if offset >= threshold:
                y += 1 if y1 < y2 else -1
                threshold += dx * 2

    def load(self, filename, translate, scale):
        model = Obj(filename)

        for face in model.faces:
            vcount = len(face)

            for j in range(vcount):
                f1 = face[j][0]
                f2 = face[(j + 1) % vcount][0]

                v1 = model.vertices[f1 - 1]
                v2 = model.vertices[f2 - 1]

                x1 = round((v1[0] + translate[0]) * scale[0])
                y1 = round((v1[1] + translate[1]) * scale[1])
                x2 = round((v2[0] + translate[0]) * scale[0])
                y2 = round((v2[1] + translate[1]) * scale[1])

                self.line(x1, y1, x2, y2)

    def transform_vertex(self, vertex, scale, translate):
        return [
            ((vertex[0] * scale[0]) + translate[0]),
            ((vertex[1] * scale[1]) + translate[1])
        ]

    def triangle(self, v1, v2, v3):
        self.line(round(v1[0]), round(v1[1]), round(v2[0]), round(v2[1]))
        self.line(round(v2[0]), round(v2[1]), round(v3[0]), round(v3[1]))
        self.line(round(v3[0]), round(v3[1]), round(v1[0]), round(v1[1]))

    def generar_3d(self, name, scale_factor, translate_factor):
        model = Obj(name)

        for face in model.faces:
            if len(face) == 3:

                v1 = self.transform_vertex(
                    model.vertices[face[0][0] - 1], scale_factor, translate_factor)
                v2 = self.transform_vertex(
                    model.vertices[face[1][0] - 1], scale_factor, translate_factor)
                v3 = self.transform_vertex(
                    model.vertices[face[2][0] - 1], scale_factor, translate_factor)

                self.triangle(v1, v2, v3)
            if len(face) == 4:

                # assuming 4
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
                f4 = face[3][0] - 1

                vertices = [
                    self.transform_vertex(
                        model.vertices[f1], scale_factor, translate_factor),
                    self.transform_vertex(
                        model.vertices[f2], scale_factor, translate_factor),
                    self.transform_vertex(
                        model.vertices[f3], scale_factor, translate_factor),
                    self.transform_vertex(
                        model.vertices[f4], scale_factor, translate_factor)
                ]

                A, B, C, D = vertices

                self.triangle(A, B, C)
                self.triangle(A, C, D)
