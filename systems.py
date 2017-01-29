import ecs
import raidersem
import components as comp
import constants as cst
import dijkstra
import utils

from sfml import sf

### Graphics ###

class DrawFighter(ecs.System):
    def __init__(self, window):
        self.window = window

    def update(self, em, eventManager, dt):
        for e in em.getEntitiesWithComponents([comp.DrawableFighter, comp.Position, comp.Fighter]):
            pos = e.component(comp.Position)
            rect = e.component(comp.DrawableFighter).surface
            rect.position = (pos.x, pos.y)
            self.window.draw(rect)

class DrawHealthBar(ecs.System):
    def __init__(self, window):
        self.window = window

    def update(self, em, eventManager, dt):
        for e in em.getEntitiesWithComponents([comp.DrawableHUD, comp.Position, comp.Vulnerable]):
            if e.component(comp.Vulnerable).visibility == cst.BarVisibility.HIDDEN:
                continue

            # TODO: can divide by 0, handle with care
            hpratio = e.component(comp.Vulnerable).currenthp / e.component(comp.Vulnerable).hpmax
            if e.component(comp.Vulnerable).visibility == cst.BarVisibility.DAMAGED and hpratio == 1:
                continue

            # Draw hp bar
            x, y = e.component(comp.Position).x, e.component(comp.Position).y
            bar_position = (x + cst.BAR_X, y + cst.TILE_SIZE + cst.BAR_Y)

            redbar = sf.RectangleShape()
            redbar.position = bar_position
            redbar.size = (cst.BAR_WIDTH, cst.BAR_HEIGHT)
            redbar.fill_color = sf.Color.RED
            redbar.outline_thickness = 1
            redbar.outline_color = sf.Color.BLACK

            self.window.draw(redbar)

            if hpratio != 0:
                greenbar = sf.RectangleShape()
                greenbar.position = bar_position
                greenbar.size = (int(hpratio * cst.BAR_WIDTH), cst.BAR_HEIGHT)
                greenbar.fill_color = sf.Color.GREEN

                self.window.draw(greenbar)

class DrawWeaponRange(ecs.System):
    def __init__(self, window):
        self.window = window

    def update(self, em, eventManager, dt):
        for e in em.getEntitiesWithComponents([comp.DrawableHUD, comp.Position, comp.Fighter, comp.Weapon, comp.Selected]):
            pos = e.component(comp.Position)
            rangeCircle = sf.CircleShape()
            rangeCircle.radius = e.component(comp.Weapon).atkRange
            rangeCircle.position = (pos.x + 0.5*cst.TILE_SIZE - rangeCircle.radius, pos.y + 0.5*cst.TILE_SIZE - rangeCircle.radius)
            rangeCircle.fill_color = sf.Color.TRANSPARENT
            rangeCircle.outline_thickness = 1
            rangeCircle.outline_color = sf.Color(0, 0, 0, 128)

            self.window.draw(rangeCircle)

### Core ###

class Teleportation(ecs.System):
    def __init__(self):
            pass

    def update(self, em, eventManager, dt):
        for e in em.getEntitiesWithComponents([comp.Position, comp.MovementTarget]):
            pos = e.component(comp.Position)
            targetTile = e.component(comp.MovementTarget).target

            pos.x, pos.y = targetTile[0] * cst.TILE_SIZE, targetTile[1] * cst.TILE_SIZE

            e.removeComponent(comp.MovementTarget)
            e.removeComponent(comp.Selected)

class MovementAI(ecs.System):
    def __init__(self):
            pass

    def update(self, em, eventManager, dt):
        for e in em.getEntitiesWithComponents([comp.Position, comp.MovementTarget, comp.Fighter]):
            pos = e.component(comp.Position)
            targetTile = e.component(comp.MovementTarget).target
            currentTile = utils.world2grid((pos.x, pos.y))

            #if targetTile == currentTile:
            if utils.norm2(utils.vec2((pos.x, pos.y), utils.grid2world(targetTile))) < 1:
                e.removeComponent(comp.MovementTarget)
                e.removeComponent(comp.Path)
            else:
                if not e.hasComponent(comp.Path):
                    area = (pos.x - 30, pos.y - 30, pos.x + 30, pos.y + 30)
                    p = dijkstra.searchPath(area, currentTile, targetTile)
                    if p == None: # No path found
                        e.removeComponent(comp.MovementTarget)
                        e.removeComponent(comp.Selected)
                        continue
                    e.addComponent(comp.Path(p, 0))

                path = e.component(comp.Path)
                fighter = e.component(comp.Fighter)

                delta = utils.vec2((pos.x, pos.y), utils.grid2world(path.path[path.currentIndex]))
                if utils.norm2(delta) < 1:
                    path.currentIndex += 1

                length = utils.norm(delta)
                if length > fighter.movSpeed * dt:
                    movement = (delta[0] * fighter.movSpeed * dt / length, delta[1] * fighter.movSpeed * dt / length)
                else:
                    movement = (delta[0], delta[1])

                pos.x += movement[0]
                pos.y += movement[1]

            e.removeComponent(comp.Selected)

class PlayerAttack(ecs.System):
    def __init__(self):
        pass

    def update(self, em, eventManager, dt):
        for e in em.getEntitiesWithComponents([comp.Fighter, comp.Weapon, comp.AttackTarget]):
            target = e.component(comp.AttackTarget)
            foe = target.target

            if not utils.inWeaponRange(e, foe) or foe.component(comp.Vulnerable).currenthp == 0:
                e.removeComponent(comp.AttackTarget)
                return

            atkSpeed = e.component(comp.Weapon).atkSpeed

            nHits = int(target.dt * atkSpeed)

            effectiveDmg = nHits * utils.effectiveDmg(e, foe)
            diff = foe.component(comp.Vulnerable).currenthp - effectiveDmg
            foe.component(comp.Vulnerable).currenthp = diff if diff > 0 else 0

            target.dt += dt
            target.dt -= nHits / atkSpeed


