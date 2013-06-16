# -*- coding: utf-8 -*-
"""
ブロック関連のVerilogを出力するためのスクリプト
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

### parameters for drawing

CELL_WIDTH = 7
CELL_GAP = 1
CELL_UNIT = CELL_WIDTH + CELL_GAP
TILE_GAP = 10

BCELL_WIDTH = 30
BCELL_GAP = 2
BCELL_UNIT = BCELL_WIDTH + BCELL_GAP
NUM_CELL_PER_LINE = 14
BOARD_WIDTH = BCELL_WIDTH * NUM_CELL_PER_LINE + BCELL_GAP * (NUM_CELL_PER_LINE + 1)
BOARD_LEFT = (640 - BOARD_WIDTH) / 2
BOARD_TOP = (480 - BOARD_WIDTH) / 2
TILE_SPACE_RIGHT = BOARD_LEFT - TILE_GAP
TILE_SPACE_LEFT = TILE_GAP

### decide drawing position

x = TILE_SPACE_LEFT
y = BOARD_TOP
next_ystep = 0
left_tile_positions = []
right_tile_positions = []
for i in range(NUM_TILES):
    w = widths[i]
    h = heights[i]
    tile = tiles[i]
    right = x + w * CELL_UNIT
    if right >= TILE_SPACE_RIGHT:
        right = right - (x - TILE_SPACE_LEFT)
        x = TILE_SPACE_LEFT
        y += next_ystep
        next_ystep = 0

    lpos = []
    left_tile_positions.append(lpos)
    rpos = []
    right_tile_positions.append(rpos)
    for j, line in enumerate(tile):
        for i, c in enumerate(line):
            if c != ' ':
                cx = x + i * CELL_UNIT
                cy = y + j * CELL_UNIT
                lpos.append((cx, cy))
                rpos.append((640 - cx - CELL_WIDTH, 480 - cy - CELL_WIDTH))

    next_ystep = max(next_ystep, h * CELL_UNIT + TILE_GAP)
    x = right + TILE_GAP

### debug output as HTML

fo = open('tmp.html', 'w')
TEMPLATE = "<span style='position: absolute; left: %d; top: %d; width: %d; height: %d; background: %s;'> </span>"
fo.write(TEMPLATE % (0, 0, 640, 480, 'lightgrey'))
fo.write(TEMPLATE % (BOARD_LEFT, BOARD_TOP, BOARD_WIDTH, BOARD_WIDTH, 'grey'))

for i in range(NUM_CELL_PER_LINE):
    for j in range(NUM_CELL_PER_LINE):
        fo.write(TEMPLATE % (
                BOARD_LEFT + BCELL_GAP + i * BCELL_UNIT,
                BOARD_TOP + BCELL_GAP + j * BCELL_UNIT,
                BCELL_WIDTH, BCELL_WIDTH, 'lightgrey'))

for lpos in left_tile_positions:
    for left, top in lpos:
        fo.write(TEMPLATE % (left, top, CELL_WIDTH, CELL_WIDTH, 'orange'))
for rpos in right_tile_positions:
    for left, top in rpos:
        fo.write(TEMPLATE % (left, top, CELL_WIDTH, CELL_WIDTH, 'purple'))

### generate verilog for drawing

## given
# x == hcount - 144, y == vcount - 35
# [20:0] left_available;
# [20:0] right_available;
# reg [5:0] board [0:196];

if 0:
    def if_x(r, v):
        return "hcount %s %d" % (r, v + 144)

    def if_y(r, v):
        return "vcount %s %d" % (r, v + 35)

def if_x(r, v):
    return "x %s %d" % (r, v)

def if_y(r, v):
    return "y %s %d" % (r, v)


def all_and(*xs):
    return ' && '.join(xs)

fo = open('tmp.v', 'w')
fo.write("assign color = \n")

# wireでxとyを作ることができるか？→もとからwireだった
# コード上で引き算の引き算をした場合に合成結果では最適化されるか？→されるだろJK
# VGAの出力を4bitに増やす
# とりあえず中身空っぽで盤の枠の表示
# RAMの内容の初期化の方法を調べる
# 手持ちコマRAMの内容を初期化

# board
is_board = all_and(
    if_x(">=", BOARD_LEFT),
    if_y(">=", BOARD_TOP),
    if_x("<=", BOARD_LEFT + BOARD_WIDTH),
    if_y("<=", BOARD_TOP + BOARD_WIDTH))

is_board_border = (
    "(x - %(BOARD_LEFT)d) %% %(BCELL_UNIT)d < 2"
    " || "
    "(y - %(BOARD_TOP)d) %% %(BCELL_UNIT)d < 2"
) % locals()

board_cell_color = (
    "board[{(x - %(BOARD_LEFT)d) / %(BCELL_UNIT)d, "
    "(y - %(BOARD_TOP)d) %% %(BCELL_UNIT)d}]"
) % locals()

print is_board
print is_board_border
print board_cell_color

#def rect(left, top, width, height):
#    return (
#        "hcount > %d && hcount < %d && vcount > %d && vcount < %d"
#        % (left + 144, left + 144 + width, top + 35, top + 35 + height))

def rect(left, top, width, height):
    return (
        "x >= %d && x < %d && y >= %d && y < %d"
        % (left, left + width, top, top + height))

def template(cond, color):
    fo.write("%s ? " % cond + color + ":\n")

ORANGE = "6'b111000"
PURPLE = "6'b010011"
for i in range(NUM_CELL_PER_LINE):
    for j in range(NUM_CELL_PER_LINE):
        left = BOARD_LEFT + BCELL_GAP + i * BCELL_UNIT
        top = BOARD_TOP + BCELL_GAP + j * BCELL_UNIT
        w = BCELL_WIDTH
        pos = i * NUM_CELL_PER_LINE + j
        template(
            rect(left, top, w, w) + " && board[%d][0]" % pos, ORANGE)
        template(
            rect(left, top, w, w) + " && board[%d][1]" % pos, PURPLE)

"""
TODO

