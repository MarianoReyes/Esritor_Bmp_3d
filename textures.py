import struct
from render import Render
from obj import Obj
from vector import *


def color(r, g, b):
    return bytes([b, g, r])


class Texture:
    def __init__(self, path):
        self.path = path
        self.read()

    def read(self):
        with open(self.path, "rb") as image:
            image.seek(10)
            header_size = struct.unpack("=l", image.read(4))[0]
            image.seek(18)
            self.width = struct.unpack("=l", image.read(4))[0]
            self.height = struct.unpack("=l", image.read(4))[0]

            image.seek(header_size)

            self.pixels = []
            for y in range(self.height):
                self.pixels.append([])
                for x in range(self.width):
                    b = ord(image.read(1))
                    g = ord(image.read(1))
                    r = ord(image.read(1))
                    self.pixels[y].append(
                        color(r, g, b)
                    )

    def getColor(self, tx, ty):
        x = round(tx * self.width)
        y = round(ty * self.height)

        return self.pixels[y][x]

    def get_color_with_intensity(self, tx, ty, intensity):
        x = round(tx * self.width)
        y = round(ty * self.height)

        b = round(self.pixels[y][x][0] * intensity)
        g = round(self.pixels[y][x][1] * intensity)
        r = round(self.pixels[y][x][2] * intensity)

        return color(r, g, b)


r = Render(2000, 2000)
t = Texture("carsr4.bmp")

r.framebuffer = t.pixels

model = Obj("./models/car.obj")

r.current_color = color(0, 255, 0)

for face in model.faces:
    if len(face) == 3:
        f1 = face[0][1] - 1
        f2 = face[1][1] - 1
        f3 = face[2][1] - 1

        vt1 = V3(
            model.tvertices[f1][0]*t.width,
            model.tvertices[f1][1]*t.height,
        )
        vt2 = V3(
            model.tvertices[f2][0]*t.width,
            model.tvertices[f2][1]*t.height,
        )
        vt3 = V3(
            model.tvertices[f3][0]*t.width,
            model.tvertices[f3][1]*t.height,
        )

        print(vt1, vt2, vt3)

        r.line(vt1, vt2)
        r.line(vt2, vt3)
        r.line(vt3, vt1)

r.write("t.bmp")
