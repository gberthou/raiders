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
BORDER_SIZE = 64

# Health bars
BAR_WIDTH   = int(0.8*TILE_SIZE)
BAR_HEIGHT  = int(0.2*TILE_SIZE)
BAR_X       = int(0.1*TILE_SIZE)
BAR_Y       = int(0.1*TILE_SIZE)

# Portraits
PORTRAIT_X_MARGIN    = 16
PORTRAIT_Y_MARGIN    = 16
PORTRAIT_INTER       = 16
PORTRAIT_LEADER_SIZE = 64
PORTRAIT_NORMAL_SIZE = 32

# Gameplay
MAX_TEAM_SIZE = 5

# Daylight
DAY_DURATION = 60 # Seconds
DAY_LUM_MIN  = 0.05
DAY_LUM_MAX  = 0.9
#DAY_A        = -4 * (DAY_LUM_MAX - DAY_LUM_MIN) / (DAY_DURATION ** 2)
