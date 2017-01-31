import ecs
import components as comp
import constants as cst

from sfml import sf

class Factory:

    def __init__(self, entityManager):
        self.em = entityManager

    def createDefaultFighter(self):
        fighter = self.em.createEntity()
        fighter.addComponent(comp.Position(96,96))
        fighter.addComponent(comp.Fighter(0, 64, 1))
        fighter.addComponent(comp.Armor(0.5, 0))
        fighter.addComponent(comp.Weapon(30, 1, 100))
        fighter.addComponent(comp.Vulnerable(100, 100, cst.BarVisibility.VISIBLE))
        fighter.addComponent(comp.DrawableFighter(sf.RectangleShape((cst.TILE_SIZE, cst.TILE_SIZE))))
        fighter.addComponent(comp.DrawableHUD(None))
        return fighter




