import glfw
import glm
import numpy as np
from objects import Object

class Cat(Object):

    def __init__(self, obj_filename, texture_filename, initial_model_state = None, color=(255,0,0)):
        super().__init__(obj_filename, texture_filename, initial_model_state, color)
        self.angle = 0
        self.radius = 6
        self.starting_model_state = self.model_state.copy()
    

    def __handle_time_event__(self, time):

        if time % 2 == 0:
            self.angle += 0.1
            x = self.radius * np.cos(self.angle)
            z = self.radius * np.sin(self.angle)

            self.model_state['translateX'] = self.starting_model_state['translateX'] + x
            self.model_state['translateZ'] = self.starting_model_state['translateZ'] + z
            

            if self.angle >= 2 * np.pi:
                self.angle = 0

    def get_model(self):
        model = glm.mat4(1.0)

        model = glm.translate(model, glm.vec3(self.model_state['translateX'], self.model_state['translateY'], self.model_state['translateZ']))

        model = glm.rotate(model, np.radians(self.model_state['angle']), glm.vec3(self.model_state['rotateX'], self.model_state['rotateY'], self.model_state['rotateZ']))

        model = glm.rotate(model, -self.angle, glm.vec3(0, 0, 1))
        
        model = glm.scale(model, glm.vec3(self.model_state['scaleX'], self.model_state['scaleY'], self.model_state['scaleZ']))

        model = np.array(model)

        return model


