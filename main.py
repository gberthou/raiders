import sys
import ecs
import components as comp
import systems
import factory
import constants as cst
import raidersem
import assets

from sfml import sf

if __name__ == "__main__":
    window = sf.RenderWindow(sf.VideoMode(cst.WINDOW_WIDTH, cst.WINDOW_HEIGHT), "Raiders")
    window.vertical_synchronization = True
    window.framerate_limit = 60

    view = sf.View()
    view.center = (cst.WINDOW_WIDTH/2, cst.WINDOW_HEIGHT/2)
    view.size = (cst.WINDOW_WIDTH, cst.WINDOW_HEIGHT)
    window.view = view

    texture = sf.RenderTexture(cst.WINDOW_WIDTH, cst.WINDOW_HEIGHT)
    
    if not sf.Shader.is_available():
        print("No shader, no game :(", file=sys.stderr)
        sys.exit(1)

    shader = sf.Shader.from_file(fragment = "shader.frag")
    shader.set_parameter("current")

    em = raidersem.RaidersEntityManager()
    eventManager  = ecs.EventManager()
    app = ecs.ECSApp(em, eventManager)

    app.addSystem(systems.DrawMap(window))
    app.addSystem(systems.DrawFighter(window))
    app.addSystem(systems.DrawHealthBar(window))
    app.addSystem(systems.DrawWeaponRange(window))
    app.addSystem(systems.MovementAI())
    app.addSystem(systems.PlayerAttack())

    facto = factory.Factory(em)
    game_map = facto.createDefaultMap("assets/map.json")
    pelo = facto.createDefaultFighter()

    foe = facto.createDefaultFighter()
    foe.component(comp.Position).x = 320
    foe.component(comp.Fighter).team = 28
    foe.component(comp.Vulnerable).currenthp = 75

    clock = sf.Clock()

    while window.is_open:
        for event in window.events:
            if type(event) is sf.CloseEvent:
                window.close()
            elif type(event) is sf.MouseButtonEvent:
                if event.button == sf.Mouse.LEFT:
                    fighter = em.fighterAt(event.position.x, event.position.y)
                    if fighter != None:
                        em.selectFighter(fighter)
                    else: # No fighter underneath mouse cursor
                        em.unselectFighters()
                elif event.button == sf.Mouse.RIGHT:
                    em.assignTargetToSelected(event.position.x, event.position.y)

        dt = clock.elapsed_time.seconds
        clock.restart()

        window.clear(sf.Color(0, 255, 0))
        
        states = sf.RenderStates()
        states.shader = shader
        # window.draw(sf.Sprite(texture.texture), states)

        app.updateAll(dt)
        window.display()

