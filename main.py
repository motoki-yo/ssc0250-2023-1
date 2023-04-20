import glfw
import math
import numpy as np
from objects.bettaFish import BettaFish
from objects.moon import Moon
from objects.ocean import Ocean
from objects.sun import Sun
from objects.ship import Ship
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
  return color[0]/255.0 , color[1]/255.0 , color[2]/255.0, 1.0

# Initializing GLFW
glfw.init()

# Disable Window Resizing
glfw.window_hint(glfw.RESIZABLE, False)

# Creating the window
window = initWindow(800, 800, "Sea View")

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

objects = [Ocean(), BettaFish(), Sun(), Moon(), Ship()]

objectsInScene = []

for obj in objects:

    # Create Vertex Buffer Object for each object
    objectVbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER,objectVbo)
    glBufferData(GL_ARRAY_BUFFER,obj.data.nbytes,obj.data,GL_STATIC_DRAW)

    # Create Vertex Array Object for each object
    objectVao = glGenVertexArrays(1)
    glBindVertexArray(objectVao)
    glBindBuffer(GL_ARRAY_BUFFER,objectVbo)
    glVertexAttribPointer(0 ,2 ,GL_FLOAT ,GL_FALSE ,0 ,None)
    glEnableVertexAttribArray(0)

    objectsInScene.append({
      "vao": objectVao,
      "vbo": objectVbo,
      "obj": obj
    })

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

time = 0

while not glfw.window_should_close(window):

  if time > 100000:
    time = 0

  time += 1

  glfw.poll_events()

  glClear(GL_COLOR_BUFFER_BIT)

  for objSc in objectsInScene:

    obj = objSc["obj"]
    vao = objSc["vao"]

    for part in obj.parts:
      glUniformMatrix4fv(matrixLoc, 1, GL_TRUE, obj.getTransformMatrix())

      partType, partStart, partLength, partColor = part

      # If there is no color, use the background color
      r,g,b,a = glGetFloatv(GL_COLOR_CLEAR_VALUE) if partColor == None else convertRGB(partColor)

      glUniform4f(colorLoc, r, g, b, a)

      glBindVertexArray(vao)

      glDrawArrays(partType, partStart, partLength)
    
    handleTime = getattr(obj, "handleTime", None)

    if callable(handleTime):
      obj.handleTime(time)


  glfw.swap_buffers(window)

glfw.terminate()
