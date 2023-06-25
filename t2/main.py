from scene_setup import SceneSetup
from objects import Object
from OpenGL.GL import *
from screeninfo import get_monitors
from cat import Cat
from moon import Moon
import json

vertex_code = """
        attribute vec3 position;
        attribute vec2 texture_coord;
        varying vec2 out_texture;
                
        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;        
        
        void main(){
            gl_Position = projection * view * model * vec4(position,1.0);
            out_texture = vec2(texture_coord);
        }
"""

fragment_code = """
        varying vec2 out_texture;
        uniform sampler2D samplerTexture;
        uniform vec4 color;
        uniform int hasTexture;
        
        void main(){
            vec4 texture = texture2D(samplerTexture, out_texture);
            if (hasTexture == 1) {
                gl_FragColor = texture;
            } else {
                gl_FragColor = color;
            }
        }
"""


primary_monitor = get_monitors()[0]
screen_width = primary_monitor.width
screen_height = primary_monitor.height

scene = SceneSetup(screen_width, screen_height, "Project 2")

scene.add_shader(vertex_code, GL_VERTEX_SHADER)
scene.add_shader(fragment_code, GL_FRAGMENT_SHADER)


objects = [
    {
        'name': 'cat',
        'customClass': Cat,
    },
    {
        'name': 'penguin'
    },
    {
        'name': 'penguin2'
    },
    {
        'name': 'box'
    },
    {
        'name': 'ground'
    },
    {
        'name': 'quetzcoatlus'
    },
    {
        'name': 'house'
    },
    {
        'name': 'skybox',
    },
    {
        'name': 'moon',
        'customClass': Moon,
    },
    {
        'name': 'grass'
    },
    {
        'name': 'bed'
    },
]

added_objects = {}

initial_model_states = json.load(open('initialModelStates.json'))

for obj in objects:

    name = obj['name']

    obj_file = f'3dModels/{name}/{name}.obj'
    texture_file = f'3dModels/{name}/{name}.jpg'
    initital_model_state = initial_model_states[name] if name in initial_model_states else None

    if 'customClass' in obj:
        added_objects[name] = obj['customClass'](obj_file, texture_file, initital_model_state)
    else:
        added_objects[name] = Object(obj_file, texture_file, initital_model_state)

    
    scene.add_object(added_objects[name])

scene.start_program()

scene.run()