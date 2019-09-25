import numpy as np
from OpenGL.GL import *
from OpenGL.arrays import vbo

POINT_SIZE = 5


class Scene:
    """ OpenGL 2D scene class """

    def __init__(self):
        self.k = 4 # Ordnung der Kurve
        self.m = 50 # Anzahl der Kurvenpunkte
        self.points = []
        self.lines = []
        self.kontroll = []

    def deletePoints(self):
        self.points = []
        self.change()

    def makePoint(self, x, y):
        self.points.append((x, y))
        self.change()

    def pop_lastPoint(self):
        if len(self.points) != 0:
            self.points.pop()
            self.change()

    def draw(self):
        my_vbo = vbo.VBO(np.array(self.points, 'f'))
        my_vbo.bind()
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(2, GL_FLOAT, 0, my_vbo)
        # glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glColor3fv([0, 0, 0])
        glPointSize(POINT_SIZE)
        glDrawArrays(GL_POINTS, 0, len(self.points))

        if len(self.points) > 1:
            glDrawArrays(GL_LINE_STRIP, 0, len(self.points))

        if self.lines:
            line = vbo.VBO(np.array(self.lines, 'f'))
            line.bind()
            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointer(2, GL_FLOAT, 0, line)
            glColor3fv([1, 0, 0])
            glDrawArrays(GL_LINE_STRIP, 0, len(line))
            line.unbind()

        glDisableClientState(GL_VERTEX_ARRAY)
        my_vbo.unbind()

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT)
        self.draw()
        glFlush()

    def deboor(self, j, i, degree, controlpoints, knotvector, t):
        if j == 0:
            if i == len(controlpoints):
                return controlpoints[i - 1]
            return controlpoints[i]

        a = (t - knotvector[i])
        b = (knotvector[i - j + degree] - knotvector[i])

        if b == 0:
            alpha = 0
        else:
            alpha = a / b

        left_term = self.deboor(j - 1, i - 1, degree, controlpoints, knotvector, t)
        right_term = self.deboor(j - 1, i, degree, controlpoints, knotvector, t)

        b1 =((1 - alpha) * left_term[0]) + (alpha * right_term[0])
        b2 =((1 - alpha) * left_term[1]) + (alpha * right_term[1])

        return [b1,b2]

    def calc_knotvector(self):
        countPoints = len(self.points)
        if countPoints < self.k:
            return None

        part1 = [0 for x in range(self.k)]
        part2 = [x for x in range(1, countPoints - (self.k - 2))]
        part3 = [countPoints - (self.k - 2) for x in range(self.k)]
        return part1 + part2 + part3

    def change(self):
        print("Ordnung der Kurve: {} Anzahl der Kurvenpunkte: {} Kontrollpunkte: {}".format(self.k,self.m,self.kontroll))
        self.kontroll = self.calc_knotvector()
        if not self.kontroll:
            self.lines.clear()
            return
        self.lines = []
        if self.m >0:
            for i in range(self.m + 1):
                t = max(self.kontroll) * (i / self.m)
                r = None
                for j in range(len(self.kontroll)):
                    if t == max(self.kontroll):
                        r = len(self.kontroll) - self.k - 1
                        break
                    if self.kontroll[j] <= t < self.kontroll[j + 1]:
                        r = j
                        break

                self.lines.append(self.deboor(self.k - 1, r, self.k, self.points, self.kontroll, t))


    def add_order(self):
        self.k += 1
        self.change()

    def remove_order(self):
        if self.k > 2:
            self.k -= 1
            self.change()

    def add_curvePoint(self):
        self.m += 10
        self.change()

    def remove_curvePoint(self):
        if self.m > 0:
            self.m -= 10
            self.change()


