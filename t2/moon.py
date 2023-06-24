import glfw
import glm
import numpy as np
from objects import Object

class Moon(Object):

    def __init__(self, obj_filename, texture_filename, initial_model_state = None, color=(255,0,0)):
        super().__init__(obj_filename, texture_filename, initial_model_state, color)
        self.angle = 0
        self.radius = 90
        self.starting_model_state = self.model_state.copy()
    

    def __handle_time_event__(self, time):

        if time % 2 == 0:
            self.angle += 0.02
            x = self.radius * np.cos(self.angle)
            z = self.radius * np.sin(self.angle)

            self.model_state['translateX'] = self.starting_model_state['translateX'] + x
            self.model_state['translateZ'] = self.starting_model_state['translateZ'] + z
            

            if self.angle >= 2 * np.pi:
                self.angle = 0

