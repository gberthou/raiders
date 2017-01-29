import ecs
import components as comp
import constants as cst

# Basic transformations

def world2grid(pos):
    x, y = pos
    return x // cst.TILE_SIZE, y // cst.TILE_SIZE

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
    return xdiff**2 + ydiff**2 <= friend.component(comp.Weapon).atkRange**2



