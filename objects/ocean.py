import glfw
import math
import numpy as np
from OpenGL.GL import *

class Ocean():
  elpsX = 0.05
  elpsY = 0.05
  nElipses = int(2/(elpsX))

  data = np.zeros(6 + 23 * (nElipses + 1), [("position", np.float32, 2)])
  parts = []

  translateX = 0.0
  translateXSign = 1.0

  translateY = 0.0
  translateYSign = 1.0

  scaleY = 1.0
  scaleYSign = 1.0

  def __init__(self):
    # First triangle
    self.data[0] = [-2, 0]
    self.data[1] = [-2, -2]
    self.data[2] = [2, 0]

    self.parts.append(
      (GL_TRIANGLES, 0, 3, (7, 7, 125))
      )

    # Second triangle
    self.data[3] = [2, 0]
    self.data[4] = [2, -2]
    self.data[5] = [-2, -2]

    self.parts.append(
      (GL_TRIANGLES, 3, 3, (7, 7, 125))
      )

    for i in range(0, self.nElipses+1):
      for j in range(6 + (i * 23), 29 + (i * 23)):
        x = self.elpsX * math.cos(j * (2 * math.pi / 23)) - 2 + (i * self.elpsX * 2)
        y = self.elpsY * math.sin(j * (2 * math.pi / 23)) + 0.02
        self.data[j] = [x, y]     

      self.parts.append(
        (GL_TRIANGLE_FAN, 6 + (i * 23) , 23, None)
        )

  def getTransformMatrix(self):
    translateMx = np.array([
      [1,0,0,self.translateX],
      [0,1,0,self.translateY],
      [0,0,1,0],
      [0,0,0,1]
    ], dtype=np.float32)

    scaleMx = np.array([
      [1, 0.0, 0.0, 0.0],
      [0.0, self.scaleY, 0.0, 0.0],
      [0.0, 0.0, 1.0, 0.0],
      [0.0, 0.0, 0.0, 1.0]
    ])

    return np.matmul(translateMx, scaleMx)

  def handleKeyEvent(self, window, key, scancode, action, mods):
    pass
  
  def handleTime(self, time):

    if time % 8 != 0:
      return
  
    self.translateX += 0.02 * self.translateXSign

    self.translateY += 0.005 * self.translateYSign

    self.scaleY += 0.01 * self.scaleYSign
 
    if np.abs(self.translateX) > 1:
      self.translateXSign *= -1

    if self.scaleY > 1.8 or self.scaleY < 1:
      self.scaleYSign *= -1

    if np.abs(self.translateY) > self.elpsY/2:
      self.translateYSign *= -1
    
    
    
    
    
