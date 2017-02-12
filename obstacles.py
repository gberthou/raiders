import assets

class Obstacles:
    def __init__(self, mapDesc):
        sEdges = []
        for index, x, y in mapDesc["houses"]:
            for edge in assets.houseset[index]:
                sEdges.append(((edge[0][0]+x, edge[0][1]+y),
                               (edge[1][0]+x, edge[1][1]+y)))
        
        self.staticEdges = set(sEdges)
        self.dynamicEdges = {}
        self.nodes = {}
