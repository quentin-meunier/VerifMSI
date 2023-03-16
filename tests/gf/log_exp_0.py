#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


# Glog(x) + Glog(y) = GLog(GMul(x, y))

x = symbol('x', 'P', 8)

e = simplify(GLog(GExp(x)))

checkResults(e, x)






