#! /usr/bin/env python3
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

    viewWorld = sf.View()
    viewWorld.center = (cst.WINDOW_WIDTH/2, cst.WINDOW_HEIGHT/2)
    viewWorld.size = (cst.WINDOW_WIDTH, cst.WINDOW_HEIGHT)
    textureWorld.view = viewWorld

    if not sf.Shader.is_available():
        print("No shader, no game :(", file=sys.stderr)
        sys.exit(1)

    rs = resources.Resources()

    em = raidersem.RaidersEntityManager()
    eventManager  = ecs.EventManager()
    app = ecs.ECSApp(em, eventManager)

    sDF         = systems.DrawFighter(textureWorld)
    sDF.team    = 0
    sDHB        = systems.DrawHealthBar(textureHUD, viewWorld)
    sDHB.team   = 0
    sDTHUD      = systems.DrawTeamHUD(textureHUD, rs)
    sDTHUD.team = 0

    app.addSystem(systems.DrawMap(textureWorld))
    app.addSystem(sDF)
    app.addSystem(sDHB)
    app.addSystem(systems.DrawWeaponRange(textureHUD, viewWorld))
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

    dx, dy = 0, 0
    zoom = 1

    while window.is_open:
        for event in window.events:
            if event.type == sf.Event.CLOSED:
                window.close()
            elif event.type == sf.Event.MOUSE_BUTTON_PRESSED:
                if event["button"] == sf.Mouse.LEFT:
                    x, y = textureWorld.map_pixel_to_coords((event["x"], event["y"]))
                    fighter = em.fighterAt(x, y)
                    if fighter != None:
                        em.selectFighter(fighter)
                    else: # No fighter underneath mouse cursor
                        em.unselectFighters()
                elif event["button"] == sf.Mouse.RIGHT:
                    x, y = textureWorld.map_pixel_to_coords((event["x"], event["y"]))
                    em.assignTargetToSelected(x, y)
            elif event.type == sf.Event.MOUSE_WHEEL_SCROLLED:
                zoom -= event["delta"] * cst.MOUSE_ZOOM
                if zoom < cst.MIN_ZOOM:
                    zoom = cst.MIN_ZOOM
                viewWorld.size = (zoom * cst.WINDOW_WIDTH, zoom * cst.WINDOW_HEIGHT)

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

        rs.fovShader.update(em, 0, tm, textureWorld)

        window.draw(sf.Sprite(textureWorld.texture), states)
        window.draw(sf.Sprite(textureHUD.texture))

        # Scrolling Keyboard
        if utils.anyMovementKeyPressed():
            dx, dy = utils.updateScrollDiff(dx, dy, dt)
            utils.scrollViewKeys(viewWorld, dx, dy)
        else:
            dx, dy = 0, 0
        # Scrolling Mouse
        utils.scrollViewMouse(viewWorld, sf.Mouse.get_position(window).x, sf.Mouse.get_position(window).y)

        window.display()

