# openGLFarm3D

Simple OpenGL program that displays a farm scene whith an extern and intern ambient. The extern ambient contains a moon, the sky, a box, a cat that moves in circles, two penguins, a dinosaur a container and a farm house. Inside the farmhouse there is a statue, a bed and a cabinet.
The moon is used as a light source and moves around in circles affecting the lighting of the objects. The sky and the ground are boundaries for the camera movement.

Made using OpenGL, GLFW and Python.

Implementation made for the discipline of Computer Graphics - SSC0250 at ICMC - USP

## Students:

- Eduardo Rodrigues Amaral - 11735021
- Felipe Cadavez - 11208558
- Jefferson Bueno - 11275255
- Melissa Motoki - 5588687

## Specifications:

- Python Interpreter: Python 3.11.3
- pipenv Version: 2023.6.18
- numpy Version: 1.24.3
- glfw Version: 2.5.9
- PyOpenGL Version: 3.1.7
- PyGLM Version: 2.7.0
- screeninfo Version: 0.8.1

## Instructions:

- Install `pipenv` in order to run the program environment:
  ```
  pip install pipenv
  ```
- Install the necessary program dependencies:

  ```
  pipenv install
  ```

  or

  ```
  ./setup
  ```

- To run the program run the following command:

  ```
  pipenv run python3 main.py
  ```

  or

  ```
  ./run
  ```

- To convert a .obj file to a compatible .obj file run the following command:

  ```
  python convert.py <input_file>
  ```

## Program Controls:

- `W, A, S, D`
  - Moves the Camera (View Matrix) (W = Up, A = Left, S = Down, D = Right)
- `Z, X`
  - Changes the Camera Projection Angle (Projection Matrix) (Z = Decrease, X = Increase)
- `P`
  - Enables/Disables Polygon Mode (GL_FILL, GL_LINE)
- `-, =/+`
  - Changes the Mouse Sensitivity (- = Decrease, =/+ = Increase)
