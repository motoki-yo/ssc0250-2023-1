import glfw
import math
import numpy as np
from OpenGL.GL import *

class Ship():
  data = np.zeros(180 + 6 + 3 + 3, [("position", np.float32, 2)])
  parts = []
  translateX = 0.0
  translateY = 0.0
  scaleInc = 1.0

  def __init__(self):

    # Semi-ellipse
    for i in range(180):
        x = math.sin(math.radians(i+90)) * 0.6 # increase the radius along the x-axis
        y = math.cos(math.radians(i+90)) * 0.3 # increase the radius along the y-axis
        self.data[i] = [x, y]

    self.parts.append(
      (GL_TRIANGLE_FAN, 0, 180, (150, 75, 0))
    )

    # Mast
    self.data[180] = [-0.05, 1] # Top left
    self.data[181] = [0.05, 1] # Top right
    self.data[182] = [-0.05, 0] # Bottom left

    self.data[183] = [-0.05, 0] # Bottom left
    self.data[184] = [0.05, 0] # Bottom right
    self.data[185] = [0.05, 1] # Top right

    self.parts.append(
    (GL_TRIANGLES, 180, 186, (150, 75, 0))
    )

    # Sail right
    self.data[186] = [0.085, 1] # Top of mast
    self.data[187] = [0.085, 0.1] # Base on mast
    self.data[188] = [0.6, 0.1] # On air

    self.parts.append(
    (GL_TRIANGLES, 186, 189, (255, 255, 255))
    )

    # Sail left
    self.data[189] = [-0.085, 0.7] # Top of mast
    self.data[190] = [-0.085, 0.1] # Base on mast
    self.data[191] = [-0.5, 0.1] # On air

    self.parts.append(
    (GL_TRIANGLES, 189, 192, (255, 255, 255))
    )

    # Scaling and translating each vertex
    for i in range(0, len(self.data)):
      for vertex in self.data[i]:
        vertex *= .3

      #self.data[i][0][1] -= 0.5
      
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
    if key == glfw.KEY_I and action != glfw.RELEASE:
      self.translateY += 0.01
    
    if key == glfw.KEY_K and action != glfw.RELEASE:
      self.translateY -= 0.01

    if key == glfw.KEY_J and action != glfw.RELEASE:
      self.translateX -= 0.01 # A key to move left

    if key == glfw.KEY_L and action != glfw.RELEASE:
      self.translateX += 0.01

