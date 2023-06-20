import glfw
import math
import numpy as np
from OpenGL.GL import *

class Sun():
  data = np.zeros(360 + 8*3, [("position", np.float32, 2)])
  parts = []
  sunAngle = 338

  def __init__(self):

    # Sun
    for i in range(360):
        x = math.sin(math.radians(i)) * 0.15
        y = math.cos(math.radians(i)) * 0.15 + 0.8 - 0.1
        self.data[i] = [x, y]

    self.parts.append(
      (GL_TRIANGLE_FAN, 0, 360, (255, 255, 0))
    )
    
    # Rays
    for i in range(8):
        rayAngle = i * (360 / 8)

        x = math.sin(math.radians(rayAngle)) * 0.2
        y = math.cos(math.radians(rayAngle)) * 0.2 + 0.8 - 0.1
        self.data[(i*3) + 360] = [x, y]

        x = math.sin(math.radians(rayAngle + 10)) * 0.3
        y = math.cos(math.radians(rayAngle + 10)) * 0.3 + 0.8 - 0.1
        self.data[(i*3)+1 + 360] = [x, y]

        x = math.sin(math.radians(rayAngle - 10)) * 0.3
        y = math.cos(math.radians(rayAngle - 10)) * 0.3 + 0.8 - 0.1
        self.data[(i*3)+2 + 360] = [x, y]

    self.parts.append(
      (GL_TRIANGLES, 360, 24, (255, 255, 0))
    )

    #  Scaling and translating each vertex
    for i in range(0, len(self.data)):
      for vertex in self.data[i]:
        vertex *= .75
      
      self.data[i][0][1] += 0.3
      
  def getTransformMatrix(self):
    translateMx = np.array([
      [1,0,0,0],
      [0,1,0,-0.9],
      [0,0,1,0],
      [0,0,0,1]
    ], dtype=np.float32)

    rotateMx = np.array(
      [[math.cos(math.radians(self.sunAngle)), -math.sin(math.radians(self.sunAngle)), 0.0, 0.0],
      [math.sin(math.radians(self.sunAngle)), math.cos(math.radians(self.sunAngle)), 0.0, 0.0],
      [0.0, 0.0, 1.0, 0.0],
      [0.0, 0.0, 0.0, 1.]], dtype=np.float32)
    
    translate2Mx = np.array([
      [1,0,0,0],
      [0,1,0,0.9],
      [0,0,1,0],
      [0,0,0,1]
    ], dtype=np.float32)

    transformationMx = np.matmul(translateMx, rotateMx)
    transformationMx = np.matmul(transformationMx, translate2Mx)

    return transformationMx
  
  def handleKeyEvent(self, window, key, scancode, action, mods):
    # Keep the sun rotating as long as the left or right arrow key is pressed
    if key == glfw.KEY_LEFT and action != glfw.RELEASE:
        self.sunAngle += 2
    elif key == glfw.KEY_RIGHT and action != glfw.RELEASE:
        self.sunAngle -= 2

    # Keep the angle between 0 and 360
    if self.sunAngle > 360:
        self.sunAngle = 0 
    
    # Change the background color based on the angle
    # Ideally, this would be in the main loop in a sort of return value handler
    self.color_transition(self.sunAngle)

  # Linear interpolation between two values
  def lerp(self, a, b, t):
      return a + (b - a) * t

  # Uses linear interpolation to change the background color based on the angle
  def color_transition(self, angle):
      t = (math.cos(math.radians(angle)) + 1) / 2
      r = self.lerp(0.2, 0.5, t)
      g = self.lerp(0.2, 0.5, t)
      b = self.lerp(0.5, 1.0, t)
      glClearColor(r, g, b, 1)

