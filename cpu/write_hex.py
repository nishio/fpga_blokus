# -*- coding: utf-8 -*-
"""
hex形式で出力するためのファイル
"""

BITWIDTH = 2  # bytes
NUM_WORDS = 196
DATA_FORMAT = "%%0%dX" % BITWIDTH

data_map = {74: 0b100000, 196 - 75: 0b000100}

for addr in range(NUM_WORDS):
    data = data_map.get(addr, 0)
    checksum = 256 - (
        BITWIDTH +
        (addr / 256) + (addr % 256) +
        data) % 256

    datas = DATA_FORMAT % data
    print (
        ":"
        "%(BITWIDTH)02X"
        "%(addr)04X"
        "00"  # means 'data record'
        "%(datas)s"
        "%(checksum)02X"
    ) % locals()

print ":00000001FF"  # means 'end record'

