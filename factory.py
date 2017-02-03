import ecs
import components as comp
import constants as cst

import json

from sfml import sf

class Factory:

    def __init__(self, entityManager):
        self.em = entityManager

    def createDefaultFighter(self):
        fighter = self.em.createEntity()
        fighter.addComponent(comp.Position(96,96))
        fighter.addComponent(comp.Fighter(0, 64, .1))
        fighter.addComponent(comp.Armor(0.5, 0))
        fighter.addComponent(comp.Weapon(30, 1, 100))
        fighter.addComponent(comp.Vulnerable(100, 100, cst.BarVisibility.VISIBLE))

        pos = fighter.component(comp.Position)
        shape = sf.CircleShape()
        shape.radius = 0.4 * cst.TILE_SIZE
        shape.position = (pos.x + 0.5*cst.TILE_SIZE - shape.radius, pos.y + 0.5*cst.TILE_SIZE - shape.radius)
        shape.fill_color = sf.Color.WHITE
        shape.outline_thickness = 0
        fighter.addComponent(comp.DrawableFighter(shape))

        fighter.addComponent(comp.DrawableHUD(None))
        return fighter

    def createDefaultMap(self, path):
        default_map = self.em.createEntity()

        temp_map = None
        # TODO check for valid path & maybe extract this to utils method
        with open(path, "r") as f:
            temp_map = json.loads(f.read())

        default_map.addComponent(comp.DrawableMap(temp_map))
        return default_map


