import ecs
import components as comp
import constants as cst
import dijkstra
from math import floor, ceil
import json

from sfml import sf

def loadMapJSON(path):
    with open(path, "r") as f:
        return json.load(f)

# Math

def floorTowardsZero(x):
    # if x < 0:
    #     return 1 + floor(x)
    # return floor(x)
    return int(x)

# Basic transformations

def world2grid(pos):
    x, y = pos
    return int(x // cst.TILE_SIZE), int(y // cst.TILE_SIZE)

def grid2world(pos):
    x, y = pos
    return x * cst.TILE_SIZE, y * cst.TILE_SIZE

# Basic vectors

def vec2(a, b):
    x0, y0 = a
    x1, y1 = b
    return x1 - x0, y1 - y0

def norm2(vec):
    x, y = vec
    return (x**2) + (y**2)

def norm(vec):
    return norm2(vec) ** .5

# Combat
def areTeamsHostile(teamA, teamB):
    # TODO: Manage neutral/friendly factions
    return teamA != teamB

def effectiveDmg(friend, foe):
    armor = foe.component(comp.Armor).defense if foe.hasComponent(comp.Armor) else 0
    effectiveDmg = friend.component(comp.Weapon).atk * (1 - armor)
    return effectiveDmg

def areFoes(fighterA, fighterB):
    return areTeamsHostile(fighterA.component(comp.Fighter).team, fighterB.component(comp.Fighter).team)

# Returns whether eA can see eB
def canSee(eA, eB):
    posA = eA.component(comp.Position)
    posB = eB.component(comp.Position)

    d2 = norm2(vec2((posA.x, posA.y), (posB.x, posB.y)))
    return d2 <= (eA.component(comp.Fighter).fov + .5 * cst.TILE_SIZE)**2

# Returns whether at least one among group can see eB
def oneCanSee(group, eB, mapObstacles):
    for i in group:
        if canSee(i, eB) and mapObstacles.isReachable(i, eB):
            return True
    return False

# Pathing & "Physics"

def inWeaponRange(friend, foe):
    # TODO make it more intelligent
    friend_pos = friend.component(comp.Position)
    foe_pos = foe.component(comp.Position)
    xdiff = abs(friend_pos.x - foe_pos.x)
    ydiff = abs(friend_pos.y - foe_pos.y)
    return xdiff**2 + ydiff**2 <= (friend.component(comp.Weapon).atkRange)**2


def closestTileInRange(posWorld, targetWorld, rang):
    p = world2grid(posWorld)
    t = world2grid(targetWorld)

    vector = vec2(t, p)
    length = norm(vector)
    factor = rang / (length * cst.TILE_SIZE)

    delta = (floorTowardsZero(vector[0] * factor), floorTowardsZero(vector[1] * factor))
    return (t[0] + delta[0], t[1] + delta[1])

def pathToTile(entity, targetTile, mapObstacles, mapData):
    pos = entity.component(comp.Position)
    currentTile = world2grid((pos.x, pos.y))
    area = (currentTile[0] - 30, currentTile[1] - 30, currentTile[0] + 30, currentTile[1] + 30)
    velocity = lambda x,y : cst.tileVelocity[cst.TileType(mapData["tiles"][x + y * mapData["width"]])]
    return dijkstra.searchPath(area, mapObstacles, currentTile, targetTile, velocity)

# Scrolling

def insideBorder(x, y):
    border_rect = sf.Rect((cst.BORDER_SIZE, cst.BORDER_SIZE), (cst.WINDOW_WIDTH - 2*cst.BORDER_SIZE, cst.WINDOW_HEIGHT - 2*cst.BORDER_SIZE))
    window_rect = sf.Rect((0, 0), (cst.WINDOW_WIDTH, cst.WINDOW_HEIGHT))
    return window_rect.contains((x, y)) and not border_rect.contains((x, y))

def scrollViewMouse(view, xm, ym):
    if not insideBorder(xm, ym):
        return
    # TODO handle mouse acceleration factor
    factor = 0.02
    xm_center = xm - cst.WINDOW_WIDTH / 2
    ym_center = ym - cst.WINDOW_HEIGHT / 2
    view.center = (view.center.x + factor * xm_center , view.center.y + factor * ym_center)

def scrollViewKeys(view, dx, dy):
    # TODO handle keyboard acceleration factor
    factor = 2
    view.center = (view.center.x + factor * dx , view.center.y + factor * dy)

# Events

def anyMovementKeyPressed():
    movementKeys = [sf.Keyboard.DOWN, sf.Keyboard.UP, sf.Keyboard.LEFT, sf.Keyboard.RIGHT]
    return any([sf.Keyboard.is_key_pressed(key) for key in movementKeys])

def pauseKeyPressed():
    return sf.Keyboard.is_key_pressed(sf.Keyboard.P)

def mapKeyPressed():
    return sf.Keyboard.is_key_pressed(sf.Keyboard.M)

def updateScrollDiff(dx, dy, dt):
    diff = 8 * dt
    if sf.Keyboard.is_key_pressed(sf.Keyboard.DOWN):
        if dy < 0:
            dy = 0
        dy += diff
    if sf.Keyboard.is_key_pressed(sf.Keyboard.UP):
        if dy > 0:
            dy = 0
        dy -= diff
    if sf.Keyboard.is_key_pressed(sf.Keyboard.LEFT):
        if dx > 0:
            dx = 0
        dx -= diff
    if sf.Keyboard.is_key_pressed(sf.Keyboard.RIGHT):
        if dx < 0:
            dx = 0
        dx += diff

    if abs(dx) > 10:
        dx = dx * 10 / abs(dx)
    if abs(dy) > 10:
        dy = dy * 10 / abs(dy)
    return dx, dy

# Wall
def isHorizontal(wall):
    # Assumptions: all walls are either horizontal or vertical, not both
    #              distance(wall.edge[0], wall.edge[1]) == 1
    return wall.edge[0][0] != wall.edge[1][0]

# a = (xWorldA, yWorldA)
# b = (xWorldB, yWorldB)
# a and b are segment ends
def edgesInSegment(a, b):
    def computeN(x, dx):
        n = x / cst.TILE_SIZE
        if dx > 0:
            n = ceil(n)
        else:
            n = floor(n)
        return n

    xA, yA = a
    xB, yB = b

    dx = xB - xA
    dy = yB - yA

    ret = []

    # Vertical edges
    if dx != 0:
        n0 = computeN(xA, dx)
        n1 = computeN(xB, -dx)

        for x in range(min(n0,n1), max(n0,n1)+1):
            k = (x * cst.TILE_SIZE - xA) / dx
            if k < 0 or k > 1:
                continue
            # Align y on grid
            y = int((yA + k * dy) // cst.TILE_SIZE)
            ret.append(((x-1, y), (x, y)))
    elif xA / cst.TILE_SIZE == floor(xA / cst.TILE_SIZE):
        # TODO?
        pass

    # Horizontal edges
    if dy != 0:
        n0 = computeN(yA, dy)
        n1 = computeN(yB, -dy)

        for y in range(min(n0,n1), max(n0,n1)+1):
            k = (y * cst.TILE_SIZE - yA) / dy
            if k < 0 or k > 1:
                continue
            # Align x on grid
            x = int((xA + k * dx) // cst.TILE_SIZE)
            ret.append(((x, y-1), (x, y)))
    elif yA / cst.TILE_SIZE== floor(yA / cst.TILE_SIZE):
        # TODO?
        pass

    return ret

# User input
class ToggleButton:
    def __init__(self):
        self.state = 0

    def nextState(self, ev):
        if (self.state & 1) ^ ev:
            self.state = (self.state+1)%4

    def isActivated(self):
        return self.state == 1 or self.state == 2
