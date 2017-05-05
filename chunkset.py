from sfml import sf
import constants as cst
import math

CHUNK_DIM = 64

class ChunkSet:
    def __init__(self, mapdata):
        self.mapWidth  = mapdata["width"]
        self.mapHeight = mapdata["height"]
        self.tiles     = mapdata["tiles"]

        self.nChunksX = math.ceil(self.mapWidth / CHUNK_DIM)
        self.nChunksY = math.ceil(self.mapHeight / CHUNK_DIM)
        self.chunks = [sf.VertexArray(sf.PrimitiveType.QUADS, 4 * CHUNK_DIM * CHUNK_DIM) for i in range(self.nChunksX * self.nChunksY)]

        for cY in range(self.nChunksY):
            for cX in range(self.nChunksX):
                self.refreshChunk(cX, cY)

    def refreshChunk(self, cX, cY):
        chunk = self.chunks[cX + cY * self.nChunksX]
        i = 0
        for y in range(cY * CHUNK_DIM, min((cY+1) * CHUNK_DIM, self.mapHeight)):
            for x in range(cX * CHUNK_DIM, min((cX+1) * CHUNK_DIM, self.mapWidth)):
                p0 = chunk[i]
                p1 = chunk[i+1]
                p2 = chunk[i+2]
                p3 = chunk[i+3]

                p0.position = (x*cst.TILE_SIZE, y*cst.TILE_SIZE)
                p1.position = ((x+1)*cst.TILE_SIZE, y*cst.TILE_SIZE)
                p2.position = ((x+1)*cst.TILE_SIZE, (y+1)*cst.TILE_SIZE)
                p3.position = (x*cst.TILE_SIZE, (y+1)*cst.TILE_SIZE)
                
                j = self.tiles[x + y * self.mapWidth] - 1
                p0.tex_coords = (j*cst.TILE_SIZE      , 0)
                p1.tex_coords = ((j + 1)*cst.TILE_SIZE, 0)
                p2.tex_coords = ((j + 1)*cst.TILE_SIZE, cst.TILE_SIZE)
                p3.tex_coords = (j*cst.TILE_SIZE      , cst.TILE_SIZE)

                i += 4

    def visibleChunks(self, x0, x1, y0, y1):
        ret = []
        x0 = max(0, x0)
        y0 = max(0, y0)
        x1 = min(self.mapWidth - 1, x1)
        y1 = min(self.mapHeight - 1, y1)
        for y in range(math.floor(y0 / CHUNK_DIM), math.ceil(y1 / CHUNK_DIM)):
            for x in range(math.floor(x0 / CHUNK_DIM), math.ceil(x1 / CHUNK_DIM)):
                ret.append(self.chunks[x + y * self.nChunksX])
        return ret

