#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


k0 = symbol('k0', 'S', 1)
k1 = symbol('k1', 'S', 1)
k2 = symbol('k2', 'S', 1)

m0 = symbol('m0', 'M', 1)

p1 = symbol('p1', 'P', 1)

n = m0 ^ (k1 & m0)
#print('n: %s' % n)
#print('simp : %s' % simplify(n))

r, v0, v1 = compareExpsWithExev(n, simplify(n))
if r != None:
    print('KO')
else:
    print('OK')

e0 = ~((k1 & m0) ^ (k0 ^ m0)) & p1
e1 = ~(k0 ^ m0) & p1


