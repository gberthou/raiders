import ecs
import components
import systems

from sfml import sf

TILE_SIZE = 32

def fighterAt(entityManager, x, y):
    entities = entityManager.getEntitiesWithComponents([components.Position, components.Fighter])
    for e in entities:
        pos = e.component(components.Position)
        print(pos.x, pos.y, x, y)
        if x >= pos.x and x < pos.x + TILE_SIZE and y >= pos.y and y < pos.y + TILE_SIZE:
            return e
    return None

if __name__ == "__main__":
    window = sf.RenderWindow(sf.VideoMode(600, 600), "Raiders")
    window.vertical_synchronization = True
    window.framerate_limit = 60

    entityManager = ecs.EntityManager()
    eventManager  = ecs.EventManager()
    app = ecs.ECSApp(entityManager, eventManager)

    app.addSystem(systems.DrawFighter(window))

    pelo = entityManager.createEntity()
    pelo.addComponent(components.Position(16, 16))
    pelo.addComponent(components.Fighter(0, 0, 0, 0))
    pelo.addComponent(components.DrawableFighter(sf.RectangleShape((TILE_SIZE, TILE_SIZE))))

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

