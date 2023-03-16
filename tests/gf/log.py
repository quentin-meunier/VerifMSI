#!/usr/bin/python

from __future__ import print_function

from verif_msi import *



for i in range(0, 256):
        c0 = Const(i, 8)
        g0 = GLog(c0)
        print('Log(%s) = %s' % (str(int(c0.cst)), str(int(g0.cst))))





