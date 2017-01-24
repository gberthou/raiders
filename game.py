import components as comp
import constants as cst

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

    @staticmethod
    def areFoes(fighterA, fighterB):
        # TODO: Manage neutral/friendly factions
        return fighterA.component(comp.Fighter).team != fighterB.component(comp.Fighter).team

    def assignTargetToSelected(self, x, y):
        foe = self.fighterAt(x, y)

        tileX = x // cst.TILE_SIZE
        tileY = y // cst.TILE_SIZE

        selected = self.em.getEntitiesWithComponents([comp.Selected])
        if len(selected) > 0:
            selected = selected[0]
            if foe == None:
                selected.addComponent(comp.MovementTarget((tileX, tileY)))
            elif self.areFoes(selected, foe):
                selected.addComponent(comp.AttackTarget(foe))
            # else <Friendly unit at (x,y)> : do nothing
