#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


x = symbol('x', 'P', 8)
y = symbol('y', 'P', 8)
z = symbol('z', 'P', 8)
u = symbol('u', 'P', 8)
v = symbol('v', 'P', 8)
w = symbol('w', 'P', 8)

e = u + GLog(x) + v + GLog(y) + w + GLog(z)

e = simplify(e)
res = u + v + w + GLog(GMul(x, y, z))

checkResults(e, res)






