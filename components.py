# Generated file: do not edit, use gen_comps.py instead

import ecs

class Pathfinding(ecs.Component):
    def __init__(self, target):
        self.target = target

class Weapon(ecs.Component):
    def __init__(self, atk, atkSpeed, atkRange):
        self.atk = atk
        self.atkSpeed = atkSpeed
        self.atkRange = atkRange

class Armor(ecs.Component):
    def __init__(self, defense, slowFactor):
        self.defense = defense
        self.slowFactor = slowFactor

class Vulnerable(ecs.Component):
    def __init__(self, hpmax, currenthp):
        self.hpmax = hpmax
        self.currenthp = currenthp

class Fighter(ecs.Component):
    def __init__(self, team, movSpeed, fov, movRange):
        self.team = team
        self.movSpeed = movSpeed
        self.fov = fov
        self.movRange = movRange

class PhysicalObject(ecs.Component):
    def __init__(self, size):
        self.size = size

class Door(ecs.Component):
    def __init__(self, tile0, tile1, isOpen):
        self.tile0 = tile0
        self.tile1 = tile1
        self.isOpen = isOpen

class DrawableMap(ecs.Component):
    def __init__(self, surface):
        self.surface = surface

class DrawableObject(ecs.Component):
    def __init__(self, surface):
        self.surface = surface

class DrawableFighter(ecs.Component):
    def __init__(self, surface):
        self.surface = surface

class DrawableTop(ecs.Component):
    def __init__(self, surface):
        self.surface = surface

class DrawableHUD(ecs.Component):
    def __init__(self, surface):
        self.surface = surface

class Position(ecs.Component):
    def __init__(self, x, y):
        self.x = x
        self.y = y

