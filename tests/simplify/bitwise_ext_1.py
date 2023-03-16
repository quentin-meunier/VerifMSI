#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


k = symbol('k', 'S', 8)
p = symbol('p', 'P', 8)

n = Extract(7, 0, ZeroExt(24, k) ^ ZeroExt(24, p) ^ ZeroExt(24, k))
print('%s' % n)

wres = p

checkResults(n, wres)



