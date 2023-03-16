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

e = GMul(s, GExp(x), t, GExp(y), u, GExp(z), v)

e = simplify(e)
res = GMul(s, t, u, v, GExp(x + y + z))

checkResults(e, res)






