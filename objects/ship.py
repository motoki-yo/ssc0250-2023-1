import glfw
import math
import numpy as np
from OpenGL.GL import *

class Ship():
  data = np.zeros(360 + 4, [("position", np.float32, 2)])
  parts = []
  translateX = 0.0
  translateY = 0.0
  scaleInc = 1.0

  def __init__(self):

    # Ship
    # Semi-ellipse
    for i in range(180):
        x = math.sin(math.radians(i+90)) * 0.6 # increase the radius along the x-axis
        y = math.cos(math.radians(i+90)) * 0.3 # increase the radius along the y-axis
        self.data[i] = [x, y]

    self.parts.append(
      (GL_TRIANGLE_FAN, 0, 180, (150, 75, 0))
    )

    # Mast
    # Thin rectangle
    rect_width = 0.1
    rect_height = 0.7
    rect_x = -rect_width / 2
    rect_y = rect_height # move the rectangle up, lower it to move it down

    self.data[180] = [rect_x, rect_y]
    self.data[181] = [rect_x + rect_width, rect_y]
    self.data[182] = [rect_x + rect_width, rect_y - rect_height]
    self.data[183] = [rect_x, rect_y - rect_height]

    self.parts.append(
    (GL_QUADS, 180, 184, (150, 75, 0))
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
    if key == glfw.KEY_I and action != glfw.RELEASE:
      self.translateY += 0.01
    
    if key == glfw.KEY_K and action != glfw.RELEASE:
      self.translateY -= 0.01

    if key == glfw.KEY_J and action != glfw.RELEASE:
      self.translateX -= 0.01 # A key to move left

    if key == glfw.KEY_L and action != glfw.RELEASE:
      self.translateX += 0.01

