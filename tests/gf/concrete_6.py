#!/usr/bin/python

from __future__ import print_function

from verif_msi import *

# GPow(x, n) ^ GPow(y, n) = GPow(x ^ y, n)

exp = [2, 4, 8, 16, 32, 64, 128]
for e in exp:
    n = constant(e, 8)
    for i in range(0, 256):
        for j in range(0, 256):
            x = Const(i, 8)
            y = Const(j, 8)
            py = GPow(x, n)
            px = GPow(y, n)
            r = px ^ py
            p = GPow(x ^ y, n)
            if r != p:
                print('x = %s' % (x))
                print('y = %s' % (y))
                print('Pow(%s, %s) = %s' % (x, n, px))
                print('Pow(%s, %s) = %s' % (y, n, py))
                print('%s ^ %s = %s' % (px, py, r))
                print('%s ^ %s = %s' % (x, y, x ^ y))
                print('GPow(%s, %s) = %s' % (x ^ y, n, p))
                print('##################')





