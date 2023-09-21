#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


k = symbol('k', 'S', 8)

a0, a1, a2 = getRealShares(k, 3)

e0 = a0 ^ a1 ^ a2
e1 = k

r, v0, v1 = compareExpsWithRandev(e0, e1, 10)

if r == None:
    print('OK')
else:
    print('KO')



