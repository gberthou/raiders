import components
import constants as cst

class Game:
    def __init__(self, entityManager):
        self.entityManager = entityManager

    def fighterAt(self, x, y):
        entities = self.entityManager.getEntitiesWithComponents([components.Position, components.Fighter])
        for e in entities:
            pos = e.component(components.Position)
            if x >= pos.x and x < pos.x + cst.TILE_SIZE and y >= pos.y and y < pos.y + cst.TILE_SIZE:
                return e
        return None

    def unselectFighters(self):
        entities = self.entityManager.entities
        for e in entities:
            e.removeComponent(components.Selected)

    def selectFighter(self, fighter):
        self.unselectFighters()
        fighter.addComponent(components.Selected())

    @staticmethod
    def areFoes(fighterA, fighterB):
        # TODO: Manage neutral/friendly factions
        return fighterA.component(components.Fighter).team != fighterB.component(components.Fighter).team

    def assignTargetToSelected(self, x, y):
        foe = self.fighterAt(x, y)

        tileX = x // cst.TILE_SIZE
        tileY = y // cst.TILE_SIZE

        selected = self.entityManager.getEntitiesWithComponents([components.Selected])
        if len(selected) > 0:
            selected = selected[0]
            if foe == None:
                selected.addComponent(components.MovementTarget((tileX, tileY)))
            elif self.areFoes(selected, foe):
                selected.addComponent(components.AttackTarget(foe))
            # else <Friendly unit at (x,y)> : do nothing
