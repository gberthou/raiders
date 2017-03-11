from sfml import sf
import shader

class Resources:
    def __init__(self, mapData):
        self.font = sf.Font.from_file("resources/arial.ttf")
        self.fovShader = shader.FieldOfViewShader("resources/fov.frag")
        self.mapShader = shader.MapShader("resources/map.frag", mapData)

