#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


x = symbol('x', 'P', 8)
y = symbol('y', 'P', 8)
z = symbol('z', 'P', 8)

e = GLog(x) + GLog(y)

e = simplify(e)
res = GLog(GMul(x, y))

checkResults(e, res)






