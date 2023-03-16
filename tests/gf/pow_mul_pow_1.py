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
w = symbol('w', 'P', 8)
a = symbol('a', 'P', 8)
b = symbol('b', 'P', 8)
c = symbol('c', 'P', 8)
d = symbol('d', 'P', 8)

e = GMul(GPow(s + t, w), a, b, GPow(x, y), GPow(x, z), c, GPow(s + t, u), d, GPow(s + t, v))

e = simplify(e)
res = GMul(GPow(s + t, u + v + w), GPow(x, y + z), a, b, c, d)

checkResults(e, res)






