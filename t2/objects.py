import numpy as np
from OpenGL.GL import *
import glm
from wavefront import parse_wavefront_file

def parse_initial_model_state(state_obj):

    default_model_state = {
        "translateX": 0.0,
        "translateY": 0.0,
        "translateZ": 0.0,

        "angle": 0.0,
        "rotateX": 0.0,
        "rotateY": 0.0,
        "rotateZ": 1.0,

        "scaleX": 1.0,
        "scaleY": 1.0,
        "scaleZ": 1.0
    }

    model_state = default_model_state

    if state_obj is None:
        return model_state
    
    if 'scale' in state_obj:
        model_state['scaleX'] = state_obj['scale']
        model_state['scaleY'] = state_obj['scale']
        model_state['scaleZ'] = state_obj['scale']
    
    for key in state_obj:
        if key in model_state:
            model_state[key] = state_obj[key]
    
    return model_state


def parse_initial_light_state(state_obj):
    
    default_light_state = {
            "ka": 0.5,
            "kd": 0.5,
            "ks": 0.9,
            "ns": 32,
    }

    light_state = default_light_state

    if state_obj is None:
        return light_state

    for key in state_obj:
        if key in light_state:
            light_state[key] = state_obj[key]
    
    return light_state

class Object():

    vertices_data = None
    textures_coord_data = None


    def __init__(self, obj_filename, texture_filename, initial_state = None, color=(255,0,0)):
        self.obj_filename = obj_filename
        self.texture_filename = texture_filename
        self.color = color
        self.model_state = parse_initial_model_state(initial_state)
        self.light_state = parse_initial_light_state(initial_state)

        self.vertices_list = []
        self.normals_list = []
        self.textures_coord_list = []
        self.drawing_mode = GL_TRIANGLES

        model = parse_wavefront_file(obj_filename)

        sample_face = model['faces'][0]

        if len(sample_face[0]) == 4:
            self.drawing_mode = GL_QUADS

        for face in model['faces']:
            for vertice_id in face[0]:
                self.vertices_list.append( model['vertices'][vertice_id-1] )
            for texture_id in face[1]:
                self.textures_coord_list.append( model['texture'][texture_id-1] )
            for normal_id in face[2]:
                self.normals_list.append( model['normals'][normal_id-1] )

        self.vertices_data = np.zeros(len(self.vertices_list), [("position", np.float32, 3)])
        self.vertices_data['position'] = self.vertices_list

        self.textures_coord_data = np.zeros(len(self.textures_coord_list), [("texture_coord", np.float32, 2)])

        self.textures_coord_data['texture_coord'] = self.textures_coord_list

        self.normals_data = np.zeros(len(self.normals_list), [("normals", np.float32, 3)])

        self.normals_data['normals'] = self.normals_list


    def get_model(self):
        model = glm.mat4(1.0)

        model = glm.translate(model, glm.vec3(self.model_state['translateX'], self.model_state['translateY'], self.model_state['translateZ']))

        model = glm.rotate(model, np.radians(self.model_state['angle']), glm.vec3(self.model_state['rotateX'], self.model_state['rotateY'], self.model_state['rotateZ']))
        
        model = glm.scale(model, glm.vec3(self.model_state['scaleX'], self.model_state['scaleY'], self.model_state['scaleZ']))

        model = np.array(model)

        return model

    def __handle_key_event__(self, window, key, scancode, action, mods):
        pass
