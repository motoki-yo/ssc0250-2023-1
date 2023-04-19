import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import math

vertex_src = """
# version 330

in vec2 a_position;

void main()
{
    gl_Position = vec4(a_position, 0.0, 1.0);
}
"""

fragment_src = """
# version 330

out vec4 out_color;

void main()
{
    out_color = vec4(1.0, 1.0, 0.0, 1.0);
}
"""

def create_sun():
    # Initialize glfw
    if not glfw.init():
        return

    window = glfw.create_window(640, 480, "Sun", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    # Create shader program
    shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

    # Create sun circle
    circle = []
    for i in range(361):
        circle.append(math.sin(math.radians(i)) * 0.2)
        circle.append(math.cos(math.radians(i)) * 0.2 + 0.8 - 0.1)

    circle = np.array(circle, dtype=np.float32)

    # Create sunrays
    rays = []
    for i in range(8):
        angle = i * (360 / 8)
        x = math.sin(math.radians(angle)) * 0.2
        y = math.cos(math.radians(angle)) * 0.2 + 0.8 - 0.1
        rays.extend([x, y])
        x = math.sin(math.radians(angle + 10)) * 0.3
        y = math.cos(math.radians(angle + 10)) * 0.3 + 0.8 - 0.1
        rays.extend([x, y])
        x = math.sin(math.radians(angle - 10)) * 0.3
        y = math.cos(math.radians(angle - 10)) * 0.3 + 0.8 - 0.1
        rays.extend([x, y])

    rays = np.array(rays, dtype=np.float32)


    # Create Vertex Buffer Object for circle and rays
    VBO_circle = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO_circle)
    glBufferData(GL_ARRAY_BUFFER, circle.nbytes, circle, GL_STATIC_DRAW)

    VBO_rays = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO_rays)
    glBufferData(GL_ARRAY_BUFFER, rays.nbytes, rays, GL_STATIC_DRAW)

    # Create Vertex Array Object for circle and rays
    VAO_circle = glGenVertexArrays(1)
    glBindVertexArray(VAO_circle)
    glBindBuffer(GL_ARRAY_BUFFER, VBO_circle)
    glVertexAttribPointer(0, 2,GL_FLOAT,GL_FALSE ,0,None)
    glEnableVertexAttribArray(0)

    VAO_rays = glGenVertexArrays(1)
    glBindVertexArray(VAO_rays)
    glBindBuffer(GL_ARRAY_BUFFER,VBO_rays)
    glVertexAttribPointer(0 ,2 ,GL_FLOAT ,GL_FALSE ,0 ,None)
    glEnableVertexAttribArray(0)

    glUseProgram(shader)

    glClearColor(0.5 ,0.5 ,1 ,1)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT)

        glBindVertexArray(VAO_circle)
        glDrawArrays(GL_TRIANGLE_FAN ,0 ,362)

        glBindVertexArray(VAO_rays)
        glDrawArrays(GL_TRIANGLES ,0 ,24)

        glfw.swap_buffers(window)

create_sun()