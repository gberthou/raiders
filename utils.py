import ecs
import components as comp
import constants as cst
from math import floor

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

def effectiveDmg(friend, foe):
    armor = foe.component(comp.Armor).defense if foe.hasComponent(comp.Armor) else 0
    effectiveDmg = friend.component(comp.Weapon).atk * (1 - armor)
    return effectiveDmg

def areFoes(fighterA, fighterB):
    # TODO: Manage neutral/friendly factions
    return fighterA.component(comp.Fighter).team != fighterB.component(comp.Fighter).team



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




