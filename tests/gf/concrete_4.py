#!/usr/bin/python

from __future__ import print_function

from verif_msi import *

# GMul(GExp(x), GExp(y)) = GExp(x + y)

for i in range(1, 256):
    for j in range(1, 256):
        x = Const(i, 8)
        y = Const(j, 8)
        ex = GExp(x)
        ey = GExp(y)
        m = GMul(ex, ey)
        a = x + y
        if x.cst + y.cst >= 256:
            a += constant(1, 8)
        ea = GExp(a)
        if m != ea:
            print('x = %s' % (x))
            print('y = %s' % (y))
            print('Exp(%s) = %s' % (x, ex))
            print('Exp(%s) = %s' % (y, ey))
            print('GMul(%s, %s) = %s' % (ex, ey, m))
            print('%s + %s = %s' % (x, y, a))
            print('GExp(%s) = %s' % (a, ea))
            print('##################')





