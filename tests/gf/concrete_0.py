#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


# Glog(x) + Glog(y) = GLog(GMul(x, y))

for i in range(1, 256):
    for j in range(1, 256):
        c0 = Const(i, 8)
        c1 = Const(j, 8)
        g0 = GLog(c0)
        g1 = GLog(c1)
        m = GMul(c0, c1)
        g2 = GLog(m)
        ad = g0 + g1
        if g0.cst + g1.cst >= 255:
            ad += constant(1, 8)
        if ad != g2:
            print('Log(%s) = %s' % (c0, g0))
            print('Log(%s) = %s' % (c1, g1))
            print('Log(%s) + Log(%s) = %s' % (c0, c1, g0 + g1))
            print('%s * %s = %s' % (c0, c1, m))
            print('Log(%s * %s) = %s' % (c0, c1, g2))
            print('##################')





