import glfw
import math
import numpy as np
from OpenGL.GL import *

class Moon():
  data = np.zeros(360, [("position", np.float32, 2)])
  parts = []
  moonAngle = (338 + 180) % 360

  def __init__(self):

    # Moon
    for i in range(360):
        x = math.sin(math.radians(i)) * 0.2
        y = math.cos(math.radians(i)) * 0.2 + 0.8 - 0.1
        self.data[i] = [x, y]

    self.parts.append(
      (GL_TRIANGLE_FAN, 0, 360, (178.5, 178.5, 178.5))
    )

    #  Scaling and translating each vertex
    for i in range(0, len(self.data)):
      for vertex in self.data[i]:
        vertex *= .75
      
      self.data[i][0][1] += 0.3
      
  def getTransformMatrix(self):
    translateMx = np.array([
      [1,0,0,0],
      [0,1,0,-1],
      [0,0,1,0],
      [0,0,0,1]
    ], dtype=np.float32)

    rotateMx = np.array(
      [[math.cos(math.radians(self.moonAngle)), -math.sin(math.radians(self.moonAngle)), 0.0, 0.0],
      [math.sin(math.radians(self.moonAngle)), math.cos(math.radians(self.moonAngle)), 0.0, 0.0],
      [0.0, 0.0, 1.0, 0.0],
      [0.0, 0.0, 0.0, 1.]], dtype=np.float32)
    
    translate2Mx = np.array([
      [1,0,0,0],
      [0,1,0,1],
      [0,0,1,0],
      [0,0,0,1]
    ], dtype=np.float32)

    transformationMx = np.matmul(translateMx, rotateMx)
    transformationMx = np.matmul(transformationMx, translate2Mx)

    return transformationMx
  
  def handleKeyEvent(self, window, key, scancode, action, mods):
    # Keep the sun rotating as long as the left or right arrow key is pressed
    if key == glfw.KEY_LEFT and action != glfw.RELEASE:
        self.moonAngle += 2
    elif key == glfw.KEY_RIGHT and action != glfw.RELEASE:
        self.moonAngle -= 2

    # Keep the angle between 0 and 360
    if self.moonAngle > 360:
        self.moonAngle = 0 

