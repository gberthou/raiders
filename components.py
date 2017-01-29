# Generated file: do not edit, use gen_comps.py instead

import ecs

class MovementTarget(ecs.Component):
    def __init__(self, target):
        self.target = target

class AttackTarget(ecs.Component):
    def __init__(self, target, dt):
        self.target = target
        self.dt = dt

class Path(ecs.Component):
    def __init__(self, path, currentIndex):
        self.path = path
        self.currentIndex = currentIndex

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
    def __init__(self, hpmax, currenthp, visibility):
        self.hpmax = hpmax
        self.currenthp = currenthp
        self.visibility = visibility

class Fighter(ecs.Component):
    def __init__(self, team, movSpeed, fov):
        self.team = team
        self.movSpeed = movSpeed
        self.fov = fov

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

class Selected(ecs.Component):
    def __init__(self):
        pass

