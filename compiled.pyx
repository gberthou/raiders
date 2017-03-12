from sfml import sf
import constants as cst

def visibleMapVertexArray(x0, x1, y0, y1, mapWidth, tilemap):
    w = x1 - x0 + 1
    h = y1 - y0 + 1

    if w < 0 or h < 0:
        return None
        
    quads = sf.VertexArray(sf.PrimitiveType.QUADS, 4 * w * h)
    tiles = tilemap["tiles"]
    i = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            p0 = quads[i]
            p1 = quads[i+1]
            p2 = quads[i+2]
            p3 = quads[i+3]

            p0.position = (x*cst.TILE_SIZE, y*cst.TILE_SIZE)
            p1.position = ((x+1)*cst.TILE_SIZE, y*cst.TILE_SIZE)
            p2.position = ((x+1)*cst.TILE_SIZE, (y+1)*cst.TILE_SIZE)
            p3.position = (x*cst.TILE_SIZE, (y+1)*cst.TILE_SIZE)
            
            j = tiles[x + y * mapWidth] - 1
            p0.tex_coords = (j*cst.TILE_SIZE      , 0)
            p1.tex_coords = ((j + 1)*cst.TILE_SIZE, 0)
            p2.tex_coords = ((j + 1)*cst.TILE_SIZE, cst.TILE_SIZE)
            p3.tex_coords = (j*cst.TILE_SIZE      , cst.TILE_SIZE)

            i += 4
    return quads

