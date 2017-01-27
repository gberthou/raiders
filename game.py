import components as comp
import constants as cst
import utils

class Game:
    def __init__(self, em):
        self.em = em

    def fighterAt(self, x, y):
        entities = self.em.getEntitiesWithComponents([comp.Position, comp.Fighter])
        for e in entities:
            pos = e.component(comp.Position)
            if x >= pos.x and x < pos.x + cst.TILE_SIZE and y >= pos.y and y < pos.y + cst.TILE_SIZE:
                return e
        return None

    def unselectFighters(self):
        entities = self.em.entities
        for e in entities:
            e.removeComponent(comp.Selected)

    def selectFighter(self, fighter):
        self.unselectFighters()
        fighter.addComponent(comp.Selected())

    def assignTargetToSelected(self, x, y):
        foe = self.fighterAt(x, y)

        tileX = x // cst.TILE_SIZE
        tileY = y // cst.TILE_SIZE

        selected = self.em.getEntitiesWithComponents([comp.Selected])
        if len(selected) > 0:
            selected = selected[0]
            if foe == None:
                selected.addComponent(comp.MovementTarget((tileX, tileY)))
            elif utils.areFoes(selected, foe):
                selected.addComponent(comp.AttackTarget(foe, 0))
            # else <Friendly unit at (x,y)> : do nothing


