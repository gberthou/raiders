import ecs
import components as comp
import constants as cst
import chunkset

from sfml import sf

class Factory:

    def __init__(self, entityManager):
        self.em = entityManager

    def createDefaultFighter(self):
        fighter = self.em.createEntity()
        fighter.addComponent(comp.Position(96,96))
        fighter.addComponent(comp.Fighter("Marcel", 0, 64, 120))
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

    def createDefaultMap(self, mapData):
        default_map = self.em.createEntity()
        default_map.addComponent(comp.DrawableMap(mapData, chunkset.ChunkSet(mapData)))
        return default_map

