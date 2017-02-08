import sys
import ecs
import components as comp
import systems
import factory
import constants as cst
import raidersem
import timeMachine
import assets
import resources
import utils

from sfml import sf

if __name__ == "__main__":
    window = sf.RenderWindow(sf.VideoMode(cst.WINDOW_WIDTH, cst.WINDOW_HEIGHT), "Raiders")
    window.vertical_synchronization = True
    window.framerate_limit = 60

    view = sf.View()
    view.center = (cst.WINDOW_WIDTH/2, cst.WINDOW_HEIGHT/2)
    view.size = (cst.WINDOW_WIDTH, cst.WINDOW_HEIGHT)
    window.view = view

    textureWorld = sf.RenderTexture(cst.WINDOW_WIDTH, cst.WINDOW_HEIGHT)
    textureHUD   = sf.RenderTexture(cst.WINDOW_WIDTH, cst.WINDOW_HEIGHT)

    if not sf.Shader.is_available():
        print("No shader, no game :(", file=sys.stderr)
        sys.exit(1)

    rs = resources.Resources()

    em = raidersem.RaidersEntityManager()
    eventManager  = ecs.EventManager()
    app = ecs.ECSApp(em, eventManager)

    sDF         = systems.DrawFighter(textureWorld)
    sDF.team    = 0
    sDHB        = systems.DrawHealthBar(textureHUD)
    sDHB.team   = 0
    sDTHUD      = systems.DrawTeamHUD(textureHUD, rs)
    sDTHUD.team = 0

    app.addSystem(systems.DrawMap(textureWorld))
    app.addSystem(sDF)
    app.addSystem(sDHB)
    app.addSystem(systems.DrawWeaponRange(textureHUD))
    app.addSystem(sDTHUD)
    app.addSystem(systems.MovementAI())
    app.addSystem(systems.PlayerAttack())

    facto = factory.Factory(em)
    game_map = facto.createDefaultMap("assets/map.json")

    pelo = facto.createDefaultFighter()
    pelo.addComponent(comp.Leader())

    copain = facto.createDefaultFighter()
    copain.component(comp.Position).y = 352
    copain.component(comp.Fighter).name = "Jeannot"

    foe = facto.createDefaultFighter()
    foe.component(comp.Position).x = 320
    foe.component(comp.Fighter).team = 28
    foe.component(comp.Vulnerable).currenthp = 75

    clock = sf.Clock()
    tm = timeMachine.TimeMachine()

    while window.is_open:
        for event in window.events:
            if type(event) is sf.CloseEvent:
                window.close()
            elif type(event) is sf.MouseButtonEvent:
                if event.button == sf.Mouse.LEFT:
                    x, y = utils.view2world(window.view, event.position)
                    fighter = em.fighterAt(x, y)
                    if fighter != None:
                        em.selectFighter(fighter)
                    else: # No fighter underneath mouse cursor
                        em.unselectFighters()
                elif event.button == sf.Mouse.RIGHT:
                    x, y = utils.view2world(window.view, event.position)
                    em.assignTargetToSelected(x, y)

        dt = clock.elapsed_time.seconds
        clock.restart()

        window.clear()
        textureWorld.clear(sf.Color(0,0,0,0))
        textureHUD.clear(sf.Color(0,0,0,0))


        states = sf.RenderStates()
        states.shader = rs.fovShader.shader

        app.updateAll(dt)
        tm.update(dt)

        textureWorld.display()
        textureHUD.display()

        rs.fovShader.update(em, 0, tm)

        window.draw(sf.Sprite(textureWorld.texture), states)
        window.draw(sf.Sprite(textureHUD.texture))

        utils.moveView(window.view, sf.Mouse.get_position().x, sf.Mouse.get_position().y)

        window.display()

