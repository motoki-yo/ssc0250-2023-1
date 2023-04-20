### Grupo CG
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math

glfw.init()
glfw.window_hint(glfw.VISIBLE, glfw.FALSE);
window = glfw.create_window(1000, 1000, "Trabalho", None, None)
glfw.make_context_current(window)

vertex_code = """
        attribute vec2 position;
        uniform mat4 mat;
        void main(){
            gl_Position = mat * vec4(position,0.0,1.0);
        }
        """

fragment_code = """
        uniform vec4 color;
        void main(){
            gl_FragColor = color;
        }
        """

# Request a program and shader slots from GPU
program  = glCreateProgram()
vertex   = glCreateShader(GL_VERTEX_SHADER)
fragment = glCreateShader(GL_FRAGMENT_SHADER)

# Set shaders source
glShaderSource(vertex, vertex_code)
glShaderSource(fragment, fragment_code)

# Compile shaders
glCompileShader(vertex)
if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(vertex).decode()
    print(error)
    raise RuntimeError("Erro de compilacao do Vertex Shader")
    
glCompileShader(fragment)
if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(fragment).decode()
    print(error)
    raise RuntimeError("Erro de compilacao do Fragment Shader")
    
# Attach shader objects to the program
glAttachShader(program, vertex)
glAttachShader(program, fragment)

# Build program
glLinkProgram(program)
if not glGetProgramiv(program, GL_LINK_STATUS):
    print(glGetProgramInfoLog(program))
    raise RuntimeError('Linking error')
    
# Make program the default program
glUseProgram(program)

# preparando espaço para 3 vértices usando 2 coordenadas (x,y)
num_vertices = 531
peixe_betta = np.zeros(num_vertices, [("position", np.float32, 2)])

### Peixe
# TORSO
peixe_betta[0] = [-0.625, 0.25]
peixe_betta[1] = [0.0, 0.0]
peixe_betta[2] = [-0.625, -0.25]

# NAD1
peixe_betta[3] = [-0.45, 0.3]
peixe_betta[4] = [-0.25, 0.20]
peixe_betta[5] = [-0.370, 0.0]
#NAD2
peixe_betta[6] = [-0.45, -0.3]
peixe_betta[7] = [-0.25, -0.20]
peixe_betta[8] = [-0.370, 0.0]

#CAUD 1
peixe_betta[9] = [-0.75, 0.375]
peixe_betta[10] = [-0.625, 0.0]
peixe_betta[11] = [-1.0, 0.25]
#CAUD2
peixe_betta[12] = [-1.05, 0.175]
peixe_betta[13] = [-0.625, 0.0]
peixe_betta[14] = [-1.05, -0.175]
#CAUD3
peixe_betta[15] = [-1.0, -0.25]
peixe_betta[16] = [-0.625, 0.0]
peixe_betta[17] = [-0.75, -0.375]

# Olho do peixe

for i in range(18,50):
    x = 0.07  * math.cos(i * (2 * math.pi / 32) ) - 0.3
    y = 0.07 * math.sin(i * (2 * math.pi / 32) ) + 0.01
    peixe_betta[i] = [x,y]
    
# Pupila do peixe

for i in range(51,83):
    x = 0.04 * math.cos(i * (2 * math.pi / 32) ) - 0.275
    y = 0.04 * math.sin(i * (2 * math.pi / 32) ) 
    peixe_betta[i] = [x,y]
    
# Definindo o fator de escala
factor = 0.3

# Aplicando a transformação de escala em cada vértice
for i in range(0, 83):
    for vertex in peixe_betta[i]:
        vertex *= factor


# Request a buffer slot from GPU
buffer = glGenBuffers(1)
# Make this buffer the default one
glBindBuffer(GL_ARRAY_BUFFER, buffer)


# Upload data
glBufferData(GL_ARRAY_BUFFER, peixe_betta.nbytes, peixe_betta, GL_DYNAMIC_DRAW)
glBindBuffer(GL_ARRAY_BUFFER, buffer)

# Bind the position attribute
# --------------------------------------
stride = peixe_betta.strides[0]
offset = ctypes.c_void_p(0)


loc = glGetAttribLocation(program, "position")
glEnableVertexAttribArray(loc)

glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, offset)

