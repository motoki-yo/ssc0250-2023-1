# openGLSeaView

Simple OpenGL program that displays a sea view with interactive elements.
Made using OpenGL, GLFW and Python.

Implementation made for the discipline of Computer Graphics - SSC0250 at ICMC - USP

## Students:

- Eduardo Rodrigues Amaral - 11735021
- Felipe Cadavez - 11208558
- Jefferson Bueno - 11275255
- Melissa Motoki - 5588687

## Specifications:

- Python Interpreter: Python 3.10.8
- pipenv Version: 2023.3.20
- numpy Version: 1.24.2
- glfw Version: 2.5.9
- pyopengl Version: 3.1.6

## Instructions:

- Install `pipenv` in order to run the program environment:
  ```
  pip install pipenv
  ```
- To run the program run the following command (the program may install the required packages before running):

  ```
  pipenv run python3 main.py
  ```

  or

  ```
  ./run
  ```

## Program Controls:

- `<-, ->`
  - Rotates Sun and Moon
- `W, A, S, D`
  - Moves Fish (W = Up, A = Left, S = Down, D = Right)
- `Z, X`
  - Scales Fish (Z = Smaller, X = Bigger)
- `I, J, K, L`
  - Moves Ship (I = Up, J = Left, K = Down, L = Right)
