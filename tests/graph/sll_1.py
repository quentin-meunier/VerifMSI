#!/usr/bin/python

from __future__ import print_function

from verif_msi import *

s0 = symbol('s0', 'S', 4)
m0 = symbol('m0', 'M', 4)

c0 = Const(1, 4)

n0 = s0 << c0
n1 = n0 ^ m0

n1.dump('graph.dot')



