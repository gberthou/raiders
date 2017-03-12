from sfml import sf
import shader
import constants as cst
import assets

class Resources:
    def __init__(self, mapData):
        self.font = sf.Font.from_file("resources/arial.ttf")
        self.fovShader = shader.FieldOfViewShader("resources/fov.frag")
        self.mapShader = shader.MapShader("resources/map.frag", mapData)

        self.tileset = sf.RenderTexture(len(assets.tileset) * cst.TILE_SIZE, cst.TILE_SIZE)
        rectangle = sf.RectangleShape()
        rectangle.size = (cst.TILE_SIZE, cst.TILE_SIZE)
        for i, tile in enumerate(assets.tileset.keys()):
            rectangle.position = (i * cst.TILE_SIZE, 0)
            rectangle.fill_color = assets.tileset[tile]
            self.tileset.draw(rectangle)
