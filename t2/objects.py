import glfw
import numpy as np
from OpenGL.GL import *
import glm
from wavefront import parse_wavefront_file

class Object():
    vertices_list = []
    textures_coord_list = []

    vertices_data = None
    textures_coord_data = None

    translateX = 0.0
    translateY = 0.0
    translateZ = 0.0

    angle = 0.0
    rotateX = 0.0
    rotateY = 0.0
    rotateZ = 1.0

    scaleX = 1.0
    scaleY = 1.0
    scaleZ = 1.0

    def __init__(self, obj_filename, texture_filename, color=(255,0,0)):
        self.obj_filename = obj_filename
        self.texture_filename = texture_filename
        self.color = color

        model = parse_wavefront_file(obj_filename)
        
        for face in model['faces']:
            for vertice_id in face[0]:
                self.vertices_list.append( model['vertices'][vertice_id-1] )
            for texture_id in face[1]:
                self.textures_coord_list.append( model['texture'][texture_id-1] )

        self.vertices_data = np.zeros(len(self.vertices_list), [("position", np.float32, 3)])
        self.vertices_data['position'] = self.vertices_list

        self.textures_coord_data = np.zeros(len(self.textures_coord_list), [("texture_coord", np.float32, 2)])

        self.textures_coord_data['texture_coord'] = self.textures_coord_list


    def get_model(self):
        model = glm.mat4(1.0)

        model = glm.translate(model, glm.vec3(self.translateX, self.translateY, self.translateZ))

        model = glm.rotate(model, np.radians(self.angle), glm.vec3(self.rotateX, self.rotateY, self.rotateZ))
        
        model = glm.scale(model, glm.vec3(self.scaleX, self.scaleY, self.scaleZ))

        model = np.array(model)

        return model

    def handleKeyEvent(self, window, key, scancode, action, mods):
        pass
