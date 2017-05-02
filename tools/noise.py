import random
from math import sqrt

EPSILON = 0.001

def d2(a, b):
    return ((a[0]-b[0])**2) + ((a[1]-b[1])**2)

def fade(x):
    #return x
    return 6*(x**5) - 15*(x**4) + 10*(x**3)

def lerp(a0, a1, w):
    w = fade(w)
    return (1-w) * a0 + w * a1

def genVec():
    l2 = 0

    while l2 < EPSILON**2:
        x  = random.random()
        y  = random.random()
        l2 = x*x + y*y

    l = sqrt(l2)
    return (x/l, y/l)

class MyNoise:
    def __init__(self, w, h, count):
        self.vertices = [(random.random() * w, random.random() * h, random.random()) for i in range(count)]

    def at(self, x, y):
        distances = [d2(i, (x, y))**-1.4 for i in self.vertices]
        l = sum(distances)
        z = [i[2] for i in self.vertices]
        return sum(map(lambda x: x[0]*x[1], zip(distances, z))) / l

    def slopeAt(self, x, y):
        H = 1e-4
        df_dx = (self.at(x + H/2, y) - self.at(x - H/2, y)) / H
        df_dy = (self.at(x, y + H/2) - self.at(x, y - H/2)) / H
        return (df_dx, df_dy)

    def normalizedSlopeAt(self, x, y):
        slope = self.slopeAt(x, y)
        l_slope = sqrt(d2((0, 0), slope))
        return (slope[0] / l_slope, slope[1] / l_slope)

    def localExtremum(self, x, y):
        DELTA = 1e-3
        pos_min = (x, y)
        pos_max = (x, y)

        current_min = self.at(x, y)
        current_max = current_min

        for i in range(1000):
            slope_min = self.normalizedSlopeAt(pos_min[0], pos_min[1])
            proposal_min = (pos_min[0] - DELTA * slope_min[0], pos_min[1] - DELTA * slope_min[1])
            proposal_value = self.at(proposal_min[0], proposal_min[1])
            if proposal_value >= current_min:
                break
            current_min = proposal_value
            pos_min = proposal_min

        for i in range(1000):
            slope_max = self.normalizedSlopeAt(pos_max[0], pos_max[1])
            proposal_max = (pos_max[0] + DELTA * slope_max[0], pos_max[1] + DELTA * slope_max[1])
            proposal_value = self.at(proposal_max[0], proposal_max[1])
            if proposal_value <= current_max:
                break
            current_max = proposal_value
            pos_max = proposal_max

        if d2((x, y), pos_min) < d2((x, y), pos_max):
            return pos_min
        return pos_max

class PerlinNoise:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.data = [genVec() for i in range(w * h)]

    def nodeValueAt(self, x, y):
        if x < 0 or x >= self.w or y < 0 or y >= self.h:
            return (0, 0)
        return self.data[x + y * self.w]
    
    def gradient(self, ix, iy, x, y):
        dx = x - ix
        dy = y - iy

        value = self.nodeValueAt(ix, iy)
        return dx * value[0] + dy * value[1]

    def at(self, x, y):
        x *= self.w
        y *= self.h

        ix = int(x)
        iy = int(y)

        dx = x - ix
        dy = y - iy

        n0 = self.gradient(ix,     iy,     x, y)
        n1 = self.gradient(ix + 1, iy,     x, y)
        tmp0 = lerp(n0, n1, dx)

        n0 = self.gradient(ix,     iy + 1, x, y)
        n1 = self.gradient(ix + 1, iy + 1, x, y)
        tmp1 = lerp(n0, n1, dx)

        return lerp(tmp0, tmp1, dy)

    def slopeAt(self, x, y):

        ix = int(x)
        iy = int(y)

        points = [(ix,     iy),
                  (ix + 1, iy),
                  (ix + 1, iy + 1),
                  (ix,     iy + 1)]

        distances = [sqrt(((x-i[0])**2) + ((y-i[1])**2)) for i in points]
        totalDist = sum(distances)
        weights = [i / totalDist for i in distances]

        grads = [self.nodeValueAt(i[0], i[1]) for i in points]

        x = sum(i[0] * weights[j] for j,i in enumerate(grads))
        y = sum(i[1] * weights[j] for j,i in enumerate(grads))

        return (x, y)

