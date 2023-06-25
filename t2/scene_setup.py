import glfw
from OpenGL.GL import *
import numpy as np
import glm
from PIL import Image

LIMITS = {
    'x': (-98, 98),
    'y': (2, 98),
    'z': (-98, 98),
}

class SceneSetup:
    objects_function = []
    shaders = []
    objects = []
    objects_in_scene = []
    uniform_locations = {}

    time = 0
    polygonal_mode = False
    camera_pos   = glm.vec3(0,5,0)
    camera_front = glm.vec3(0.0,  0.0, -1.0)
    camera_up    = glm.vec3(0.0,  1.0,  0.0)
    first_mouse = True
    yaw = -90.0
    pitch = 0.0
    projection_angle = 45.0

    def __init__(self, width, height, window_title, camera_speed = 0.8, sensitivity = 0.3, initial_color = (255,255,255)):
        self.height = height
        self.width = width
        self.window_title = window_title
        self.camera_speed = camera_speed
        self.sensitivity = sensitivity
        self.initial_color = initial_color
        self.last_x =  width/2
        self.last_y =  height/2

    def __convert_rgb__(self, color):
        return color[0]/255.0 , color[1]/255.0 , color[2]/255.0, 1.0

    # Creates a shader, sets it's source, compiles it and attaches it to a program
    def __setup_shader__(self, program, shaderSrc, shaderType):

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
    
    def __build_program__(self, program):
        glLinkProgram(program)
        if not glGetProgramiv(program, GL_LINK_STATUS):
            programLog = glGetProgramInfoLog(program)
            raise RuntimeError(f'Error linking program: {programLog}')

    def __init_window__(self):
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)
        window = glfw.create_window(self.width, self.height, self.window_title, None, None)
        glfw.make_context_current(window)

        return window
    

    def __load_objects__(self):
        for obj in self.objects:
            object_vbo = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, object_vbo)
            glBufferData(GL_ARRAY_BUFFER, obj.vertices_data.nbytes, obj.vertices_data, GL_STATIC_DRAW)

            object_vao = glGenVertexArrays(1)
            glBindVertexArray(object_vao)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
            glEnableVertexAttribArray(0)

            texture = None
            object_texture_vbo = None

            if obj.texture_filename is not None:
                texture = glGenTextures(1)
                self.load_texture_file(texture, obj.texture_filename)

                object_texture_vbo = glGenBuffers(1)
                glBindBuffer(GL_TEXTURE_BUFFER, object_texture_vbo)
                glBufferData(GL_TEXTURE_BUFFER, obj.textures_coord_data.nbytes, obj.textures_coord_data, GL_STATIC_DRAW)

                glBindBuffer(GL_ARRAY_BUFFER, object_texture_vbo)
                glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, None)
                glEnableVertexAttribArray(1)

            object_normal_vbo = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, object_normal_vbo)
            glBufferData(GL_ARRAY_BUFFER, obj.normals_data.nbytes, obj.normals_data, GL_STATIC_DRAW)

            glBindBuffer(GL_ARRAY_BUFFER, object_normal_vbo)
            glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, None)
            glEnableVertexAttribArray(2)

            self.objects_in_scene.append({
                "vao": object_vao,
                "vbo": object_vbo,
                "texture": texture,                
                "texture_vbo": object_texture_vbo,
                "normal_vbo": object_normal_vbo,
                "obj": obj
            })

    def __handle_key_event__(self, window, key, scancode, action, mods):
        for obj in self.objects:
            obj.__handle_key_event__(window, key, scancode, action, mods)

        if key == glfw.KEY_W and action != glfw.RELEASE:
            self.camera_pos += self.camera_speed * self.camera_front

        if key == glfw.KEY_S and action != glfw.RELEASE:
            self.camera_pos -= self.camera_speed * self.camera_front

        if key == glfw.KEY_A and action != glfw.RELEASE:
            self.camera_pos -= glm.normalize(glm.cross(self.camera_front, self.camera_up)) * self.camera_speed

        if key == glfw.KEY_D and action != glfw.RELEASE:
            self.camera_pos += glm.normalize(glm.cross(self.camera_front, self.camera_up)) * self.camera_speed

        if self.camera_pos[0] < LIMITS['x'][0]:
            self.camera_pos[0] = LIMITS['x'][0]
        elif self.camera_pos[0] > LIMITS['x'][1]:
            self.camera_pos[0] = LIMITS['x'][1]
        
        if self.camera_pos[1] < LIMITS['y'][0]:
            self.camera_pos[1] = LIMITS['y'][0]
        elif self.camera_pos[1] > LIMITS['y'][1]:
            self.camera_pos[1] = LIMITS['y'][1]

        if self.camera_pos[2] < LIMITS['z'][0]:
            self.camera_pos[2] = LIMITS['z'][0]
        elif self.camera_pos[2] > LIMITS['z'][1]:
            self.camera_pos[2] = LIMITS['z'][1]

        if key == glfw.KEY_P and action != glfw.RELEASE:
            self.polygonal_mode = not self.polygonal_mode

        if key == glfw.KEY_MINUS and action != glfw.RELEASE:
            self.sensitivity -= 0.01

        if key == glfw.KEY_EQUAL and action != glfw.RELEASE:
            self.sensitivity += 0.01

        if key == glfw.KEY_Z and action != glfw.RELEASE:
            self.projection_angle -= 1
        if key == glfw.KEY_X and action != glfw.RELEASE:
            self.projection_angle += 1
        
        if self.projection_angle < 45:
            self.projection_angle = 45
        elif self.projection_angle > 90:
            self.projection_angle = 90
            
    
    def __handle_mouse_event__(self, window, xpos, ypos):

        if self.first_mouse:
            self.last_x = xpos
            self.last_y = ypos
            self.first_mouse = False

        xoffset = (xpos - self.last_x) * self.sensitivity
        yoffset = (self.last_y - ypos) * self.sensitivity

        self.last_x = xpos
        self.last_y = ypos

        self.yaw += xoffset;
        self.pitch += yoffset;


        if self.pitch >= 90.0: self.pitch = 90.0
        if self.pitch <= -90.0: self.pitch = -90.0

        front = glm.vec3()
        front.x = np.cos(glm.radians(self.yaw)) * np.cos(glm.radians(self.pitch))
        front.y = np.sin(glm.radians(self.pitch))
        front.z = np.sin(glm.radians(self.yaw)) * np.cos(glm.radians(self.pitch))

        self.camera_front = glm.normalize(front)

    def load_texture_file(self,texture_id, texture_file):
        glBindTexture(GL_TEXTURE_2D, texture_id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        img = Image.open(texture_file)
        img_width = img.size[0]
        img_height = img.size[1]
        image_data = img.tobytes("raw", "RGB", 0, -1)
        
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_width, img_height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)


    def add_shader(self, shaderSrc, shader_type):
        self.shaders.append(
            {
                "shader": None,
                "shaderSrc": shaderSrc,
                "shaderType": shader_type
            }
        )

    def add_object(self, object):
        self.objects.append(object)

    def get_uniform_location(self, uniform_name):
        if uniform_name not in self.uniform_locations:
            self.uniform_locations[uniform_name] = glGetUniformLocation(self.program, uniform_name)
        return self.uniform_locations[uniform_name]

    def start_program(self):
        glfw.init()
        self.window = self.__init_window__()
        
        self.program = glCreateProgram()
        
        for shader in self.shaders:
            shader["shader"] = self.__setup_shader__(self.program, shader["shaderSrc"], shader["shaderType"])
        
        self.__build_program__(self.program)

        glUseProgram(self.program)

        self.__load_objects__()

        glfw.set_key_callback(self.window, self.__handle_key_event__)
        glfw.set_cursor_pos_callback(self.window, self.__handle_mouse_event__)

        r,g,b,a = self.__convert_rgb__(self.initial_color)
        glClearColor(r,g,b,a)

        glEnable(GL_DEPTH_TEST)

        glfw.show_window(self.window)
    
    
    def get_view(self):
        view = glm.lookAt(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up);
        view = np.array(view)
        return view

    def get_projection(self):
        # perspective parameters: fovy, aspect, near, far
        projection = glm.perspective(glm.radians(self.projection_angle), self.width/self.height, 0.1, 1000.0)
        projection = np.array(projection)
        return projection

    def run(self):
        while not glfw.window_should_close(self.window):            
            if self.time > 100000:
                self.time = 0

            self.time += 1

            for obj in self.objects:
                if hasattr(obj, '__handle_time_event__'):
                    obj.__handle_time_event__(self.time)

            glfw.poll_events()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            if self.polygonal_mode==True:
                glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
            else:
                glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)

            for objSc in self.objects_in_scene:

                obj = objSc["obj"]
                vao = objSc["vao"]
                texture = objSc["texture"]

                glBindVertexArray(vao)

                glUniformMatrix4fv(self.get_uniform_location("model"), 1, GL_TRUE, obj.get_model())

                glUniform1f(self.get_uniform_location("ka"), obj.light_state["ka"])

                glUniform1f(self.get_uniform_location("kd"), obj.light_state["kd"])

                glUniform1f(self.get_uniform_location("ks"), obj.light_state["ks"])
                
                glUniform1f(self.get_uniform_location("ns"), obj.light_state["ns"])

                if hasattr(obj, 'light_position'):
                    glUniform3f(self.get_uniform_location("lightPos"), obj.light_position[0], obj.light_position[1], obj.light_position[2])

                if texture is not None:
                    glUniform1i(self.get_uniform_location("hasTexture"), 1)
                    glBindTexture(GL_TEXTURE_2D, texture)
                else:
                    r,g,b,a = self.__convert_rgb__(obj.color)
                    glUniform1i(self.get_uniform_location("hasTexture"), 0)
                    glUniform4f(self.get_uniform_location("color"), r, g, b, a)
                                
                glDrawArrays(obj.drawing_mode, 0, obj.vertices_data.size)

                glBindVertexArray(0)


            glUniformMatrix4fv(self.get_uniform_location("view"), 1, GL_TRUE, self.get_view())

            glUniformMatrix4fv(self.get_uniform_location("projection"), 1, GL_TRUE, self.get_projection())

            glUniform3f(self.get_uniform_location("viewPos"), self.camera_pos[0], self.camera_pos[1], self.camera_pos[2])

            glfw.swap_buffers(self.window)
        
        glfw.terminate()