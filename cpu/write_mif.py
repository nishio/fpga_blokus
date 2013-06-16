# -*- coding: utf-8 -*-
"""
mif形式で出力するためのスクリプト
"""


TEMPLATE = """
WIDTH={WIDTH};
DEPTH={DEPTH};

ADDRESS_RADIX=UNS;
DATA_RADIX=UNS;

CONTENT BEGIN
{contents}
END;
"""


def write(bitmap):
    WIDTH = 1
    if WIDTH != 1: raise NotImplemented

    DEPTH = 39150
    contents = []
    for i in range(DEPTH):
        if bitmap.get(i):
            contents.append("%d : 1;" % i)
        else:
            contents.append("%d : 0;" % i)

    contents = '\n'.join(contents)

    fo = file('side.mif', 'w')
    fo.write(TEMPLATE.format(**locals()))
    fo.close()
