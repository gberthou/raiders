from enum import Enum
from sfml import sf

BarVisibility = Enum("BarVisibility", "VISIBLE DAMAGED HIDDEN")
TileType = Enum("TileType", [
    ("PLAIN", 1),
    ("FOREST", 2),
    ("MOUNTAIN", 3),
    ("WATER", 4),
    ("ROAD", 5),
    ("DEBUG", 6),
    ("INDOORS", 7)
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

# FPS
HUD_MARGIN = 16

# Gameplay
MAX_TEAM_SIZE  = 5
DOOR_THICKNESS = 4

# Daylight
DAY_DURATION = 60 # Seconds
DAY_LUM_MIN  = 0.05
DAY_LUM_MAX  = 0.9
#DAY_A        = -4 * (DAY_LUM_MAX - DAY_LUM_MIN) / (DAY_DURATION ** 2)

# Zoom
MOUSE_ZOOM = 0.5
MIN_ZOOM   = 0.1

# Map
MAP_PALETTE = [sf.Color(64, 64, 255),
               sf.Color(255, 255, 128),
               sf.Color(255, 128, 64),
               sf.Color(0, 255, 64),
               sf.Color(192, 192, 192)]

MAP_WIDTH  = 500
MAP_HEIGHT = 500
