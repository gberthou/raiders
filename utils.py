import ecs
import components as comp
import constants as cst

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



