import ecs
import components
import systems
import factory
import constants as cst

from sfml import sf

def fighterAt(entityManager, x, y):
    entities = entityManager.getEntitiesWithComponents([components.Position, components.Fighter])
    for e in entities:
        pos = e.component(components.Position)
        print(pos.x, pos.y, x, y)
        if x >= pos.x and x < pos.x + cst.TILE_SIZE and y >= pos.y and y < pos.y + cst.TILE_SIZE:
            return e
    return None

if __name__ == "__main__":
    window = sf.RenderWindow(sf.VideoMode(cst.WINDOW_WIDTH, cst.WINDOW_HEIGHT), "Raiders")
    window.vertical_synchronization = True
    window.framerate_limit = 60

    entityManager = ecs.EntityManager()
    eventManager  = ecs.EventManager()
    app = ecs.ECSApp(entityManager, eventManager)

    app.addSystem(systems.DrawFighter(window))

    facto = factory.Factory(entityManager)
    pelo = facto.createDefaultFighter()

    clock = sf.Clock()

    while window.is_open:
        for event in window.events:
            if type(event) is sf.CloseEvent:
                window.close()
            elif type(event) is sf.MouseButtonEvent:
                if event.button == sf.Mouse.LEFT:
                    fighter = fighterAt(entityManager, event.position.x, event.position.y)
                    print(fighter)

        dt = clock.elapsed_time.seconds
        clock.restart()

        window.clear(sf.Color(0, 255, 0))
        app.updateAll(dt)
        window.display()

