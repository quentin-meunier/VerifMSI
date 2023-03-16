#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


x = symbol('x', 'P', 8)
y = symbol('y', 'P', 8)
z = symbol('z', 'P', 8)
t = symbol('t', 'P', 8)
u = symbol('u', 'P', 8)
v = symbol('v', 'P', 8)
w = symbol('w', 'P', 8)
a = symbol('a', 'P', 8)
b = symbol('b', 'P', 8)

e = u ^ GPow(x, Const(16, 8)) ^ GPow(y, Const(16, 8)) ^ GPow(z, Const(16, 8)) ^ v ^ w ^ GPow(t, Const(32, 8)) ^ GPow(a, Const(64, 8)) ^ GPow(b, Const(64, 8))

e = simplify(e)
res = u ^ v ^ w ^ GPow(x ^ y ^ z, Const(16, 8)) ^ GPow(a ^ b, Const(64, 8)) ^ GPow(t, Const(32, 8))

checkResults(e, res)






