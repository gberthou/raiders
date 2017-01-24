from enum import Enum

BarVisibility = Enum("BarVisibility", "VISIBLE DAMAGED HIDDEN")

TILE_SIZE = 32
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

# Health bars
BAR_WIDTH   = int(0.8*TILE_SIZE)
BAR_HEIGHT  = int(0.2*TILE_SIZE)
BAR_X       = int(0.1*TILE_SIZE)
BAR_Y       = int(0.1*TILE_SIZE)




