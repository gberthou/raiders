import assets
import copy

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
