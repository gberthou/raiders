import sys
import ecs
import components as comp
import systems
import factory
import constants as cst
import raidersem
import assets
import shader

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

    fovShader = shader.FieldOfViewShader("shader.frag")

    em = raidersem.RaidersEntityManager()
    eventManager  = ecs.EventManager()
    app = ecs.ECSApp(em, eventManager)

    app.addSystem(systems.DrawMap(textureWorld))
    app.addSystem(systems.DrawFighter(textureWorld))
    app.addSystem(systems.DrawHealthBar(textureHUD))
    app.addSystem(systems.DrawWeaponRange(textureHUD))
    app.addSystem(systems.MovementAI())
    app.addSystem(systems.PlayerAttack())

    facto = factory.Factory(em)
    game_map = facto.createDefaultMap("assets/map.json")

    pelo = facto.createDefaultFighter()

    copain = facto.createDefaultFighter()
    copain.component(comp.Position).y = 352

    

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

        window.clear()
        textureWorld.clear(sf.Color(0,0,0,0))
        textureHUD.clear(sf.Color(0,0,0,0))
    
        
        states = sf.RenderStates()
        states.shader = fovShader.shader

        app.updateAll(dt)
        textureWorld.display()
        textureHUD.display()
    
        fovShader.update(em, 0)
        
        window.draw(sf.Sprite(textureWorld.texture), states)
        window.draw(sf.Sprite(textureHUD.texture))
        window.display()

