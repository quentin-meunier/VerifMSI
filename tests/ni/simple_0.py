#!/usr/bin/python

from __future__ import print_function

from verif_msi import *

k0 = symbol('k0', 'S', 8)
k1 = symbol('k1', 'S', 8)
m = symbol('m', 'M', 8)

u0, u1, u2 = getPseudoShares(k0, 3)
v0, v1, v2 = getPseudoShares(k1, 3)

e = u0 ^ m ^ u1 ^ u2
print('e : %s' % e)
res = checkTpsVal(e)
print('Result: %r (True expected)' % res[0])

e = u0 ^ v0 ^ u1 ^ u2
print('e : %s' % e)
res = checkTpsVal(e)
print('Result: %r (True expected)' % res[0])


