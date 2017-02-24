import copy
import utils
import assets
import components as comp
import constants as cst

class Obstacles:
    def __init__(self, mapDesc):
        sWalls = []
        dWalls = []
        for index, x, y in mapDesc["houses"]:
            for wall in assets.houseset[index]:
                w = wall.copyWithOffset(x, y)
                if w.isdoor:
                    dWalls.append(w)
                else:
                    sWalls.append(w)
        
        self.staticWalls = set(sWalls)
        self.dynamicWalls = set(dWalls)
        self.nodes = {}

    def doorAt(self, x, y):
        for wall in self.dynamicWalls:
            dx = x - wall.edge[1][0] * cst.TILE_SIZE
            dy = y - wall.edge[1][1] * cst.TILE_SIZE
            if utils.isHorizontal(wall): # Swap dx and dy
                tmp = dx
                dx = dy
                dy = tmp

            if (dx >= 0 and dx < cst.TILE_SIZE
            and dy >= -cst.DOOR_THICKNESS and dy < cst.DOOR_THICKNESS):
                return wall
        return None

    def activeEdges(self):
        return (set(w for w in self.staticWalls)
              | set(w for w in self.dynamicWalls if w.active))

    def isReachable(self, selected, foe):
        selectedPos = selected.component(comp.Position)
        foePos      = foe.component(comp.Position)

        edges = utils.edgesInSegment((selectedPos.x + cst.TILE_SIZE/2, selectedPos.y + cst.TILE_SIZE/2),
                                     (foePos.x + cst.TILE_SIZE/2, foePos.y + cst.TILE_SIZE/2))

        return len(set(edges).intersection(self.activeEdges())) == 0


