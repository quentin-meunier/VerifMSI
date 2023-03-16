#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


x = symbol('x', 'P', 8)
y = symbol('y', 'P', 8)
z = symbol('z', 'P', 8)
s = symbol('s', 'P', 8)
t = symbol('t', 'P', 8)
u = symbol('u', 'P', 8)
v = symbol('v', 'P', 8)

e = GMul(constant(0x3, 8), GLog(x), y, constant(0x2, 8))

e = simplify(e)
res = GMul(y, GLog(GPow(x, constant(0x6, 8))))

checkResults(e, res)






