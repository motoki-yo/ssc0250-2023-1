import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import math

vertex_src = """
# version 330

in vec2 a_position;
uniform mat4 u_transformation;

void main()
{
    gl_Position = u_transformation * vec4(a_position, 0.0, 1.0);
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

moon_fragment_src = """
# version 330

out vec4 out_color;

void main()
{
    out_color = vec4(0.7, 0.7, 0.7, 1.0);
}
"""



def multiplica_matriz(a,b):
    m_a = a.reshape(4,4)
    m_b = b.reshape(4,4)
    m_c = np.dot(m_a,m_b)
    c = m_c.reshape(1,16)
    return c

def key_event(window, key, scancode, action, mods):
    global angle

    # Rotate the sun only once when the left or right arrow key is pressed
    # if key == glfw.KEY_LEFT and action == glfw.PRESS:
    #     angle -= 5
    # elif key == glfw.KEY_RIGHT and action == glfw.PRESS:
    #     angle += 5

    # Keep the sun rotating as long as the left or right arrow key is pressed
    if key == glfw.KEY_LEFT and action != glfw.RELEASE:
        angle += 2
    elif key == glfw.KEY_RIGHT and action != glfw.RELEASE:
        angle -= 2

    # Keep the angle between 0 and 360
    if angle % 360 == 0:
        angle = 0 
    
    print(angle)

    # Change the background color based on the angle
    if abs(angle) >= 280 or abs(angle) <= 80:
        glClearColor(0.5 ,0.5 ,1 ,1) # Blue sky
    else:
        glClearColor(0.3 ,0.3 ,0.5 ,1) # Night sky



def create_sun():
    global angle
    angle = 338 # Sun starts at the right position

    # Initialize glfw
    if not glfw.init():
        return
    
    window_width = 720
    window_height = 600
    window = glfw.create_window(window_width, window_height, "Sun", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_event)

    glfw.make_context_current(window)

    # Create shader program
    shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))
    moon_shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(moon_fragment_src, GL_FRAGMENT_SHADER))

    # Create sun circle
    circle = []
    for i in range(361):
        circle.append(math.sin(math.radians(i)) * 0.15)
        circle.append(math.cos(math.radians(i)) * 0.15 + 0.8 - 0.1)

    circle = np.array(circle, dtype=np.float32)

    # Create moon circle
    moon_circle = []
    for i in range(361):
        moon_circle.append(math.sin(math.radians(i)) * 0.15)
        moon_circle.append(math.cos(math.radians(i)) * 0.15 + 0.8 - 0.1)

    moon_circle = np.array(moon_circle, dtype=np.float32)

    # Create sunrays
    rays = []
    for i in range(8):
        ray_angle = i * (360 / 8)
        x = math.sin(math.radians(ray_angle)) * 0.2
        y = math.cos(math.radians(ray_angle)) * 0.2 + 0.8 - 0.1
        rays.extend([x, y])
        x = math.sin(math.radians(ray_angle + 10)) * 0.3
        y = math.cos(math.radians(ray_angle + 10)) * 0.3 + 0.8 - 0.1
        rays.extend([x, y])
        x = math.sin(math.radians(ray_angle - 10)) * 0.3
        y = math.cos(math.radians(ray_angle - 10)) * 0.3 + 0.8 - 0.1
        rays.extend([x, y])

    rays = np.array(rays, dtype=np.float32)

    # Create Vertex Buffer Object for circle and rays
    VBO_circle = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER,VBO_circle)
    glBufferData(GL_ARRAY_BUFFER,circle.nbytes,circle,GL_STATIC_DRAW)

    VBO_moon_circle = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER,VBO_moon_circle)
    glBufferData(GL_ARRAY_BUFFER,moon_circle.nbytes,moon_circle,GL_STATIC_DRAW)

    VBO_rays = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER,VBO_rays)
    glBufferData(GL_ARRAY_BUFFER,rays.nbytes,rays,GL_STATIC_DRAW)

    # Create Vertex Array Object for circle and rays
    VAO_circle = glGenVertexArrays(1)
    glBindVertexArray(VAO_circle)
    glBindBuffer(GL_ARRAY_BUFFER,VBO_circle)
    glVertexAttribPointer(0 ,2 ,GL_FLOAT ,GL_FALSE ,0 ,None)
    glEnableVertexAttribArray(0)

    VAO_moon_circle = glGenVertexArrays(1)
    glBindVertexArray(VAO_moon_circle)
    glBindBuffer(GL_ARRAY_BUFFER,VBO_moon_circle)
    glVertexAttribPointer(0 ,2 ,GL_FLOAT ,GL_FALSE ,0 ,None)
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

        # Drawing the sun
        glUseProgram(shader)

        sun_translation = np.array([[1.0, 0.0, 0.0, 0],
                [0.0, 1.0, 0.0, -0.9],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0]], dtype=np.float32)
        
        sun_translation2 = np.array([[1.0, 0.0, 0.0, 0],
                [0.0, 1.0, 0.0, 0.9],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0]], dtype=np.float32)
        
        sun_scaling = np.array([[1.0, 0.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 0.0],
                    [0.0, 0.0, 0.0, 1.]], dtype=np.float32)
        
        sun_rotation = np.array([[math.cos(math.radians(angle)), -math.sin(math.radians(angle)), 0.0, 0.0],
                     [math.sin(math.radians(angle)), math.cos(math.radians(angle)), 0.0, 0.0],
                     [0.0, 0.0, 1.0, 0.0],
                     [0.0, 0.0, 0.0, 1.]], dtype=np.float32)
        
        sun_transformation = multiplica_matriz(sun_translation, sun_rotation)
        sun_transformation = multiplica_matriz(sun_transformation, sun_translation2)

        glUniformMatrix4fv(glGetUniformLocation(shader, "u_transformation"), 1, GL_TRUE, sun_transformation)

        glClear(GL_COLOR_BUFFER_BIT)

        glBindVertexArray(VAO_circle)
        glDrawArrays(GL_TRIANGLE_FAN ,0 ,362)

        glBindVertexArray(VAO_rays)
        glDrawArrays(GL_TRIANGLES ,0 ,24)

        # Drawing the moon
        glUseProgram(moon_shader)


        moon_translation = np.array([[1.0, 0.0, 0.0, 0],
                [0.0, 1.0, 0.0, -1],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0]], dtype=np.float32)
        
        moon_translation2 = np.array([[1.0, 0.0, 0.0, 0],
                [0.0, 1.0, 0.0, 1],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0]], dtype=np.float32)
        
        moon_scaling = np.array([[1.0, 0.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 0.0],
                    [0.0, 0.0, 0.0, 1.]], dtype=np.float32)
        
        moon_rotation = np.array([[math.cos(math.radians(angle + 180)), -math.sin(math.radians(angle + 180)), 0.0, 0.0],
                     [math.sin(math.radians(angle + 180)), math.cos(math.radians(angle + 180)), 0.0, 0.0],
                     [0.0, 0.0, 1.0, 0.0],
                     [0.0, 0.0, 0.0, 1.]], dtype=np.float32)
        
        moon_transformation = multiplica_matriz(moon_translation, moon_rotation)
        moon_transformation = multiplica_matriz(moon_transformation, moon_translation2)

        glUniformMatrix4fv(glGetUniformLocation(moon_shader, "u_transformation"), 1, GL_TRUE, moon_transformation)

        glBindVertexArray(VAO_moon_circle)
        glDrawArrays(GL_TRIANGLE_FAN ,0 ,362)

        glfw.swap_buffers(window)

create_sun()