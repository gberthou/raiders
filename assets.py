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



