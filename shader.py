import components as comp
import constants as cst
from sfml import sf

class FieldOfViewShader:
    def __init__(self, filename):
        self.shader = sf.Shader.from_file(fragment = filename)
        self.shader.set_parameter("texture")
        self.shader.set_parameter("aspectRatio", cst.WINDOW_WIDTH / cst.WINDOW_HEIGHT);
        self.shader.set_parameter("baseLuminance", 0.)

        self.reinit()

    def reinit(self):
        for i in range(16):
            self.shader.set_parameter("ranges[%d]" % i, 0)

    def update(self, em, playerTeam, timeMachine, target):
        n = 0
        for e in em.getEntitiesWithComponents([comp.Fighter, comp.Position]):
            fighter = e.component(comp.Fighter) 
            if fighter.team == playerTeam: 
                pos = e.component(comp.Position)
                pos = target.map_coords_to_pixel((pos.x, pos.y))
                self.shader.set_parameter("allies[%d]" % n, ((pos.x+.5*cst.TILE_SIZE)/cst.WINDOW_WIDTH, 1 - (pos.y+.5*cst.TILE_SIZE)/cst.WINDOW_HEIGHT))
                self.shader.set_parameter("ranges[%d]" % n, fighter.fov / cst.WINDOW_WIDTH)
                n += 1

        for i in range(n, 16):
            self.shader.set_parameter("ranges[%d]" % i, 0)

        self.shader.set_parameter("baseLuminance", timeMachine.getLuminance())
