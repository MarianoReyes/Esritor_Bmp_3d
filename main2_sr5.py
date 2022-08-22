import Obj
from gl import *
from vector import V3
from render import Render
from Obj import Obj

# ----------- dibujar los vertices de la textura -----------------

r = Render(1024, 1024)
t = Texture('out.bmp')

r.framebuffer = t.pixels

cube = Obj('./models/car2.obj')
r.current_color = color(255, 255, 255)

for faceDict in cube.faces:
    face = faceDict['face']

    if len(face) == 3:

        ft1 = face[0][1] - 1
        ft2 = face[1][1] - 1
        ft3 = face[2][1] - 1

        vt1 = V3(
            cube.tvertices[ft1][0] * t.width,
            cube.tvertices[ft1][1] * t.width
        )
        vt2 = V3(
            cube.tvertices[ft2][0] * t.width,
            cube.tvertices[ft2][1] * t.width
        )
        vt3 = V3(
            cube.tvertices[ft3][0] * t.width,
            cube.tvertices[ft3][1] * t.width
        )

        r.line(vt1, vt2)
        r.line(vt2, vt3)
        r.line(vt3, vt1)

r.write("out_textura.bmp")

glCreateWindow(2000, 2000)

glClearColor(0, 0, 0)
glClear()

glColor(0, 0, 0)

glTexture('out.bmp')

glRenderObj('./models/car2.obj', (600, 600, 1800), (1000, 1000, 1000))

glFinish('textura_SR5.bmp')
