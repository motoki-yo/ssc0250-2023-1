from scene_setup import SceneSetup
from objects import Object
from screeninfo import get_monitors
from cat import Cat
from moon import Moon
import json

vertex_code = """
        attribute vec3 position;
        attribute vec2 texture_coord;
        attribute vec3 normals;

        varying vec2 out_texture;
        varying vec3 out_fragPos;
        varying vec3 out_normal;
                
        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;        
        
        void main(){
            gl_Position = projection * view * model * vec4(position,1.0);
            out_texture = vec2(texture_coord);
            out_fragPos = vec3(model * vec4(position, 1.0));
            out_normal = vec3(model * vec4(normals, 1.0));
        }
"""

fragment_code = """

        // parametro com a cor da(s) fonte(s) de iluminacao
        uniform vec3 lightPos; // define coordenadas de posicao da luz
        vec3 lightColor = vec3(1.0, 1.0, 1.0);

        // parametros da iluminacao ambiente e difusa
        uniform float ka; // coeficiente de reflexao ambiente
        uniform float kd; // coeficiente de reflexao difusa

        // parametros da iluminacao especular
        uniform vec3 viewPos; // define coordenadas com a posicao da camera/observador
        uniform float ks; // coeficiente de reflexao especular
        uniform float ns; // expoente de reflexao especular
        
        // parametros recebidos do vertex shader
        varying vec2 out_texture; // recebido do vertex shader
        varying vec3 out_normal; // recebido do vertex shader
        varying vec3 out_fragPos; // recebido do vertex shader
        uniform sampler2D samplerTexture;
        uniform vec4 color;
        uniform int hasTexture;
        
        void main(){

            // calculando reflexao ambiente
            vec3 ambient = ka * lightColor;             
        
            // calculando reflexao difusa
            vec3 norm = normalize(out_normal); // normaliza vetores perpendiculares
            vec3 lightDir = normalize(lightPos - out_fragPos); // direcao da luz
            float diff = max(dot(norm, lightDir), 0.0); // verifica limite angular (entre 0 e 90)
            vec3 diffuse = kd * diff * lightColor; // iluminacao difusa
            
            // calculando reflexao especular
            vec3 viewDir = normalize(viewPos - out_fragPos); // direcao do observador/camera
            vec3 reflectDir = normalize(reflect(-lightDir, norm)); // direcao da reflexao
            float spec = pow(max(dot(viewDir, reflectDir), 0.0), ns);
            vec3 specular = ks * spec * lightColor;             

            if (hasTexture == 1) {
                vec4 texture = texture2D(samplerTexture, out_texture);
                vec4 result = vec4((ambient + diffuse + specular),1.0) * texture; // aplica iluminacao
                gl_FragColor = result;
            } else {
                vec4 result = vec4((ambient + diffuse + specular),1.0) * color; // aplica iluminacao
                gl_FragColor = result;
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
    {
        'name': 'cabinet'
    },
    {
        'name': 'statue'
    },
    {
        'name': 'container'
    },
]

added_objects = {}

initial_states = json.load(open('initialStates.json'))

for obj in objects:

    name = obj['name']

    obj_file = f'3dModels/{name}/{name}.obj'
    texture_file = f'3dModels/{name}/{name}.jpg'
    initital_state = initial_states[name] if name in initial_states else None

    if 'customClass' in obj:
        added_objects[name] = obj['customClass'](obj_file, texture_file, initital_state)
    else:
        added_objects[name] = Object(obj_file, texture_file, initital_state)

    
    scene.add_object(added_objects[name])

scene.start_program()

scene.run()