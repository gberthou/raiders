# All coordinates are in tile space

def neighborsOf(pos):
    cdef int x, y
    x, y = pos
    return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

cdef int distance(p0, p1):
    return abs(p0[0]-p1[0]) + abs(p0[1]-p1[1])

# x1 > x0
# y1 > y0
def dijkstra(area, start, goal):
    cdef int x0, y0, x1, y1, startX, startY, goalX, goalY

    x0, y0, x1, y1 = area
    startX, startY = start
    goalX, goalY   = goal
    dist = {(startX, startY) : 0}
    nQ = set()
    prev = dict()

    cdef int i
    for i in range((x1-x0+1) * (y1-y0+1)):
        d, minDistPoint = min([(j, x) for x, j in dist.items() if not x in nQ])

        if minDistPoint == goal: # Mathematical proof of correctness?
            break

        nQ.add(minDistPoint)
        del dist[minDistPoint]

        for neighbor in neighborsOf(minDistPoint):
            if neighbor in nQ:
                continue
            alt = d + 1 + distance(neighbor, goal) # A* like
            if not neighbor in dist.keys() or alt < dist[neighbor]:
                dist[neighbor] = alt
                prev[neighbor] = minDistPoint
    return prev

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

