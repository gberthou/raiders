import dijkstra
import time
import statistics

area  = (0, 0, 70, 70)
start = (10, 10)
goal  = (40, 60)

t = []
N = 10
for i in range(N):
    a = time.time()
    tmp = dijkstra.searchPath(area, start, goal)
    t.append(time.time() - a)

print(statistics.mean(t))
print(statistics.stdev(t))