fo.write(TEMPLATE % (BOARD_LEFT, BOARD_TOP, BOARD_WIDTH, BOARD_WIDTH, 'grey'))

for lpos in left_tile_positions:
    for left, top in lpos:
        fo.write(TEMPLATE % (left, top, CELL_WIDTH, CELL_WIDTH, 'orange'))
for rpos in right_tile_positions:
    for left, top in rpos:
        fo.write(TEMPLATE % (left, top, CELL_WIDTH, CELL_WIDTH, 'purple'))
"""

fo.write("6'111111;");

### valid hand
for i in range(NUM_TILES):
    w = widths[i]
    h = heights[i]
    broaden = [[0] * (w + 2) for _i in range(h + 2)]
    tile = tiles[i]
    for y in range(h):
        for x in range(w):
            if tile[y][x] != ' ':
                broaden[y + 1][x + 1] |= 0b100
                # edge
                broaden[y + 0][x + 1] |= 0b10
                broaden[y + 1][x + 0] |= 0b10
                broaden[y + 2][x + 1] |= 0b10
                broaden[y + 1][x + 2] |= 0b10
                # corner
                broaden[y + 0][x + 0] |= 0b1
                broaden[y + 0][x + 2] |= 0b1
                broaden[y + 2][x + 0] |= 0b1
                broaden[y + 2][x + 2] |= 0b1
            if tile[y][x] == 'x':
                center = x + 1 + (y + 1) * NUM_CELL_PER_LINE

    for y in range(h + 2):
        for x in range(w + 2):
            v = broaden[y][x]
            if v & 0b100:
                v = 0b100
            elif v & 0b10:
                v = 0b10
            elif v & 0b1:
                v = 0b1
            else:
                v = 0b0

    for y in range(h + 2):
        for x in range(w + 2):
            pass
            'TODO:座標+3bitの列を吐く、長さセットで'
            '100のところの座標の列を吐く、長さセットで？ハードな回路で？'
            'center'
