import ecs
import components
import constants as cst
from sfml import sf

class DrawFighter(ecs.System):
    def __init__(self, window):
        self.window = window

    def update(self, entityManager, eventManager, dt):
        for e in entityManager.getEntitiesWithComponents([components.DrawableFighter, components.Position, components.Fighter]):
            pos = e.component(components.Position)
            rect = e.component(components.DrawableFighter).surface
            rect.position = (pos.x, pos.y)
            self.window.draw(rect)

class Teleportation(ecs.System):
    def __init__(self):
        pass

    def update(self, entityManager, eventManager, dt):
        for e in entityManager.getEntitiesWithComponents([components.Position, components.MovementTarget]):
            pos = e.component(components.Position)
            targetTile = e.component(components.MovementTarget).target
            
            pos.x, pos.y = targetTile[0] * cst.TILE_SIZE, targetTile[1] * cst.TILE_SIZE

            e.removeComponent(components.MovementTarget)
            e.removeComponent(components.Selected)
