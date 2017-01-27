# All coordinates are in tile space
cimport libc.limits
from libc.stdint cimport uint32_t, int64_t

def neighborsOf(pos):
    cdef int x, y
    x, y = pos
    return ((x+1, y), (x-1, y), (x, y+1), (x, y-1))

cdef unsigned int distance(p0, p1):
    cdef int64_t x0, x1, y0, y1
    x0,y0 = p0
    x1, y1 = p1
    return abs(x0 - x1) + abs(y0 - y1)

# x1 > x0
# y1 > y0
def dijkstra(area, start, goal):
    cdef int x0, y0, x1, y1, startX, startY, goalX, goalY

    x0, y0, x1, y1 = area
    startX, startY = start
    goalX, goalY   = goal
    nQ = set()
    prev = dict()
    
    dist = {(startX, startY) : 0}

    cdef int i, j, d
    for i in range((x1-x0+1) * (y1-y0+1)):
        d = libc.limits.INT_MAX
        for x, j in dist.items():
            if j < d and (x not in nQ):
                d = j
                minDistPoint = x

        if minDistPoint == goal: # Mathematical proof of correctness?
            break

        nQ.add(minDistPoint)
        del dist[minDistPoint]

        for neighbor in neighborsOf(minDistPoint):
            if neighbor in nQ:
                continue
            alt = d + 1 + distance(neighbor, goal) # A* like
            if neighbor not in dist.keys() or alt < dist[neighbor]:
                dist[neighbor] = alt
                prev[neighbor] = minDistPoint
    return prev

def searchPath(area, start, goal):
    if start == goal:
        return [start]

    prev = dijkstra(area, start, goal)
    if goal not in prev.keys(): # No path
        return None

    ret = [goal]
    while ret[0] in prev.keys():
        ret = [prev[ret[0]]] + ret
    return ret

