#!/usr/bin/python

from __future__ import print_function

from verif_msi import *

# GLog(GExp(x)) = x

for i in range(0, 256):
    x = Const(i, 8)
    e = GExp(x)
    l = GLog(e)
    if l != x:
        print('x = %s' % (x))
        print('Exp(%s) = %s' % (x, e))
        print('Log(%s) = %s' % (e, l))
        print('##################')