locb = glGetAttribLocation(program, "position")
glEnableVertexAttribArray(locb)

glVertexAttribPointer(locb, 2, GL_FLOAT, False, stride, offset)

loc_color = glGetUniformLocation(program, "color")
R = 0.0
G = 0.0
B = 0.0

# translacao
x_peixe = 0.0

# coeficiente de escala
s_inc = 1.0


def key_event(window,key,scancode,action,mods):
    global x_peixe, s_inc
    
    if key == 67: x_peixe -= 0.0001 ###tecla C para mover o peixe
    if key == 86: x_peixe += 0.0001 ###tecla V para mover o peixe
        
    if key == 90: s_inc += 0.01 ### tecla Z para aumentar
    if key == 88: s_inc -= 0.01 ### tecla X para dimminuir 

    
glfw.set_key_callback(window,key_event)

glfw.show_window(window)

tx_peixe = 0.0
s_x = 1.0
s_y = 1.0



def multiplica_matriz(a,b):
    m_a = a.reshape(4,4)
    m_b = b.reshape(4,4)
    m_c = np.dot(m_a,m_b)
    c = m_c.reshape(1,16)
    return c




while not glfw.window_should_close(window):
    tx_peixe += x_peixe
    s_x = s_inc
    s_y = s_inc
 
    glfw.poll_events() 

    
    glClear(GL_COLOR_BUFFER_BIT) 
    glClearColor(0.0, 1.0, 1.0, 1.0)
    
    
    #Matrizes

    
    ### Peixe
    
    mat_trans_peixe = np.array([ 1.0, 0.0, 0.0, tx_peixe, 
                                  0.0, 1.0, 0.0, 0.0, 
                                  0.0, 0.0, 1.0, 0.0, 
                                  0.0, 0.0, 0.0, 1.0], np.float32)
    
 

   #Matrizes  
    mat_scale =    np.array([  s_x, 0.0, 0.0, 0.0, 
                               0.0, s_y, 0.0, 0.0, 
                               0.0, 0.0, 1.0, 0.0, 
                               0.0, 0.0, 0.0, 1.0], np.float32)

    
    ### Matriz peixe
    mat_peixe = multiplica_matriz(mat_trans_peixe,mat_scale)

    loc = glGetUniformLocation(program, "mat")
    

    glUniform4f(loc_color, 0.0, 0.75, 0.75, 1.0) ### modificando a cor do objeto!
    glDrawArrays(GL_TRIANGLE_FAN, 466, 64)
    
    ### Peixe
    glUniformMatrix4fv(loc, 1, GL_TRUE, mat_trans_peixe)
    
    glUniform4f(loc_color, float(206) / 255.0, float(66) / 255.0, float(87) / 255.0, 1.0);
    glDrawArrays(GL_TRIANGLES, 3, 3) # NAD1
    
    glUniform4f(loc_color, float(206) / 255.0, float(66) / 255.0, float(87) / 255.0, 1.0);
    glDrawArrays(GL_TRIANGLES, 6, 3) # NAD2
    
    glUniform4f(loc_color, float(255) / 255.0, float(127) / 255.0, float(81) / 255.0, 1.0);
    glDrawArrays(GL_TRIANGLES, 0, 3) # TORSO
    
    glUniform4f(loc_color, float(206) / 255.0, float(66) / 255.0, float(87) / 255.0, 1.0);
    glDrawArrays(GL_TRIANGLES, 9, 3) # CAUD1
    
    glUniform4f(loc_color, float(206) / 255.0, float(66) / 255.0, float(87) / 255.0, 1.0);
    glDrawArrays(GL_TRIANGLES, 12, 3) # CAUD2

    glUniform4f(loc_color, float(206) / 255.0, float(66) / 255.0, float(87) / 255.0, 1.0);
    glDrawArrays(GL_TRIANGLES, 15, 3) # CAUD3
    
    glUniform4f(loc_color, 1.0, 1.0, 1.0, 1.0) 
    glDrawArrays(GL_TRIANGLE_FAN, 18, 32) #OLHO
    
    glUniform4f(loc_color, 0.0, 0.0, 0.0, 0.0) 
    glDrawArrays(GL_TRIANGLE_FAN, 51, 32) #PUPILA
    
    glfw.swap_buffers(window)

glfw.terminate()