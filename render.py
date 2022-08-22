from Obj import Obj
from vector import *
from writeutilities import *


def color(r, g, b):
    return bytes([b, g, r])


def color_unit(r, g, b):
    return color(clamping(r*255), clamping(g*255), clamping(b*255))


def clamping(num):
    return int(max(min(num, 255), 0))


# ===============================================================
# Constants
# ===============================================================

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)


# ===============================================================
# Renders a BMP file
# ===============================================================

class Render(object):

    def __repr__(self):
        return "render %s x %s " % (self.width, self.height)

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.current_color = WHITE
        self.clear_color = BLACK
        self.texture = None
        self.material = None
        self.clear()

    def clear(self):
        self.framebuffer = [
            [self.clear_color for x in range(self.width)]
            for y in range(self.height)
        ]

        self.zBuffer = [
            [-9999 for x in range(self.width)]
            for y in range(self.height)
        ]

        self.zClear = [
            [self.clear_color for x in range(self.width)]
            for y in range(self.height)
        ]

    def clamping(self, num):
        return int(max(min(num, 255), 0))

    def set_clear_color(self, r, g, b):
        adjusted_r = self.clamping(r * 255)
        adjusted_g = self.clamping(g * 255)
        adjusted_b = self.clamping(b * 255)
        self.clear_color = color(adjusted_r, adjusted_g, adjusted_b)

    def write(self, filename):
        f = open(filename, 'bw')

        # pixel header
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(word(0))
        f.write(word(0))
        f.write(dword(14 + 40))

        # info header
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

        # pixel data
        for x in range(self.height):
            for y in range(self.width):
                f.write(self.framebuffer[y][x])

        f.close()

    def write_z(self, filename):
        f = open(filename, 'bw')

        # pixel header
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(word(0))
        f.write(word(0))
        f.write(dword(14 + 40))

        # info header
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

        # pixel data
        for x in range(self.height):
            for y in range(self.width):
                f.write(self.zClear[y][x])

        f.close()

    def set_current_color(self, r, g, b):
        red = self.clamping(r * 255)
        green = self.clamping(g * 255)
        blue = self.clamping(b * 255)
        self.current_color = color(red, green, blue)

    def point(self, x, y):
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            self.framebuffer[x][y] = self.current_color

    def convert_coordinates(self, x, y):
        if x < -1 or x > 1 or y < -1 or y > 1:
            return

        adjusted_x = x + 1
        adjusted_y = y + 1

        converted_x = (adjusted_x * self.viewport["width"])/2
        converted_y = (adjusted_y * self.viewport["height"])/2

        final_x = int(converted_x + self.viewport["x"])
        final_y = int(converted_y + self.viewport["y"])

        return final_x, final_y

    def line(self, v1, v2):

        x0 = round(v1.x)
        x1 = round(v2.x)
        y0 = round(v1.y)
        y1 = round(v2.y)

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        # Si es empinado, poco movimiento en x y mucho en y.
        steep = dy > dx

        # Se invierte si es empinado
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        # Si la linea tiene direccion contraria, invertir
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0
        threshold = dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                self.point(y, x)
            else:
                self.point(x, y)

            offset += dy * 2

            if offset >= threshold:
                y += 1 if y0 < y1 else -1

                threshold += dx * 2

    def simple_line(self, x0, y0, x1, y1):

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        # Si es empinado, poco movimiento en x y mucho en y.
        steep = dy > dx

        # Se invierte si es empinado
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        # Si la linea tiene direccion contraria, invertir
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0
        threshold = dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                self.point(y, x)
            else:
                self.point(x, y)

        offset += dy * 2

        if offset >= threshold:
            y += 1 if y0 < y1 else -1

            threshold += dx * 2

    def transform_vertex(self, vertex, scale, translate):
        return V3(
            ((vertex[0] * scale[0]) + translate[0]),
            ((vertex[1] * scale[1]) + translate[1]),
            ((vertex[2] * scale[2]) + translate[2])
        )

    def bounding_box(self, A, B, C):
        coords = [(A.x, A.y), (B.x, B.y), (C.x, C.y)]

        xmin = 999999
        xmax = -999999
        ymin = 999999
        ymax = -999999

        for (x, y) in coords:
            if x < xmin:
                xmin = x
            if x > xmax:
                xmax = x
            if y < ymin:
                ymin = y
            if y > ymax:
                ymax = y

        return V3(xmin, ymin), V3(xmax, ymax)

    def cross(self, v1, v2):
        return (
            v1.y * v2.z - v1.z * v2.y,
            v1.z * v2.x - v1.x * v2.z,
            v1.x * v2.y - v1.y * v2.x
        )

    def barycetric(self, A, B, C, P):
        cx, cy, cz = self.cross(
            V3(B.x - A.x, C.x - A.x, A.x - P.x),
            V3(B.y - A.y, C.y - A.y, A.y - P.y)
        )

        u = cx / cz
        v = cy / cz
        w = 1 - (u + v)

        return (w, v, u)

    def triangle(self, vertices, tvertices=[0, 0, 0], material=None):
        A, B, C = vertices

        if self.texture and tvertices != [0, 0, 0]:
            tA, tB, tC = tvertices

        N = (C - A) * (B - A)
        L = V3(0, 0, -1)
        i = N.norm() @ L.norm()

        if i <= 0 or i > 1:
            return

        grey = round(255 * i)

        self.current_color = color(grey, grey, grey)

        Bmin, Bmax = self.bounding_box(A, B, C)
        for x in range(round(Bmin.x), round(Bmax.x) + 1):
            for y in range(round(Bmin.y), round(Bmax.y) + 1):
                w, v, u = self.barycetric(A, B, C, V3(x, y))

                if (w < 0 or v < 0 or u < 0):
                    continue

                z = A.z * w + B.z * v + C.z * u

                factor = z/self.width

                try:
                    if (self.zBuffer[x][y] <= z):
                        self.zBuffer[x][y] = z
                        self.zClear[x][y] = color_unit(factor, factor, factor)

                        if self.texture and tvertices != [0, 0, 0]:
                            tx = tA.x * w + tB.x * u + tC.x * v
                            ty = tA.y * w + tB.y * u + tC.y * v

                            self.current_color = self.texture.get_color_with_intensity(
                                tx, ty, i)

                        if self.material:
                            if self.material.materials.get(material):
                                self.current_color = color(
                                    *[clamping(c * i) for c in self.material.materials[material]['difuse']])
                            else:
                                self.current_color = color(255, 0, 0)

                        self.point(y, x)
                except:
                    continue

        pass

    def display(self, filename='out.bmp'):
        self.write(filename)

    def generar_3d(self, name, scale_factor, translate_factor):
        model = Obj(name)

        for face in model.faces:
            faced = face['face']
            if len(face) == 3:
                if self.texture and len(model.tvertices) != 0:

                    ft1 = faced[0][1] - 1
                    ft2 = faced[1][1] - 1
                    ft3 = faced[2][1] - 1

                    vt1 = V3(*model.tvertices[ft1])
                    vt2 = V3(*model.tvertices[ft2])
                    vt3 = V3(*model.tvertices[ft3])

                    self.triangle((v1, v2, v3), (vt1, vt2, vt3),
                                  material=face['material'])

                else:

                    v1 = self.transform_vertex(
                        model.vertices[face[0][0] - 1], scale_factor, translate_factor)
                    v2 = self.transform_vertex(
                        model.vertices[face[1][0] - 1], scale_factor, translate_factor)
                    v3 = self.transform_vertex(
                        model.vertices[face[2][0] - 1], scale_factor, translate_factor)

                    self.triangle(v1, v2, v3)
            if len(face) == 4:
                # si hay f 4
                if self.texture and len(model.tvertices) != 0:
                    ft1 = face[0][1] - 1
                    ft2 = face[1][1] - 1
                    ft3 = face[2][1] - 1
                    ft4 = face[3][1] - 1

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

                    self.triangle(A, B, C, material=face['material'])
                    self.triangle(A, C, D, material=face['material'])

                else:
                    f1 = faced[0][0] - 1
                    f2 = faced[1][0] - 1
                    f3 = faced[2][0] - 1
                    f4 = faced[3][0] - 1

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
