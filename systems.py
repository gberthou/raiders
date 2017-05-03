import ecs
import raidersem
import components as comp
import constants as cst
import utils
import assets
import math

from sfml import sf

### Graphics ###

class DrawMap(ecs.System):
    def __init__(self, window, mapObstacles, rs):
        self.window = window
        self.mapObstacles = mapObstacles
        self.rs = rs

    def update(self, em, eventManager, dt):
        drawableMap = em.getEntitiesWithComponents([comp.DrawableMap])[0].component(comp.DrawableMap)

        tilemap = drawableMap.tilemap
        width  = tilemap["width"]
        height = tilemap["height"]

        tile = sf.RectangleShape()
        vlx, vly = self.window.map_pixel_to_coords((0, 0))
        vhx, vhy = self.window.map_pixel_to_coords((cst.WINDOW_WIDTH, cst.WINDOW_HEIGHT))
    
        states = sf.RenderStates()
        states.texture = self.rs.tileset.texture

        x0 = math.floor(vlx/cst.TILE_SIZE)
        x1 = math.ceil(vhx/cst.TILE_SIZE)
        y0 = math.floor(vly/cst.TILE_SIZE)
        y1 = math.ceil(vhy/cst.TILE_SIZE)
        for chunk in drawableMap.chunkset.visibleChunks(x0, x1, y0, y1):
            self.window.draw(chunk, states)

        # House debug
        for wall in self.mapObstacles.staticWalls | self.mapObstacles.dynamicWalls:
            if utils.isHorizontal(wall):
                line = sf.RectangleShape((4, cst.TILE_SIZE))
                line.origin = (2, 0)
            else:
                line = sf.RectangleShape((cst.TILE_SIZE, 4))
                line.origin = (0, 2)

            if wall.isdoor:
                if not wall.active:
                    continue
                line.fill_color = sf.Color(255, 0, 255)
            else:
                line.fill_color = sf.Color(255, 255, 0)
            line.position = (wall.edge[1][0] * cst.TILE_SIZE, wall.edge[1][1] * cst.TILE_SIZE)
            self.window.draw(line)

class DrawFighter(ecs.System):
    def __init__(self, window, mapObstacles):
        self.window = window
        self.mapObstacles = mapObstacles
        self.team = -1

    def update(self, em, eventManager, dt):
        allies = em.teamMembers(self.team)

        for e in em.getEntitiesWithComponents([comp.DrawableFighter, comp.Position, comp.Fighter]):
            if e.component(comp.Fighter).team != self.team and not utils.oneCanSee(allies, e, self.mapObstacles):
                continue

            pos = e.component(comp.Position)
            shape = e.component(comp.DrawableFighter).surface
            shape.position = (pos.x + 0.5*cst.TILE_SIZE - shape.radius, pos.y + 0.5*cst.TILE_SIZE - shape.radius)
            if e.component(comp.Fighter).team == self.team:
                shape.fill_color = sf.Color.BLUE
            else:
                shape.fill_color = sf.Color.RED
            self.window.draw(shape)

