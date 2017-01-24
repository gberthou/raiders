import ecs
import components
import constants as cst
import game

from sfml import sf

class DrawFighter(ecs.System):
    def __init__(self, window):
        self.window = window

    def update(self, entityManager, eventManager, dt):
        for e in entityManager.getEntitiesWithComponents([components.DrawableFighter, components.Position, components.Fighter]):
            pos = e.component(components.Position)
            rect = e.component(components.DrawableFighter).surface
            rect.position = (pos.x, pos.y)
            self.window.draw(rect)

class DrawHealthBar(ecs.System):
    def __init__(self, window):
        self.window = window

    def update(self, entityManager, eventManager, dt):
        for e in entityManager.getEntitiesWithComponents([components.DrawableHUD, components.Position, components.Vulnerable]):
            hpratio = e.component(components.Vulnerable).currenthp / e.component(components.Vulnerable).hpmax
            # TODO: Draw hp bar

class Teleportation(ecs.System):
    def __init__(self):
        pass

    def update(self, entityManager, eventManager, dt):
        for e in entityManager.getEntitiesWithComponents([components.Position, components.MovementTarget]):
            pos = e.component(components.Position)
            targetTile = e.component(components.MovementTarget).target

            pos.x, pos.y = targetTile[0] * cst.TILE_SIZE, targetTile[1] * cst.TILE_SIZE

            e.removeComponent(components.MovementTarget)
            e.removeComponent(components.Selected)

class PlayerAttack(ecs.System):
    def __init__(self):
        pass

    def update(self, entityManager, eventManager, dt):
        for e in entityManager.getEntitiesWithComponents([components.Fighter, components.Selected, components.Weapon, components.AttackTarget]):
            # TODO in a support method:
            # if not in range > warn player
            # if no weapon > warn player
            # if ally > warn player
            foe = e.component(components.AttackTarget).target
            effectiveDmg = self.effectiveDmg(e, foe)
            foe.component(components.Vulnerable).currenthp -= effectiveDmg if effectiveDmg > 0 else 0
            # TODO: Properly handle attack speed
            print("%d" % foe.component(components.Vulnerable).currenthp)

            # TODO: Don't forget to remove AttackTarget once another valid order has been issued
            e.removeComponent(components.AttackTarget)
            e.removeComponent(components.Selected)

    # TODO extract in support method
    def effectiveDmg(self, friend, foe):
        armor = foe.component(components.Armor).defense if foe.hasComponent(components.Armor) else 0
        effectiveDmg = friend.component(components.Weapon).atk * (1 - armor)
        return effectiveDmg

# TODO: Another attack for NPCs ? = non selected

