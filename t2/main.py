from scene_setup import SceneSetup
from objects import Object
from OpenGL.GL import *
from screeninfo import get_monitors

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

box = Object('obj/caixa/caixa.obj', 'obj/caixa/caixa.jpg')

house = Object('obj/casa/casa.obj', 'obj/casa/casa.jpg')

scene = SceneSetup(screen_width, screen_height, "Project 2")

scene.add_shader(vertex_code, GL_VERTEX_SHADER)
scene.add_shader(fragment_code, GL_FRAGMENT_SHADER)

scene.add_object(box)

scene.add_object(house)

scene.start_program()

scene.run()