class DrawHealthBar(ecs.System):
    def __init__(self, window, view, mapObstacles):
        self.window = window
        self.view = view
        self.team = -1
        self.mapObstacles = mapObstacles

    def update(self, em, eventManager, dt):
        allies = em.teamMembers(self.team)
        zoom_factor = cst.WINDOW_WIDTH / self.view.size.x

        for e in em.getEntitiesWithComponents([comp.DrawableHUD, comp.Position, comp.Vulnerable]):
            if e.component(comp.Vulnerable).visibility == cst.BarVisibility.HIDDEN:
                continue
            if e.component(comp.Fighter).team != self.team and not utils.oneCanSee(allies, e, self.mapObstacles):
                continue

            # TODO: can divide by 0, handle with care
            hpratio = e.component(comp.Vulnerable).currenthp / e.component(comp.Vulnerable).hpmax
            if e.component(comp.Vulnerable).visibility == cst.BarVisibility.DAMAGED and hpratio == 1:
                continue

            # Draw hp bar
            x, y = e.component(comp.Position).x, e.component(comp.Position).y
            bar_position = self.window.map_coords_to_pixel((x + cst.BAR_X, y + cst.TILE_SIZE + cst.BAR_Y), self.view)

            redbar = sf.RectangleShape()
            redbar.position = bar_position
            redbar.size = (cst.BAR_WIDTH * zoom_factor, cst.BAR_HEIGHT * zoom_factor)
            redbar.fill_color = sf.Color.RED
            redbar.outline_thickness = 1
            redbar.outline_color = sf.Color.BLACK

            self.window.draw(redbar)

            if hpratio != 0:
                greenbar = sf.RectangleShape()
                greenbar.position = bar_position
                greenbar.size = (hpratio * cst.BAR_WIDTH * zoom_factor, cst.BAR_HEIGHT * zoom_factor)
                greenbar.fill_color = sf.Color.GREEN

                self.window.draw(greenbar)

class DrawWeaponRange(ecs.System):
    def __init__(self, window, view):
        self.window = window
        self.view = view

    def update(self, em, eventManager, dt):
        zoom_factor = cst.WINDOW_WIDTH / self.view.size.x

        for e in em.getEntitiesWithComponents([comp.DrawableHUD, comp.Position, comp.Fighter, comp.Weapon, comp.Selected]):
            pos = e.component(comp.Position)
            pos = self.window.map_coords_to_pixel((pos.x + .5 * cst.TILE_SIZE, pos.y + .5 * cst.TILE_SIZE), self.view)
            rangeCircle = sf.CircleShape()
            rangeCircle.radius = e.component(comp.Weapon).atkRange * zoom_factor
            rangeCircle.origin = (rangeCircle.radius, rangeCircle.radius)
            rangeCircle.position = (pos.x, pos.y)
            rangeCircle.fill_color = sf.Color.TRANSPARENT
            rangeCircle.outline_thickness = 1
            rangeCircle.outline_color = sf.Color(0, 0, 0, 128)

            self.window.draw(rangeCircle)

class DrawTeamHUD(ecs.System):
    def __init__(self, window, rs):
        self.window = window
        self.rs = rs
        self.team = -1

    def update(self, em, eventManager, dt):
        allies = em.teamMembers(self.team)

        leaderPortrait = sf.RectangleShape((cst.PORTRAIT_LEADER_SIZE, cst.PORTRAIT_LEADER_SIZE))
        leaderPortrait.origin = (0, cst.PORTRAIT_LEADER_SIZE)
        leaderPortrait.position = (cst.PORTRAIT_X_MARGIN, cst.WINDOW_HEIGHT - cst.PORTRAIT_Y_MARGIN)

        text = sf.Text()
        text.font = self.rs.font
        text.character_size = 30
        text.color = sf.Color(128, 128, 128)

        self.window.draw(leaderPortrait)

        leader = [e for e in allies if e.hasComponent(comp.Leader)]
        if len(leader): # Should be always true
            text.string = leader[0].component(comp.Fighter).name[0]
            text.origin = (text.global_bounds.width / 2, text.global_bounds.height / 2)
            text.position = (leaderPortrait.position.x + cst.PORTRAIT_LEADER_SIZE / 2, leaderPortrait.position.y - cst.PORTRAIT_LEADER_SIZE / 2)
            self.window.draw(text)

            allies.remove(leader[0])

        text.character_size = 16

        for i in range(cst.MAX_TEAM_SIZE - 1):
            emptySlot = (i >= len(allies))
            portrait = sf.RectangleShape((cst.PORTRAIT_NORMAL_SIZE, cst.PORTRAIT_NORMAL_SIZE))
            portrait.origin = (0, cst.PORTRAIT_NORMAL_SIZE)
            portrait.position = (cst.PORTRAIT_X_MARGIN + cst.PORTRAIT_LEADER_SIZE + i * cst.PORTRAIT_NORMAL_SIZE + (i+1) * cst.PORTRAIT_INTER, cst.WINDOW_HEIGHT - cst.PORTRAIT_Y_MARGIN)
            if emptySlot:
                portrait.fill_color = sf.Color(128, 128, 128)

            self.window.draw(portrait)

            if not emptySlot:
                text.string = allies[i].component(comp.Fighter).name[0]
                text.origin = (text.global_bounds.width / 2, text.global_bounds.height / 2)
                text.position = (portrait.position.x + cst.PORTRAIT_NORMAL_SIZE / 2, portrait.position.y - cst.PORTRAIT_NORMAL_SIZE / 2)
                self.window.draw(text)

