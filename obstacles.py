import copy
import utils
import assets
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
