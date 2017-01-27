import ecs
import components as comp
import constants as cst
import game
import utils

from sfml import sf

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


