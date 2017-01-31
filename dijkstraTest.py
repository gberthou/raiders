import dijkstra
import time
import statistics
import collections
import sys

area  = (0, 0, 70, 70)
start = (10, 10)
goal  = (40, 60)

t = []
N = 10
for i in range(N):
    a = time.time()
    tmp = dijkstra.searchPath(area, start, goal)
    t.append(time.time() - a)

# NetPBM output, can be converted to png using:
# dikjstraTest.py | convert /dev/stdin path.png
img = collections.defaultdict(lambda: (0x0, 0x0, 0x0))
for i, j in tmp:
    img[i, j] = (0xFF, 0xFF, 0xFF)

img[start] = (0x00, 0x00, 0xFF)
img[goal] = (0xFF, 0x00, 0x00)

print('P3')
print(str(area[2])+' '+str(area[3]))
print(255)
for i in range(area[2]):
    for j in range(area[3]):
        print(' '.join(str(component) for component in img[i, j]), end=' ')
    print('')

print(statistics.mean(t), file=sys.stderr)
print(statistics.stdev(t), file=sys.stderr)

