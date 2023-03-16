#!/usr/bin/python

from __future__ import print_function

from verif_msi import *


c0 = constant(1, 8)
c1 = constant(5, 8)
c2 = constant(6, 8)

n0 = c0 + c1

# result is 6
checkResults(n0, c2)

n0.dump('graph.dot')


