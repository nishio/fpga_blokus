# -*- coding: utf-8 -*-
"""
hex形式で出力するためのファイル
"""

BYTES = 1
NUM_CHAR = BYTES * 2
NUM_WORDS = 196
DATA_FORMAT = "%%0%dX" % NUM_CHAR
MAX_VALUE = 256 ** BYTES

POS = 4 + 14 * 4
data_map = {POS: 0b100000, 196 - POS: 0b000100}

for addr in range(NUM_WORDS):
    data = data_map.get(addr, 0)
    assert 0 <= data < MAX_VALUE

    checksum = 256 - (
        BYTES +
        (addr / 256) + (addr % 256) +
        data) % 256

    datas = DATA_FORMAT % data
    print (
        ":"
        "%(BYTES)02X"
        "%(addr)04X"
        "00"  # means 'data record'
        "%(datas)s"
        "%(checksum)02X"
    ) % locals()

print ":00000001FF"  # means 'end record'

