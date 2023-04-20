import glfw
import math
import numpy as np
from OpenGL.GL import *

class Sun():
  data = np.zeros(360 + 8*3, [("position", np.float32, 2)])
  parts = []
  sunAngle = 200
  windowHeight = None

  def __init__(self, windowHeight):

    self.windowHeight = windowHeight

    # Sun
    for i in range(360):
        x = math.sin(math.radians(i)) * 0.05
        y = math.cos(math.radians(i)) * 0.05
        self.data[i] = [x, y]

    self.parts.append(
      (GL_TRIANGLE_FAN, 0, 360, (255, 255, 0))
    )
    
    # Rays
    # for i in range(8):
    #     rayAngle = i * (360 / 8)

    #     x = math.sin(math.radians(rayAngle)) * 0.2
    #     y = math.cos(math.radians(rayAngle)) * 0.2
    #     self.data[(i*3) + 360] = [x, y]

    #     x = math.sin(math.radians(rayAngle + 10)) * 0.3
    #     y = math.cos(math.radians(rayAngle + 10)) * 0.3
    #     self.data[(i*3)+1 + 360] = [x, y]

    #     x = math.sin(math.radians(rayAngle - 10)) * 0.3
    #     y = math.cos(math.radians(rayAngle - 10)) * 0.3
    #     self.data[(i*3)+2 + 360] = [x, y]

    self.parts.append(
      (GL_TRIANGLES, 360, 24, (255, 255, 0))
    )
      
    

  def getTransformMatrix(self):
    translateMatrix = np.array([
      [1,0,0, -math.sin(math.radians(self.sunAngle))*1],
      [0,1,0, -math.cos(math.radians(self.sunAngle))-0.6],
      [0,0,1,0],
      [0,0,0,1]
    ], dtype=np.float32)

    return translateMatrix
  
  def handleKeyEvent(self, window, key, scancode, action, mods):
    # Keep the sun rotating as long as the left or right arrow key is pressed
    if key == glfw.KEY_LEFT and action != glfw.RELEASE:
        self.sunAngle -= 2
    elif key == glfw.KEY_RIGHT and action != glfw.RELEASE:
        self.sunAngle += 2

    # Keep the angle between 0 and 360
    if self.sunAngle % 360 == 0:
        self.sunAngle = 0 
    
    # Change the background color based on the angle
    # Ideally, this would be in the main loop, but I'm not sure how to do that
    if abs(self.sunAngle) >= 280 or abs(self.sunAngle) <= 80:
        glClearColor(0.3 ,0.3 ,0.5 ,1) # Night sky
    else:
        glClearColor(0.5 ,0.5 ,1 ,1) # Blue sky
