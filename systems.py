import ecs
import components as comp
import constants as cst
import game

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
        for e in em.getEntitiesWithComponents([comp.Fighter, comp.Selected, comp.Weapon, comp.AttackTarget]):
            # TODO in a support method:
            # if not in range > warn player
            # if no weapon > warn player
            # if ally > warn player
            foe = e.component(comp.AttackTarget).target
            effectiveDmg = self.effectiveDmg(e, foe)
            diff = foe.component(comp.Vulnerable).currenthp - effectiveDmg
            foe.component(comp.Vulnerable).currenthp = diff if diff > 0 else 0
            # TODO: Properly handle attack speed
            print("%d" % foe.component(comp.Vulnerable).currenthp)

            # TODO: Don't forget to remove AttackTarget once another valid order has been issued
            e.removeComponent(comp.AttackTarget)
            e.removeComponent(comp.Selected)

    # TODO extract in support method
    def effectiveDmg(self, friend, foe):
        armor = foe.component(comp.Armor).defense if foe.hasComponent(comp.Armor) else 0
        effectiveDmg = friend.component(comp.Weapon).atk * (1 - armor)
        return effectiveDmg

# TODO: Another attack for NPCs ? = non selected

