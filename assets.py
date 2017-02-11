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

houseset = [
    # House 0
    #  ___
    # |   |
    # |   |
    # |_ _|
    [
        ((-1,0), (0,0)),
        ((-1,1), (0,1)),
        ((-1,2), (0,2)),
        ((2,0), (3,0)),
        ((2,1), (3,1)),
        ((2,2), (3,2)),
        ((0,-1), (0,0)),
        ((1,-1), (1,0)),
        ((2,-1), (2,0)),
        ((0,2), (0,3)),
        ((2,2), (2,3))
    ]
]


