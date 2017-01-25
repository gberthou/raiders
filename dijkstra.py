# All coordinates are in tile space

def neighborsOf(pos):
    x, y = pos
    return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

class RectangleSet:
    def __init__(self, area):
        self.x0, self.y0, self.x1, self.y1 = area
        self.w = self.x1 - self.x0 + 1
        self.h = self.y1 - self.y0 + 1
        elementCount = self.w * self.h
        self.Q = [True] * elementCount
        self.dist = [-1] * elementCount

    def index(self, pos):
        x, y = pos
        return (y - self.y0) * self.w + (x - self.x0)

    def coord(self, i):
        return i % self.w, i // self.w

    def setDist(self, pos, value):
        self.dist[self.index(pos)] = value
    
    def minDistActive(self):
        tmp = min([(d,i) for i, d in enumerate(self.dist) if d != -1 and self.Q[i]])
        return tmp[0], self.coord(tmp[1])

    def remove(self, pos):
        self.Q[self.index(pos)] = False

    def isActive(self, pos):
        x, y = pos
        if x < 0 or x >= self.w or y < 0 or y >= self.h:
            return False
        return self.Q[self.index(pos)]

    def isShorterThan(self, pos, d):
        ref = self.dist[self.index(pos)]
        return ref == -1 or d < ref
        
    def findPath(self):
        prev = dict()

        while len(self.Q):
            d, minDistPoint = self.minDistActive()
            self.remove(minDistPoint)

            for neighbor in neighborsOf(minDistPoint):
                if not self.isActive(neighbor):
                    continue
                alt = d + 1
                if self.isShorterThan(neighbor, alt):
                    self.setDist(neighbor, alt)
                    prev[neighbor] = minDistPoint
        return prev

def distance(p0, p1):
    return abs(p0[0]-p1[0]) + abs(p0[1]-p1[1])

# x1 > x0
# y1 > y0
def dijkstra(area, start, goal):
    x0, y0, x1, y1 = area
    startX, startY = start
    goalX, goalY   = goal
    dist = {(startX, startY) : 0}
    Q = {(x,y) for x in range(x0, x1+1) for y in range(y0, y1+1)}
    prev = dict()

    while len(Q):
        _, minDistPoint = min([(dist[i], i) for i in dist.keys() if i in Q])

        if minDistPoint == goal: # Mathematical proof of correctness?
            break

        Q.remove(minDistPoint)

        d = dist[minDistPoint]
        for neighbor in neighborsOf(minDistPoint):
            if not neighbor in Q:
                continue
            alt = d + 1 + distance(neighbor, goal) # A* like
            if not neighbor in dist.keys() or alt < dist[neighbor]:
                dist[neighbor] = alt
                prev[neighbor] = minDistPoint
    return prev

# x1 > x0
# y1 > y0
def dijkstraRectangle(area, start, goal):
    x0, y0, x1, y1 = area
    startX, startY = start
    goalX, goalY   = goal

    rs = RectangleSet(area)

    rs.setDist((startX, startY), 0)
    return rs.findPath()

def searchPath(area, start, goal):
    if start == goal:
        return [start]

    prev = dijkstra(area, start, goal)
    if not goal in prev.keys(): # No path
        return None

    ret = [goal]
    while ret[0] in prev.keys():
        ret = [prev[ret[0]]] + ret
    return ret


### Test here
area  = (0, 0, 100, 100)
start = (10, 10)
goal  = (50, 50)

print(searchPath(area, start, goal))

