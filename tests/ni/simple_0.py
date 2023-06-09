#!/usr/bin/python

from __future__ import print_function

from verif_msi import *

k0 = symbol('k0', 'S', 8)
k1 = symbol('k1', 'S', 8)
m = symbol('m', 'M', 8)

u0, u1, u2 = getRealShares(k0, 3)
v0, v1, v2 = getRealShares(k1, 3)

e = u0 ^ m ^ u1 ^ u2
#print('e : %s' % e)
res = checkNIVal(e, 2)
# True expected
if res[0]:
    print('OK')
else:
    print('KO')


e = u0 ^ v0 ^ u1 ^ u2
#print('e : %s' % e)
res = checkNIVal(e, 2)
# False expected
if not res[0]:
    print('OK')
else:
    print('KO')



