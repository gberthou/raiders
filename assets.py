import copy
import constants as cst

from sfml import sf

# TODO replace this once we have real assets

tileset = {
        cst.TileType.PLAIN      : sf.Color(180, 238, 180, 128),
        cst.TileType.FOREST     : sf.Color(0, 205, 102, 128),
        cst.TileType.MOUNTAIN   : sf.Color(139, 90, 43, 128),
        cst.TileType.WATER      : sf.Color(0, 178, 238, 128),
        cst.TileType.ROAD       : sf.Color(193, 193, 193, 128)
}

class Wall:
    def __init__(self, edge, isdoor = False):
        self.edge    = edge
        self.isdoor  = isdoor
        self.active  = True

    def copyWithOffset(self, x, y):
        ret = copy.copy(self)
        ret.edge = ((ret.edge[0][0]+x, ret.edge[0][1]+y),
                    (ret.edge[1][0]+x, ret.edge[1][1]+y))
        return ret

houseset = [
    # House 0
    #  ___
    # |   |
    # |   |
    # |_H_|
    [
        Wall(((-1,0), (0,0))),
        Wall(((-1,1), (0,1))),
        Wall(((-1,2), (0,2))),
        Wall(((2,0), (3,0))),
        Wall(((2,1), (3,1))),
        Wall(((2,2), (3,2))),
        Wall(((0,-1), (0,0))),
        Wall(((1,-1), (1,0))),
        Wall(((2,-1), (2,0))),
        Wall(((0,2), (0,3))),
        Wall(((2,2), (2,3))),
        Wall(((1,2), (1,3)), True)
    ],

    # House 1
    #  ___
    # |   |
    # |_H_|
    # |   |
    # |   I
    # |___|
    [
        Wall(((-1,0), (0,0))),
        Wall(((-1,1), (0,1))),
        Wall(((-1,2), (0,2))),
        Wall(((-1,3), (0,3))),
        Wall(((-1,4), (0,4))),
        Wall(((2,0), (3,0))),
        Wall(((2,1), (3,1))),
        Wall(((2,2), (3,2))),
        Wall(((2,3), (3,3)), True),
        Wall(((2,4), (3,4))),
        Wall(((0,-1), (0,0))),
        Wall(((1,-1), (1,0))),
        Wall(((2,-1), (2,0))),
        Wall(((0,1), (0,2))),
        Wall(((1,1), (1,2)), True),
        Wall(((2,1), (2,2))),
        Wall(((0,4), (0,5))),
        Wall(((1,4), (1,5))),
        Wall(((2,4), (2,5)))
    ]
]


