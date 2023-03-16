#!/usr/bin/python

from __future__ import print_function

from verif_msi import *

# GExp(GLog(x)) = x

for i in range(1, 256):
    x = Const(i, 8)
    lx = GLog(x)
    e = GExp(lx)
    if e != x:
        print('x = %s' % (x))
        print('Log(%s) = %s' % (x, lx))
        print('Exp(%s) = %s' % (lx, e))
        print('##################')





