#!/usr/bin/python

from __future__ import print_function

from verif_msi import *



c0 = constant(0, 8)
c1 = constant(0, 8)

n0 = c0 - c1
# result is 0
wres = c0

checkResults(n0, wres)

n0.dump('graph.dot')


