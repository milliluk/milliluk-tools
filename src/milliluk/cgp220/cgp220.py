#!/usr/bin/env python

# emulates Tandy CGP-220 printer (Canon PJ-1080A)
#
# usage: cgp220.py infile.prn outfile.png
# 
# infile.prn: captured RS-232 output
# outfile.png: rendered as a .png 
#
# Copyright (C) 2015 Erik Gavriluk
# Released under the Artistic License 2.0
# https://opensource.org/licenses/Artistic-2.0

from __future__ import print_function, division
import argparse
import colorsys
import png #pip install pypng
import sys


def main():
    p = argparse.ArgumentParser(description='Convert CGP-220 printer output to a PNG', epilog='Copyright 2015 Erik Gavriluk. Released under the Artistic License 2.0.')
    p.add_argument('infile', help='input file containing raw printer dump')
    p.add_argument('outfile', help='output filename for PNG')
    p.add_argument('-c', action="store_false", default=True, help='block cyan')
    p.add_argument('-m', action="store_false", default=True, help='block magenta')
    p.add_argument('-y', action="store_false", default=True, help='block yellow')
    p.add_argument('-k', action="store_false", default=True, help='block black')
    p.add_argument('-d', action="store", type=int, help='desaturate (0-100)')

    if len(sys.argv[1:]) == 0:
        p.print_help()
        p.exit()

    arg = p.parse_args()

    width = 960
    height = 600
    bitmap = [0] * (width*height)
    palette = [
        (0xff,0xff,0xff),   # white
        (0xff,0xff,0x00),   # yellow
        (0x7f,0x00,0xff),   # violet
        (0xff,0x00,0x00),   # red
        (0xff,0x00,0xff),   # magenta
        (0x00,0xff,0x00),   # green
        (0x00,0x00,0xff),   # blue
        (0x00,0x00,0x00)    # black
        ]
    bitset = [ 128, 64, 32, 16, 8, 4, 2, 1 ]

    if arg.d is not None:
        desat = 1 - (arg.d / 100)
        for i in range(len(palette)):
            p = palette[i]
            p = colorsys.rgb_to_hsv(p[0]/255, p[1]/255, p[2]/255)
            p = colorsys.hsv_to_rgb(p[0], p[1]*desat, p[2]*desat)
            palette[i] = int(p[0]*255), int(p[1]*255), int(p[2]*255)

    with open(arg.infile, 'rb') as file:
        data = bytearray(file.read())
        
        # skip to first ESC
        for i in range(len(data)):
            if data[i] == 0x1b:
                break
        
        x = width-1
        y = 0

        while i < len(data):
            if data[i] == 0x0d:
                break

            if data[i] != 0x1b and data[i+1] != 0x43 or data[i+2] != 0x4b:
                raise Exception('sync error')

            i += 3

            for k in range(0, 75):
                for b in bitset:
                    cc = 0 if (data[i] & b) and arg.c else 4
                    mm = 0 if (data[i+75] & b) and arg.m else 2
                    yy = 0 if (data[i+150] & b) and arg.y else 1
                    bitmap[y * width + x] = cc | mm | yy
                    y += 1
                i += 1

            i += 150
            y = 0
            x -= 1

    with open(arg.outfile, 'wb') as file:
        img = png.Writer(width=width, height=height, bitdepth=4, palette=palette)
        img.write_array(file, bitmap)

