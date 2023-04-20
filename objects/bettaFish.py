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
    # Body
    self.data[0] = [-0.625, 0.25]
    self.data[1] = [0.0, 0.0]
    self.data[2] = [-0.625, -0.25]

    self.parts.append(
      (GL_TRIANGLES, 0, 3, (255, 127, 81))
      )

    # Fin 1
    self.data[3] = [-0.45, 0.3]
    self.data[4] = [-0.25, 0.20]
    self.data[5] = [-0.370, 0.0]

    self.parts.append(
      (GL_TRIANGLES, 3, 3, (206, 66, 87))
    )

    # Fin 2
    self.data[6] = [-0.45, -0.3]
    self.data[7] = [-0.25, -0.20]
    self.data[8] = [-0.370, 0.0]

    self.parts.append(
      (GL_TRIANGLES, 6, 3, (206, 66, 87))
    )

    # Tail 1
    self.data[9] = [-0.75, 0.375]
    self.data[10] = [-0.625, 0.0]
    self.data[11] = [-1.0, 0.25]

    self.parts.append(
      (GL_TRIANGLES, 9, 3, (206, 66, 87))
    )

    # Tail 2
    self.data[12] = [-1.05, 0.175]
    self.data[13] = [-0.625, 0.0]
    self.data[14] = [-1.05, -0.175]

    self.parts.append(
      (GL_TRIANGLES, 12, 3, (206, 66, 87))
    )

    # Tail 3
    self.data[15] = [-1.0, -0.25]
    self.data[16] = [-0.625, 0.0]
    self.data[17] = [-0.75, -0.375]

    self.parts.append(
      (GL_TRIANGLES, 15, 3, (206, 66, 87))
    )

    # Eye
    for i in range(18, 41):
      x = 0.07 * math.cos(i * (2 * math.pi / 23)) - 0.3
      y = 0.07 * math.sin(i * (2 * math.pi / 23)) + 0.01
      self.data[i] = [x, y]

    self.parts.append(
      (GL_TRIANGLE_FAN, 18, 23, (255, 255, 255))
    )

    # Pupil
    for i in range(41, 64):
      x = 0.04 * math.cos(i * (2 * math.pi / 23)) - 0.275
      y = 0.04 * math.sin(i * (2 * math.pi / 23))
      self.data[i] = [x, y]

    self.parts.append(
      (GL_TRIANGLE_FAN, 41, 23, (0, 0, 0))
    )

    # Scaling and translating each vertex
    for i in range(0, len(self.data)):
      for vertex in self.data[i]:
        vertex *= .3
      
      self.data[i][0][1] -= 0.5

  def getTransformMatrix(self):
    translateMx = np.array([
      [1.0, 0.0, 0.0, self.translateX],
      [0.0, 1.0, 0.0, self.translateY],
      [0.0, 0.0, 1.0, 0.0],
      [0.0, 0.0, 0.0, 1.0]
    ])

    scaleMx = np.array([
      [self.scaleInc, 0.0, 0.0, 0.0],
      [0.0, self.scaleInc, 0.0, 0.0],
      [0.0, 0.0, 1.0, 0.0],
      [0.0, 0.0, 0.0, 1.0]
    ])

    return np.matmul(translateMx, scaleMx)
  
  def handleKeyEvent(self, window, key, scancode, action, mods):

    if key == glfw.KEY_W and action != glfw.RELEASE:
      self.translateY += 0.01
    
    if key == glfw.KEY_S and action != glfw.RELEASE:
      self.translateY -= 0.01

    if key == glfw.KEY_A and action != glfw.RELEASE:
      self.translateX -= 0.01 # A key to move left

    if key == glfw.KEY_D and action != glfw.RELEASE:
      self.translateX += 0.01
    
    if key == glfw.KEY_Z and action != glfw.RELEASE:
      self.scaleInc += 0.01 # Z key to increase
    if key == glfw.KEY_X and action != glfw.RELEASE:
      self.scaleInc -= 0.01
