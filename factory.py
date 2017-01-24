import ecs
import components as comp
import constants as cst

from sfml import sf

class Factory:

    def __init__(self, entityManager):
        self.em = entityManager

    def createDefaultFighter(self):
        fighter = self.em.createEntity()
        fighter.addComponent(comp.Position(0, 0))
        fighter.addComponent(comp.Fighter(0, 1, 1))
        fighter.addComponent(comp.Armor(0.5, 0))
        fighter.addComponent(comp.Weapon(30, 1, 1))
        fighter.addComponent(comp.Vulnerable(100, 100))
        fighter.addComponent(comp.DrawableFighter(sf.RectangleShape((cst.TILE_SIZE, cst.TILE_SIZE))))
        # HP bar
        return fighter




