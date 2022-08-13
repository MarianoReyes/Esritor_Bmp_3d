import sys
import random
from render import Render


def simple_cube():
    """
    Draws a cube
    """
    r = Render(800, 600)
    r.generar_3d('./models/cube.obj', (4, 3), (100, 100))
    # r.display()
    r.display('out.bmp')


def car():
    """
    Draws a car
    """
    r = Render(2000, 2000)
    r.generar_3d('./models/car.obj', (600, 600, 1800), (1000, 1000, 1000))
    # r.display()
    r.display('out.bmp')


if __name__ == "__main__":
    example = sys.argv[1] if len(sys.argv) > 1 else ""
    if example == "simple_cube":
        simple_cube()
    elif example == "car":
        car()
    else:
        print("Usage: python3 examples.py <example>")
        print("\nExample can be one of:\n")
        print("simple_cube: ", simple_cube.__doc__)
        print("car: ", car.__doc__)
