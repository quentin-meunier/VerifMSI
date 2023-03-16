#!/usr/bin/python

from __future__ import print_function

from verif_msi import *

k0 = symbol('k0', 'S', 8)
k1 = symbol('k1', 'S', 8)
m = symbol('m', 'M', 8)

a0, a1, a2 = getPseudoShares(k0, 3)
b0, b1, b2 = getPseudoShares(k1, 3)

e = a0 ^ a1 ^ b1 ^ b2
e = e | (a0 & b1)

print('e : %s' % e)
res = checkTpsVal(e)
print('Result: %r (True expected)' % res[0])

f = (a2 ^ m ^ b0)
g = Concat(e, f)

res = checkTpsVal(g)
print('Result: %r (True expected)' % res[0])



