import ecs
import components
from sfml import sf

TILE_SIZE = 32

class DrawFighter(ecs.System):
    def __init__(self, window):
        self.window = window

    def update(self, entityManager, eventManager, dt):
        for e in entityManager.getEntitiesWithComponents([components.DrawableFighter, components.Position, components.Fighter]):
            pos = e.component(components.Position)

            rect = sf.RectangleShape((TILE_SIZE, TILE_SIZE))
            rect.position = (pos.x, pos.y)
            self.window.draw(rect)

