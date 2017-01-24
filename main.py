import ecs
import components as comp
import systems
import factory
import constants as cst
import game

from sfml import sf

if __name__ == "__main__":
    window = sf.RenderWindow(sf.VideoMode(cst.WINDOW_WIDTH, cst.WINDOW_HEIGHT), "Raiders")
    window.vertical_synchronization = True
    window.framerate_limit = 60

    view = sf.View()
    view.center = (cst.WINDOW_WIDTH/2, cst.WINDOW_HEIGHT/2)
    view.size = (cst.WINDOW_WIDTH, cst.WINDOW_HEIGHT)
    window.view = view

    em = ecs.EntityManager()
    eventManager  = ecs.EventManager()
    app = ecs.ECSApp(em, eventManager)

    game = game.Game(em)

    app.addSystem(systems.DrawFighter(window))
    app.addSystem(systems.DrawHealthBar(window))
    app.addSystem(systems.Teleportation())
    app.addSystem(systems.PlayerAttack())

    facto = factory.Factory(em)
    pelo = facto.createDefaultFighter()

    foe = facto.createDefaultFighter()
    foe.component(comp.Position).x = 300
    foe.component(comp.Fighter).team = 28
    foe.component(comp.Vulnerable).currenthp = 75

    clock = sf.Clock()

    while window.is_open:
        for event in window.events:
            if type(event) is sf.CloseEvent:
                window.close()
            elif type(event) is sf.MouseButtonEvent:
                if event.button == sf.Mouse.LEFT:
                    fighter = game.fighterAt(event.position.x, event.position.y)
                    if fighter != None:
                        game.selectFighter(fighter)
                    else: # No fighter underneath mouse cursor
                        game.unselectFighters()
                elif event.button == sf.Mouse.RIGHT:
                    game.assignTargetToSelected(event.position.x, event.position.y)

        dt = clock.elapsed_time.seconds
        clock.restart()

        window.clear(sf.Color(0, 255, 0))
        app.updateAll(dt)
        window.display()

