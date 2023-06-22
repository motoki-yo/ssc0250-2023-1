import glfw
import math
import numpy as np
from OpenGL.GL import *

class Star():
  data = np.zeros(3 * 2, [("position", np.float32, 2)])
  parts = []
  rotateX = 0.0

  def __init__(self):

    # Triangle pointing up
    self.data[0] = [0.5, 0.0] # Bottom right
    self.data[1] = [-0.5, 0.0] # Bottom left
    self.data[2] = [0.0, math.sqrt(3)/2] # Top

    self.parts.append(
        (GL_TRIANGLES, 0, 3, (255, 100, 100))
    )

    # Triangle pointing down
    self.data[3] = [0.5, 0.6] # Top right
    self.data[4] = [-0.5, 0.6] # Top left
    self.data[5] = [0.0, -math.sqrt(3)/2 + 0.6] # Bottom

    self.parts.append(
        (GL_TRIANGLES, 3, 6, (255, 100, 100))
    )

    # Scaling and translating each vertex
    for i in range(0, len(self.data)):
      for vertex in self.data[i]:
        vertex *= .2

      self.data[i][0][1] -= 0.5
      self.data[i][0][0] += 0.5
      
  #Transform Matrix
  def getTransformMatrix(self):
    translateMx = np.array([
      [1.0, 0.0, 0.0, -0.5],
      [0.0, 1.0, 0.0, 0.5 - math.sqrt(3)/6 * .2],
      [0.0, 0.0, 1.0, 0.0],
      [0.0, 0.0, 0.0, 1.0]
    ])

    #Rotate Matrix
    rotateMx = np.array(
      [[math.cos(math.radians(self.rotateX)), -math.sin(math.radians(self.rotateX)), 0.0, 0.0],
      [math.sin(math.radians(self.rotateX)), math.cos(math.radians(self.rotateX)), 0.0, 0.0],
      [0.0, 0.0, 1.0, 0.0],
      [0.0, 0.0, 0.0, 1.]], dtype=np.float32)
    
    translate2Mx = np.array([
      [1,0,0,0.5],
      [0,1,0,-0.5 + math.sqrt(3)/6 * .2],
      [0,0,1,0],
      [0,0,0,1]
    ], dtype=np.float32)

    transformationMx = np.matmul(translate2Mx, rotateMx)
    transformationMx = np.matmul(transformationMx, translateMx)

    return transformationMx
  
  #On key event do nothing
  def handleKeyEvent(self, window, key, scancode, action, mods):
        pass
  
  #on time event rotate the star 
  def handleTime(self, time):

    if time % 8 != 0:
      return
  
    self.rotateX += 10