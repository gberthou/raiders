# All coordinates are in tile space

def neighborsOf(pos):
    x, y = pos
    return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

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
        minDist = min([dist[i] for i in dist.keys() if i in Q])
        minDistPoint = [i for i in dist.keys() if i in Q and dist[i] == minDist][0]
        Q.remove(minDistPoint)

        d = dist[minDistPoint]
        for neighbor in neighborsOf(minDistPoint):
            if not neighbor in Q:
                continue
            alt = d + 1
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


### Test here
area  = (0, 0, 100, 100)
start = (4, 3)
goal  = (10, 7)

print(searchPath(area, start, goal))

