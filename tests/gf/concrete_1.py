#!/usr/bin/python

from __future__ import print_function

from verif_msi import *

# GMul(cst, GLog(x)) = GLog(GPow(x, cst))

for i in range(1, 256):
    for j in range(1, 256):
        cst = Const(i, 8)
        x = Const(j, 8)
        lx = GLog(x)
        m = GMul(cst, lx)
        p = GPow(x, cst)
        lp = GLog(p)
        if m != lp:
            print('cst = %s' % (cst))
            print('x = %s' % (x))
            print('Log(%s) = %s' % (x, lx))
            print('%s * Log(%s) = %s' % (cst, x, m))
            print('Pow(%s, %s) = %s' % (x, cst, p))
            print('Log(%s) = %s' % (p, lp))
            print('##################')





