# -*- coding: utf-8 -*-
"""
ブロックの定義
"""

data = """
x

x
o

o
x
o

o
xo

o
x
o
o

 o
 x
oo

o
xo
o

xo
oo

ox
 oo

o
o
x
o
o

 o
 o
 x
oo

 o
 o
ox
o

 o
ox
oo

oo
 x
oo

o
xo
o
o

 o
 x
ooo

o
o
xoo

oo
 xo
  o

o
oxo
  o

o
oxo
 o

 o
oxo
 o
"""

NUM_TILES = 21
tiles = [x.strip('\n').split('\n') for x in data.split('\n\n')]
assert len(tiles) == NUM_TILES

heights = map(len, tiles)
widths = [max(len(line) for line in x) for x in tiles]

for i in range(NUM_TILES):
    w = widths[i]
    h = heights[i]
    tile = tiles[i]
    for y in range(h):
        tile[y] = tile[y].ljust(w)
