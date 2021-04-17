#!/usr/bin/env python

# converts .MAX (CoCo Max) to .PNG
#
# usage: max2png.py LINCOLN.MAX lincoln.png
# 
# Copyright (C) 2016 Erik Gavriluk
# Released under the Artistic License 2.0
# https://opensource.org/licenses/Artistic-2.0

from __future__ import print_function, division
import argparse
import png #pip install pypng
import sys


def main():
    p = argparse.ArgumentParser(description='Convert CoCo Max images to PNG', epilog='Copyright 2016 Erik Gavriluk. Released under the Artistic License 2.0.')
    p.add_argument('infile', help='input .max file')
    p.add_argument('outfile', help='output .png file')
    p.add_argument('--color', action='store_true', help='generate an artifact color image')
    p.add_argument('--swap', action='store_true', help='swap blue/orange')

    if len(sys.argv[1:]) == 0:
        p.print_help()
        p.exit()

    arg = p.parse_args()

    palette = [
        (0x00,0x00,0x00),   # black
        (0x00,0x80,0xff),   # blue
        (0xff,0x80,0x00),   # orange
        (0xff,0xff,0xff)    # white
        ]

    if arg.swap:
        palette[1], palette[2] = palette[2], palette[1]

    bits = [ 128, 64, 32, 16, 8, 4, 2, 1 ]

    with open(arg.infile, 'rb') as file:
        data = bytearray(file.read())
        
    width = 256
    size = data[1] * width + data[0]
    height = size // 32
    bitmap = [0] * (width * height)

    j = 0
    for byte in data[5:]:
        if not arg.color:
            for bit in bits:
                bitmap[j] = 3 if byte & bit else 0
                j += 1
        else:
            bitmap[j]   = bitmap[j+1] = byte >> 6
            bitmap[j+2] = bitmap[j+3] = (byte & 0b00110000) >> 4
            bitmap[j+4] = bitmap[j+5] = (byte & 0b00001100) >> 2
            bitmap[j+6] = bitmap[j+7] = byte & 0b00000011
            j += 8
        if j == width * height: break

    with open(arg.outfile, 'wb') as file:
        img = png.Writer(width=width, height=height, bitdepth=8, palette=palette)
        img.write_array(file, bitmap)

