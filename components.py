# Generated file: do not edit, use gen_comps.py instead

import ecs

def Pathfinding(Component):
    def __init__(target):
        self.target = target

def Weapon(Component):
    def __init__(atk,atk_speed,atk_range):
        self.atk = atk
        self.atk_speed = atk_speed
        self.atk_range = atk_range

def Armor(Component):
    def __init__(defense,slow_factor):
        self.defense = defense
        self.slow_factor = slow_factor

def Vulnerable(Component):
    def __init__(hpmax,currenthp):
        self.hpmax = hpmax
        self.currenthp = currenthp

def Fighter(Component):
    def __init__(team,mov_speed,fov,mov_range):
        self.team = team
        self.mov_speed = mov_speed
        self.fov = fov
        self.mov_range = mov_range

def PhysicalObject(Component):
    def __init__(size):
        self.size = size

def Door(Component):
    def __init__(tile0,tile1,isOpen):
        self.tile0 = tile0
        self.tile1 = tile1
        self.isOpen = isOpen

def DrawableMap(Component):
    def __init__(surface):
        self.surface = surface

def DrawableObject(Component):
    def __init__(surface):
        self.surface = surface

def DrawableFighter(Component):
    def __init__(surface):
        self.surface = surface

def DrawableTop(Component):
    def __init__(surface):
        self.surface = surface

def DrawableHUD(Component):
    def __init__(surface):
        self.surface = surface

def Position(Component):
    def __init__(x,y):
        self.x = x
        self.y = y

