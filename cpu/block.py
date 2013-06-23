# -*- coding: utf-8 -*-
"""
ブロック関連のVerilogを出力するためのスクリプト
"""

from block_def import tiles, NUM_TILES, widths, heights

### parameters for drawing

CELL_WIDTH = 5
CELL_GAP = 1
CELL_UNIT = CELL_WIDTH + CELL_GAP
TILE_GAP = 4

# bcell: cell board
BCELL_WIDTH = 30
BCELL_GAP = 2
BCELL_UNIT = BCELL_WIDTH + BCELL_GAP
NUM_CELL_PER_LINE = 14
BOARD_WIDTH = BCELL_WIDTH * NUM_CELL_PER_LINE + BCELL_GAP * (NUM_CELL_PER_LINE + 1)
BOARD_LEFT = (640 - BOARD_WIDTH) / 2
BOARD_TOP = (480 - BOARD_WIDTH) / 2
BOARD_RIGHT = BOARD_LEFT + BOARD_WIDTH
BOARD_BOTTOM = BOARD_TOP + BOARD_WIDTH

SIDEBAR_WIDTH = 43
LSIDE_RIGHT = BOARD_LEFT - TILE_GAP
LSIDE_LEFT = LSIDE_RIGHT - SIDEBAR_WIDTH
RSIDE_LEFT = BOARD_RIGHT + TILE_GAP
RSIDE_RIGHT = RSIDE_LEFT + SIDEBAR_WIDTH

### decide drawing position

x = LSIDE_LEFT
y = BOARD_TOP
next_ystep = 0
left_tile_positions = []
right_tile_positions = []
for i in range(NUM_TILES):
    w = widths[i]
    h = heights[i]
    tile = tiles[i]
    right = x + w * CELL_UNIT
    if right >= LSIDE_RIGHT:
        right = right - (x - LSIDE_LEFT)
        x = LSIDE_LEFT
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

fo = open('VGA_drawing.v', 'w')
SIDE_VRAM_SIZE = SIDEBAR_WIDTH * BOARD_WIDTH
print "%d x %d = %d" % (
    SIDEBAR_WIDTH, BOARD_WIDTH, SIDE_VRAM_SIZE)

ORANGE = "12'he70"
PURPLE = "12'h70e"

fo.write("""
    assign board_x = ((x - {BOARD_LEFT}) / {BCELL_UNIT})[3:0];
    assign board_y = ((y - {BOARD_TOP}) / {BCELL_UNIT})[3:0];
    assign board_vram_addr = (board_x + board_y * d{NUM_CELL_PER_LINE})[7:0];
    assign leftside_addr = x - {LSIDE_LEFT} + (y - {BOARD_TOP}) * {SIDEBAR_WIDTH};
    assign rightside_addr = {SIDE_VRAM_SIZE} - 2 - (x - {RSIDE_LEFT} + (y - {BOARD_TOP}) * {SIDEBAR_WIDTH}); // It works but why -2?

    assign color =
    x >= {BOARD_LEFT} && y >= {BOARD_TOP} && x < {BOARD_RIGHT} && y < {BOARD_BOTTOM} ? (
        (x - {BOARD_LEFT}) % {BCELL_UNIT} < {BCELL_GAP} || (y - {BOARD_TOP}) % {BCELL_UNIT} < {BCELL_GAP} ? 12'hccc :
        board_vram_out & 6'b100000 ? {ORANGE} :
        board_vram_out & 6'b000100 ? {PURPLE} :
        12'hddd
    ) :
    (x < {LSIDE_RIGHT} && x >= {LSIDE_LEFT}) & leftside_out ? {ORANGE}:
    (x < {RSIDE_RIGHT} && x >= {RSIDE_LEFT}) & rightside_out ? {PURPLE}:
    12'heee
    ;
""".format(**locals()))

## sidebar

bitmap = {}
for lpos in left_tile_positions:
    for left, top in lpos:
        x = left - LSIDE_LEFT
        y = top - BOARD_TOP
        for dx in range(CELL_WIDTH):
            for dy in range(CELL_WIDTH):
                pos = x + dx + (y + dy) * SIDEBAR_WIDTH
                bitmap[pos] = 1

import write_mif
write_mif.write(bitmap)



### valid hand
for i in range(NUM_TILES):
    w = widths[i]
    h = heights[i]
    #broaden = [[0] * (w + 2) for _i in range(h + 2)]
    broaden = [[0] * 5 for _i in range(7)] # 5x7
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

    for y in range(7):
        for x in range(5):
            v = broaden[y][x]
            if v & 0b100:
                v = 0b100
            elif v & 0b10:
                v = 0b10
            elif v & 0b1:
                v = 0b1
            else:
                v = 0b0
            #print ' .+ *'[v],
            broaden[y][x] = v
        #print

    print center
    for y in range(7):
        for x in range(5):
            print broaden[y][x],
    print
