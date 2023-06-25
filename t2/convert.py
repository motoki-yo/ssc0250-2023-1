import sys

def convert_quads_to_triangles(input_file: str, output_file: str):
    with open(input_file, 'r') as f_in:
        with open(output_file, 'w') as f_out:
            for line in f_in:
                if line.startswith('f'):
                    vertices = line.split()[1:]
                    if len(vertices) == 4:
                        f_out.write(f'f {vertices[0]} {vertices[1]} {vertices[2]}\n')
                        f_out.write(f'f {vertices[0]} {vertices[2]} {vertices[3]}\n')
                    else:
                        f_out.write(line)
                else:
                    f_out.write(line)


fileName = sys.argv[1]

convert_quads_to_triangles(fileName, fileName.replace('.obj', '_triangles.obj'))

print(f'Converted {fileName} to {fileName.replace(".obj", "_triangles.obj")}')