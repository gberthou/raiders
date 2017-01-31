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
    path = dijkstra.searchPath(area, start, goal)
    t.append(time.time() - a)

# NetPBM output, can be converted to png using:
# dikjstraTest.py | convert /dev/stdin path.png
path_offset = 50
background_color = (0x0, 0x0, 0x0)
start_color = (0x00, 0x00, 0xFF)
goal_color =  (0xFF, 0x00, 0x00)

img = collections.defaultdict(lambda: background_color)
for k, point in enumerate(path):
    grey = int(k/len(path) * (0xFF-path_offset))+path_offset
    img[point] = (grey, grey, grey)

img[start] = start_color
img[goal] = goal_color

print('P3')
print(str(area[2])+' '+str(area[3]))
print(255)
for i in range(area[2]):
    for j in range(area[3]):
        print(' '.join(str(component) for component in img[i, j]), end=' ')
    print('')

print(statistics.mean(t), file=sys.stderr)
print(statistics.stdev(t), file=sys.stderr)

