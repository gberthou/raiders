import components as comp
import constants as cst
import utils
from sfml import sf

FOV_SHADER_RANGE_COUNT = 16
FOV_SHADER_EDGE_COUNT  = 256

def isWallVisible(wall, target):
    a = (wall.edge[1][0]*cst.TILE_SIZE, wall.edge[1][1]*cst.TILE_SIZE)
    if utils.isHorizontal(wall):
        b = (a[0], a[1] + cst.TILE_SIZE)
    else:
        b = (a[0] + cst.TILE_SIZE, a[1])

    tmp = [target.map_coords_to_pixel(i) for i in [a, b]]
    tmp = [(i.x / cst.WINDOW_WIDTH, i.y / cst.WINDOW_HEIGHT) for i in tmp]

    # TODO: Change bounds
    # Should be [0,1] +- maxrange/cst.WINDOW_WIDTH
    ret = [i[0] >= -1 and i[0] < 2 and i[1] >= -1 and i[1] < 2 for i in tmp]
    return (ret[0] or ret[1], tmp)

class FieldOfViewShader:
    def __init__(self, filename):
        self.shader = sf.Shader.from_file(fragment = filename)
        self.shader.set_parameter("texture")
        self.shader.set_parameter("aspectRatio", cst.WINDOW_WIDTH / cst.WINDOW_HEIGHT);
        self.shader.set_parameter("baseLuminance", 0.)

        self.reinit()

    def reinit(self):
        for i in range(FOV_SHADER_RANGE_COUNT):
            self.shader.set_parameter("ranges[%d]" % i, 0)

        for i in range(FOV_SHADER_EDGE_COUNT):
            self.shader.set_parameter("edges[%d]" % i, 0, 0, 0, 0)


    def update(self, em, playerTeam, timeMachine, mapObstacles, target):
        nRange = 0

        zoom_factor = cst.WINDOW_WIDTH / target.view.size.x

        # Set fighters ranges
        for e in em.getEntitiesWithComponents([comp.Fighter, comp.Position]):
            fighter = e.component(comp.Fighter) 
            if fighter.team == playerTeam: 
                pos = e.component(comp.Position)
                pos = target.map_coords_to_pixel((pos.x + .5 * cst.TILE_SIZE, pos.y + .5 * cst.TILE_SIZE))
                self.shader.set_parameter("allies[%d]" % nRange, (pos.x / cst.WINDOW_WIDTH, 1 - pos.y / cst.WINDOW_HEIGHT))
                self.shader.set_parameter("ranges[%d]" % nRange, fighter.fov * zoom_factor / cst.WINDOW_WIDTH)
                nRange += 1
        for i in range(nRange, FOV_SHADER_RANGE_COUNT):
            self.shader.set_parameter("ranges[%d]" % i, 0)
        self.shader.set_parameter("baseLuminance", timeMachine.getLuminance())

        # Set map edges
        wallList = mapObstacles.activeEdges()
        visible  = [isWallVisible(w, target) for w in wallList]
        visible  = [j for i,j in visible if i]

        if len(visible) > FOV_SHADER_EDGE_COUNT:
            raise Exception("Unable to allocate that many edges: %d/%d" % (len(visible), FOV_SHADER_EDGE_COUNT))

        edges = [(v[0][0], (1-v[0][1]), v[1][0], (1-v[1][1])) for v in visible]
        for i,j in enumerate(edges):
            self.shader.set_parameter("edges[%d]" % i, j[0], j[1], j[2], j[3])
        for i in range(len(edges), FOV_SHADER_RANGE_COUNT):
            self.shader.set_parameter("edges[%d]" % i, sf.Color(0, 0, 0, 0))

class MapShader:
    def __init__(self, filename, mapData):
        domains = mapData["domains"]
        if len(domains) > 64:
            raise Exception("MapShader: too many domains (%d)" % len(domains))

        if len(cst.MAP_PALETTE) > 8:
            raise Exception("MapShader: too many palette colors (%d)" % len(domains))

        self.shader = sf.Shader.from_file(fragment = filename)

        self.shader.set_parameter("domainCount", len(domains))
        for i, domain in enumerate(domains):
            self.shader.set_parameter("domainPositions[%d]" % i, domain[0] / mapData["width"], 1 - domain[1] / mapData["height"], domain[2])

        for i, color in enumerate(cst.MAP_PALETTE):
            self.shader.set_parameter("palette[%d]" % i, color)

