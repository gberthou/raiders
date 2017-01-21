import ecs
import components
import systems

from sfml import sf

if __name__ == "__main__":
    TILE_SIZE = 32

    window = sf.RenderWindow(sf.VideoMode(600, 600), "Raiders")
    window.vertical_synchronization = True
    window.framerate_limit = 60

    entityManager = ecs.EntityManager()
    eventManager  = ecs.EventManager()
    app = ecs.ECSApp(entityManager, eventManager)

    app.addSystem(systems.DrawFighter(window))

    pelo = entityManager.createEntity()
    pelo.addComponent(components.Position(100, 100))
    pelo.addComponent(components.Fighter(0, 0, 0, 0))
    pelo.addComponent(components.DrawableFighter(sf.RectangleShape((TILE_SIZE, TILE_SIZE))))

    clock = sf.Clock()

    while window.is_open:
        for event in window.events:
            if type(event) is sf.CloseEvent:
                window.close()

        dt = clock.elapsed_time.seconds
        clock.restart()

        pelo.component(components.Position).x += 100*dt # 100px/s

        window.clear(sf.Color(0, 255, 0))
        app.updateAll(dt)
        window.display()

