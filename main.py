import ecs
import components
import systems

from sfml import sf

if __name__ == "__main__":
    TILE_SIZE = 32

    window = sf.RenderWindow(sf.VideoMode(600, 600), "Raiders")
    window.vertical_synchronization = True

    entityManager = ecs.EntityManager()
    eventManager  = ecs.EventManager()
    app = ecs.ECSApp(entityManager, eventManager)

    app.addSystem(systems.DrawFighter(window))

    pelo = entityManager.createEntity()
    pelo.addComponent(components.Position(100, 100))
    pelo.addComponent(components.Fighter(0, 0, 0, 0))
    pelo.addComponent(components.DrawableFighter(sf.RectangleShape((TILE_SIZE, TILE_SIZE))))

    while window.is_open:
        for event in window.events:
            if type(event) is sf.CloseEvent:
                window.close()

        pelo.component(components.Position).x += 1

        window.clear(sf.Color(0, 255, 0))
        app.updateAll(0)
        window.display()

