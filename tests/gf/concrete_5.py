#!/usr/bin/python

from __future__ import print_function

from verif_msi import *

# GMul(GPow(x, c0), GPow(x, c1)) = GPow(x, c0 + c1)

for i in range(1, 256):
    for j in range(1, 256):
        x = Const(i, 8)
        c = Const(j, 8)
        p = GPow(x, c)
        m = GMul(p, p)
        a = c + c
        if c.cst + c.cst >= 256:
            a += constant(1, 8)
        pa = GPow(x, a)
        if m != pa:
            print('x = %s' % (x))
            print('c = %s' % (c))
            print('Pow(%s, %s) = %s' % (x, c, p))
            print('GMul(%s, %s) = %s' % (p, p, m))
            print('%s + %s = %s' % (c, c, a))
            print('GPow(%s, %s) = %s' % (x, a, pa))
            print('##################')





