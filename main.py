import ecs
import components
import systems

from sfml import sf

if __name__ == "__main__":
    window = sf.RenderWindow(sf.VideoMode(800, 800), "Raiders")
    window.vertical_synchronization = True

    entityManager = ecs.EntityManager()
    eventManager  = ecs.EventManager()
    app = ecs.ECSApp(entityManager, eventManager)

    app.addSystem(systems.DrawFighter(window))

    pelo = entityManager.createEntity()
    pelo.addComponent(components.Position(100, 100))
    pelo.addComponent(components.Fighter(0, 0, 0, 0))
    pelo.addComponent(components.DrawableFighter(0))

    while window.is_open:
        for event in window.events:
            if type(event) is sf.CloseEvent:
                window.close()

        window.clear(sf.Color(0, 255, 0))
        app.updateAll(0)
        window.display()

