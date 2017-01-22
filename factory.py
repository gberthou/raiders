import ecs
import components as comps
import constants as cst

from sfml import sf

class Factory:

    def __init__(self, entityManager):
        self._entityManager = entityManager

    def createDefaultFighter(self):
        fighter = self._entityManager.createEntity()
        fighter.addComponent(comps.Position(100, 100))
        fighter.addComponent(comps.Fighter(0, 1, 1))
        fighter.addComponent(comps.Armor(0, 0))
        fighter.addComponent(comps.Weapon(1, 1, 1))
        fighter.addComponent(comps.DrawableFighter(sf.RectangleShape((cst.TILE_SIZE, cst.TILE_SIZE))))
        return fighter




