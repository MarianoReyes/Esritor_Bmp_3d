import sys
import random
from render import Render


def planta():
    """
    Draws a player
    """
    r = Render(1000, 1000)
    r.generar_3d('./models/planta.obj', (15, 15), (500, 300))
    # r.display()
    r.display('out.bmp')


def simple_cube():
    """
    Draws a cube
    """
    r = Render(800, 600)
    r.load('./models/cube.obj', (4, 3), (100, 100))
    # r.display()
    r.display('out.bmp')


def skull():
    """
    Draws a skull
    """
    r = Render(2000, 2000)
    r.generar_3d('./models/skull.obj', (50, 50), (1000, 1000))
    # r.display()
    r.display('out.bmp')


if __name__ == "__main__":
    example = sys.argv[1] if len(sys.argv) > 1 else ""
    if example == "planta":
        planta()
    elif example == "simple_cube":
        simple_cube()
    elif example == "skull":
        skull()
    else:
        print("Usage: python3 examples.py <example>")
        print("\nExample can be one of:\n")
        print("planta: ", planta.__doc__)
        print("simple_cube: ", simple_cube.__doc__)
        print("skull: ", skull.__doc__)
