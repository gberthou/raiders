import components as comp
import constants as cst
import ecs
import utils

class RaidersEntityManager(ecs.EntityManager):

    def fighterAt(self, x, y):
        fighterEntities = self.getEntitiesWithComponents([comp.Position, comp.Fighter])
        for e in fighterEntities:
            pos = e.component(comp.Position)
            if x >= pos.x and x < pos.x + cst.TILE_SIZE and y >= pos.y and y < pos.y + cst.TILE_SIZE:
                return e
        return None

    def hasAllyAtTile(self, tileX, tileY, team):
        e = self.fighterAt(tileX * cst.TILE_SIZE, tileY * cst.TILE_SIZE)
        return e != None and e.component(comp.Fighter).team == team

    def unselectFighters(self):
        for e in self.entities:
            e.removeComponent(comp.Selected)

    def selectFighter(self, fighter):
        self.unselectFighters()
        fighter.addComponent(comp.Selected())

    def assignTargetToSelected(self, x, y, mapObstacles, mapData):
        foe = self.fighterAt(x, y)

        tileX = int(x // cst.TILE_SIZE)
        tileY = int(y // cst.TILE_SIZE)

        selected = self.getEntitiesWithComponents([comp.Selected])
        if selected:
            selected = selected[0]
            if foe == None or not utils.oneCanSee([selected], foe, mapObstacles):
                selected.removeComponent(comp.AttackTarget)
                if not selected.hasComponent(comp.MovementTarget) or selected.component(comp.MovementTarget).target != (tileX, tileY) and utils.pathToTile(selected, (tileX, tileY), mapObstacles, mapData):
                    selected.removeComponent(comp.Path)
                    selected.addComponent(comp.MovementTarget((tileX, tileY)))
            elif utils.areFoes(selected, foe):
                if not selected.hasComponent(comp.AttackTarget) or selected.component(comp.AttackTarget).target != foe:
                    # Here we know that the foe is reachable
                    selected.addComponent(comp.AttackTarget(foe, 1/selected.component(comp.Weapon).atkSpeed))

            # else <Friendly unit at (x,y)> : do nothing

    def teamMembers(self, team):
        return  [e for e
                in self.getEntitiesWithComponents([comp.Fighter])
                if e.component(comp.Fighter).team == team
                ]

    def visibleEnnemies(self, team, mapObstacles):
        allies = self.teamMembers(team)
        return set(e for e in self.getEntitiesWithComponents([comp.Fighter])
                   if utils.areTeamsHostile(team, e.component(comp.Fighter).team) and utils.oneCanSee(allies, e, mapObstacles))
