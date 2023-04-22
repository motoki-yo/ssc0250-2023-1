import glfw
import math
import numpy as np
from OpenGL.GL import *


class BettaFish():
    data = np.zeros(64, [("position", np.float32, 2)])
    parts = []
    translateX = 0.0
    translateY = 0.0
    scaleInc = 1.0


def __init__(self):

    # Star Body
    self.data[0] = [-0.5, 0.5]
    self.data[1] = [0.0, -0.5]
    self.data[2] = [0.5, 0.5]
    self.parts.append(
        (GL_TRIANGLES, 0, 3, (255, 255, 0))
    )
    self.data[3] = [-0.5, -0.5]
    self.data[4] = [0.0, 0.5]
    self.data[5] = [0.5, -0.5]

    self.parts.append(
        (GL_TRIANGLES, 3, 6, (255, 255, 0))
    )

    for i in range(0, len(self.data)):
        for vertex in self.data[i]:
            vertex *= .3
        self.data[i][0][1] -= 0.5