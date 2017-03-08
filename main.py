#! /usr/bin/env python3
import sys
import ecs
import components as comp
import systems
import factory
import constants as cst
import raidersem
import timeMachine
import obstacles
import assets
import resources
import utils

from sfml import sf

def pauseNextState(pause, ev):
    if ((pause & 1) and not ev) or (ev and not (pause & 1)):
        return (pause+1)%4
    return pause

def isPaused(pause):
    return pause == 1 or pause == 2

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

    facto = factory.Factory(em)
    game_map = facto.createDefaultMap("assets/map1.json")
    mapObstacles = obstacles.Obstacles(game_map.component(comp.DrawableMap).surface)

    pelo = facto.createDefaultFighter()
    pelo.addComponent(comp.Leader())

    copain = facto.createDefaultFighter()
    copain.component(comp.Position).y = 352
    copain.component(comp.Fighter).name = "Jeannot"

    foe = facto.createDefaultFighter()
    foe.component(comp.Position).x = 320
    foe.component(comp.Fighter).team = 28

    sDF         = systems.DrawFighter(textureWorld, mapObstacles)
    sDF.team    = 0
    sDHB        = systems.DrawHealthBar(textureHUD, viewWorld, mapObstacles)
    sDHB.team   = 0
    sDTHUD      = systems.DrawTeamHUD(textureHUD, rs)
    sDTHUD.team = 0

    app.addSystem(systems.DrawMap(textureWorld, mapObstacles))
    app.addSystem(sDF)
    app.addSystem(sDHB)
    app.addSystem(systems.DrawWeaponRange(textureHUD, viewWorld))
    app.addSystem(sDTHUD)
    app.addSystem(systems.DrawFPS(textureHUD, rs))
    app.addSystem(systems.MovementAI(mapObstacles))
    app.addSystem(systems.PlayerAttack())

    clock = sf.Clock()
    tm = timeMachine.TimeMachine()

    dx, dy = 0, 0
    zoom = 1
    pause = 0

    oldVisibleEnnemies = set()

    while window.is_open:
        for event in window.events:
            if event.type == sf.Event.CLOSED:
                window.close()
            elif event.type == sf.Event.MOUSE_BUTTON_PRESSED:
                if event["button"] == sf.Mouse.LEFT:
                    x, y = textureWorld.map_pixel_to_coords((event["x"], event["y"]))
                    # First, check if door
                    door = mapObstacles.doorAt(x, y)
                    if  (door != None
                    and (em.hasAllyAtTile(door.edge[0][0], door.edge[0][1], 0)
                    or   em.hasAllyAtTile(door.edge[1][0], door.edge[1][1], 0))):
                        door.active = not door.active
                        continue

                    # If not door, check if fighter
                    fighter = em.fighterAt(x, y)
                    if fighter != None:
                        em.selectFighter(fighter)
                    else: # No fighter underneath mouse cursor
                        em.unselectFighters()
                elif event["button"] == sf.Mouse.RIGHT:
                    x, y = textureWorld.map_pixel_to_coords((event["x"], event["y"]))
                    em.assignTargetToSelected(x, y, mapObstacles)
            elif event.type == sf.Event.MOUSE_WHEEL_SCROLLED:
                zoom -= event["delta"] * cst.MOUSE_ZOOM
                if zoom < cst.MIN_ZOOM:
                    zoom = cst.MIN_ZOOM
                viewWorld.size = (zoom * cst.WINDOW_WIDTH, zoom * cst.WINDOW_HEIGHT)

        pause = pauseNextState(pause, utils.pauseKeyPressed())

        # Scrolling Keyboard
        if utils.anyMovementKeyPressed():
            dx, dy = utils.updateScrollDiff(dx, dy, dt)
            utils.scrollViewKeys(viewWorld, dx, dy)
        else:
            dx, dy = 0, 0
        # Scrolling Mouse
        utils.scrollViewMouse(viewWorld, sf.Mouse.get_position(window).x, sf.Mouse.get_position(window).y)

        if isPaused(pause):
            dt = 0
        else:
            dt = clock.elapsed_time.seconds
            visibleEnnemies = em.visibleEnnemies(0, mapObstacles)
            if visibleEnnemies - oldVisibleEnnemies: # New ennemies spotted
                pause = 1
                dt = 0
            oldVisibleEnnemies = visibleEnnemies

        clock.restart()

        window.clear()
        textureWorld.clear(sf.Color(0,0,0,0))
        textureHUD.clear(sf.Color(0,0,0,0))

        states = sf.RenderStates()
        states.shader = rs.fovShader.shader

        # TODO: Update only display related systems when paused
        app.updateAll(dt)
        tm.update(dt)

        textureWorld.display()
        textureHUD.display()

        rs.fovShader.update(em, 0, tm, mapObstacles, textureWorld)

        window.draw(sf.Sprite(textureWorld.texture), states)
        window.draw(sf.Sprite(textureHUD.texture))

        if isPaused(pause):
            text = sf.Text()
            text.font = rs.font
            text.character_size = 30
            text.color = sf.Color(128, 128, 128)
            text.string = "PAUSED - Press P to resume"
            text.origin = (text.global_bounds.width/2, text.global_bounds.height/2)
            text.position = (cst.WINDOW_WIDTH/2, cst.WINDOW_HEIGHT/2)
            window.draw(text)

        window.display()

