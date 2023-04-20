import glfw
import math
import numpy as np
from bettaFish import BettaFish
from sun import Sun
from OpenGL.GL import *

vertexSrc = """
  attribute vec2 position;
  uniform mat4 matrix;

  void main(){
    gl_Position = matrix * vec4(position,0.0,1.0);
  }
  """

fragmentSrc = """
  uniform vec4 color;

  void main(){
    gl_FragColor = color;
  }
  """

# Creates a shader, sets it's source, compiles it and attaches it to a program
def setUpShader(program, shaderSrc, shaderType):

  # Request a shader slot from GPU
  shader = glCreateShader(shaderType)

  # Set shader source code
  glShaderSource(shader, shaderSrc)

  # Compile shader
  glCompileShader(shader)
  if not glGetShaderiv(shader, GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(shader).decode()
    raise RuntimeError(f'Error compiling shader: {error}')

  # Attach shader to program
  glAttachShader(program, shader)

  return shader


def buildProgram(program):
  glLinkProgram(program)
  if not glGetProgramiv(program, GL_LINK_STATUS):
    programLog = glGetProgramInfoLog(program)
    raise RuntimeError(f'Error linking program: {programLog}')


def initWindow(w, h, title):
  glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
  window = glfw.create_window(w, h, title, None, None)
  glfw.make_context_current(window)

  return window

def convertRGB(color):
  return color[0]/255.0 , color[1]/255.0 , color[2]/255.0

# Initializing GLFW
glfw.init()

# Creating the window
window = initWindow(800, 800, "Ocean")

# Create OpenGL program
program = glCreateProgram()

# Create, compile and attach shaders
vertexShader = setUpShader(program, vertexSrc, GL_VERTEX_SHADER)
fragmentShader = setUpShader(program, fragmentSrc, GL_FRAGMENT_SHADER)

# Build program
buildProgram(program)

# Make program the default program
glUseProgram(program)

# Request a buffer slot from GPU
buffer = glGenBuffers(1)

# Make this buffer the default one
glBindBuffer(GL_ARRAY_BUFFER, buffer)

# Populate vertex array

objects = [Sun(800)]

vertexes = []

for obj in objects:
  vertexes.extend(obj.data)

vertexes = np.array(vertexes, dtype=[("position", np.float32, 2)])

# Upload data
glBufferData(GL_ARRAY_BUFFER, vertexes.nbytes, vertexes, GL_DYNAMIC_DRAW)
glBindBuffer(GL_ARRAY_BUFFER, buffer)

# Bind the position attribute
stride = vertexes.strides[0]
offset = ctypes.c_void_p(0)

# Getting the position attribute location
positionLoc = glGetAttribLocation(program, "position")
glEnableVertexAttribArray(positionLoc)
glVertexAttribPointer(positionLoc, 2, GL_FLOAT, False, stride, offset)

# Getting the color uniform location
colorLoc = glGetUniformLocation(program, "color")

# Getting the matrix uniform location
matrixLoc = glGetUniformLocation(program, "matrix")

def handleKeyEvent(window, key, scancode, action, mods):
  for obj in objects:
    obj.handleKeyEvent(window, key, scancode, action, mods)

glfw.set_key_callback(window, handleKeyEvent)

glfw.show_window(window)

glClearColor(0.5 ,0.5 ,1 ,1)

while not glfw.window_should_close(window):

  glfw.poll_events()

  glClear(GL_COLOR_BUFFER_BIT)

  vertexOffset = 0

  for obj in objects:
    for part in obj.parts:
      glUniformMatrix4fv(matrixLoc, 1, GL_TRUE, obj.getTransformMatrix())

      partType, partStart, partLength, partColor = part
      r,g,b = convertRGB(partColor)

      glUniform4f(colorLoc, r, g, b, 1.0)

      glDrawArrays(partType, vertexOffset + partStart, partLength)

  vertexOffset += len(obj.data)


  glfw.swap_buffers(window)

glfw.terminate()
