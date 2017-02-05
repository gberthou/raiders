from sfml import sf
import shader

class Resources:
    def __init__(self):
        self.font = sf.Font.from_file("resources/arial.ttf")
        self.fovShader = shader.FieldOfViewShader("resources/shader.frag")

