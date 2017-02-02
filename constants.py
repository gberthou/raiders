from enum import Enum

BarVisibility = Enum("BarVisibility", "VISIBLE DAMAGED HIDDEN")
TileType = Enum("TileType", [
    ("PLAIN", 1),
    ("FOREST", 2),
    ("MOUNTAIN", 3),
    ("WATER", 4),
    ("ROAD", 5)
    ])

TILE_SIZE = 32
WINDOW_WIDTH = 640 #20*32
WINDOW_HEIGHT = 640

# Health bars
BAR_WIDTH   = int(0.8*TILE_SIZE)
BAR_HEIGHT  = int(0.2*TILE_SIZE)
BAR_X       = int(0.1*TILE_SIZE)
BAR_Y       = int(0.1*TILE_SIZE)




