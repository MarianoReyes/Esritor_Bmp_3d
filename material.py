
def color(r, g, b):
    return bytes([b, g, r])


def color_unit(r, g, b):
    return color(clamping(r*255), clamping(g*255), clamping(b*255))


def clamping(num):
    return int(max(min(num, 255), 0))


class Material(object):
    def __init__(self, filename):

        with open(filename) as f:
            self.lines = f.read().splitlines()

        self.materials = {}
        self.current_material = None

        for line in self.lines:

            if line:

                if ' ' not in line:
                    continue

                prefix, value = line.split(' ', 1)

                if prefix == 'Kd':
                    self.materials[self.current_material] = {
                        'difuse': color_unit(*(float(x) for x in value.split(' ')))
                    }

                if prefix == 'newmtl':
                    self.current_material = value
