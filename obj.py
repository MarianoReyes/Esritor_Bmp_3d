
class Obj(object):
    def __init__(self, filename):
        with open(filename) as f:
            self.lines = f.read().splitlines()

        self.vertices = []
        self.faces = []

        for line in self.lines:

            if line:

                if ' ' not in line:
                    continue

                prefix, value = line.split(' ', 1)

                if value[0] == ' ':
                    value = '' + value[1:]

                if prefix == 'v':
                    self.vertices.append(
                        list(
                            map(float, value.split(' '))
                        )
                    )

                if prefix == 'f':
                    self.faces.append([
                        list(map(int, face.split('/')))
                        for face in value.split(' ') if face != ''
                    ])
