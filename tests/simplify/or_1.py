#!/usr/bin/python

from __future__ import print_function

from verif_msi import *



k0 = symbol('k0', 'S', 8)
k1 = symbol('k1', 'S', 8)
k2 = symbol('k2', 'S', 8)
c0 = constant(0, 8)

n0 = c0 | k0 | k0 | c0 | c0 | k1 | c0 | k0 | k0 | k1 | k2 | c0 | k2 | c0 | k1 | k0 | c0
# result is k0 & k1 & k2
wres = k1 | k2 | k0

checkResults(n0, wres)

n0.dump('graph.dot')