class DrawFPS(ecs.System):
    def __init__(self, window, rs):
        self.window = window
        self.rs = rs
        self.sum_dt = 0
        self.num_dt = 0
        self.old_fps = "60"

    def update(self, em, eventManager, dt):
        self.sum_dt += dt
        self.num_dt += 1

        fps = sf.Text()
        fps.font = self.rs.font
        fps.character_size = 16
        fps.color = sf.Color.RED

        if self.sum_dt >= 0.5:
            self.old_fps = str(int(self.num_dt/self.sum_dt))
            self.sum_dt, self.num_dt = 0, 0
        fps.string = self.old_fps

        fps.origin = (fps.global_bounds.width, 0)
        fps.position = (cst.WINDOW_WIDTH - cst.HUD_MARGIN, cst.HUD_MARGIN)
        self.window.draw(fps)

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
    def __init__(self, mapObstacles):
        self.mapObstacles = mapObstacles

    def update(self, em, eventManager, dt):
        for e in em.getEntitiesWithComponents([comp.Position, comp.MovementTarget, comp.Fighter]):
            pos = e.component(comp.Position)
            currentTile = utils.world2grid((pos.x, pos.y))
            targetTile = e.component(comp.MovementTarget).target
            targetWorld = utils.grid2world(targetTile)

            if utils.norm2(utils.vec2((pos.x, pos.y), targetWorld)) < 1:
                pos.x, pos.y = targetWorld # Align the actual position along the tile
                e.removeComponent(comp.MovementTarget)
                e.removeComponent(comp.Path)
            else:
                if not e.hasComponent(comp.Path):
                    p = utils.pathToTile(e, targetTile, self.mapObstacles)
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

class PlayerAttack(ecs.System):
    def __init__(self):
        pass

    def update(self, em, eventManager, dt):
        for e in em.getEntitiesWithComponents([comp.Position, comp.Fighter, comp.Weapon, comp.AttackTarget]):
            target = e.component(comp.AttackTarget)
            foe = target.target

            if foe.component(comp.Vulnerable).currenthp <= 0:
                e.removeComponent(comp.AttackTarget)
                continue

            if not utils.inWeaponRange(e, foe):
                pos    = e.component(comp.Position)
                foepos = foe.component(comp.Position)

                currentMoveT = e.component(comp.MovementTarget) if e.hasComponent(comp.MovementTarget) else None

                moveT = utils.closestTileInRange((pos.x, pos.y), (foepos.x, foepos.y), e.component(comp.Weapon).atkRange)

                if currentMoveT == None or currentMoveT.target != moveT:
                    e.removeComponent(comp.Path)
                    e.addComponent(comp.MovementTarget(moveT))
                continue

            atkSpeed = e.component(comp.Weapon).atkSpeed

            nHits = int(target.dt * atkSpeed)

            effectiveDmg = nHits * utils.effectiveDmg(e, foe)
            diff = foe.component(comp.Vulnerable).currenthp - effectiveDmg
            foe.component(comp.Vulnerable).currenthp = diff if diff > 0 else 0

            target.dt += dt
            target.dt -= nHits / atkSpeed


