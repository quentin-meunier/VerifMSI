#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


k0 = symbol('k0', 'S', 8)
c0 = constant(0, 8)

n0 = c0 + k0
# result is k0

checkResults(n0, k0)

n0.dump('graph.dot')


